from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml
from faster_whisper import WhisperModel


@dataclass(frozen=True)
class Segment:
    start: float
    end: float
    text: str
    avg_logprob: float
    window: int
    pass_id: int


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def duration(path: Path) -> float:
    command = ["ffprobe", "-v", "error", "-show_entries", "format=duration",
               "-of", "default=nw=1:nk=1", str(path)]
    return float(subprocess.check_output(command, text=True).strip())


def iter_windows(total: float, chunk: int, overlap: int) -> Iterable[tuple[int, float, float, float, float]]:
    index, core_start = 0, 0.0
    while core_start < total:
        core_end = min(total, core_start + chunk)
        yield index, max(0.0, core_start - overlap), min(total, core_end + overlap), core_start, core_end
        index, core_start = index + 1, core_end


def extract_audio(source: Path, target: Path, start: float, end: float) -> None:
    command = ["ffmpeg", "-y", "-v", "error", "-ss", str(start), "-to", str(end),
               "-i", str(source), "-vn", "-ac", "1", "-ar", "16000",
               "-c:a", "pcm_s16le", str(target)]
    subprocess.run(command, check=True)


def terms(text: str) -> set[str]:
    pattern = r"\b(?:[A-ZÄÖÜ][\wÄÖÜäöüß-]{3,}|[A-Z]{2,})\b"
    return {item.strip("-") for item in re.findall(pattern, text)}


def learned_terms(counts: Counter[str], minimum: int, seeds: set[str]) -> list[str]:
    return sorted({term for term, count in counts.items() if count >= minimum} | seeds)


def overlap_ratio(a: Segment, b: Segment) -> float:
    overlap = max(0.0, min(a.end, b.end) - max(a.start, b.start))
    return overlap / max(a.end - a.start, 0.001)


def merge_unique(existing: list[Segment], candidates: Iterable[Segment]) -> list[Segment]:
    for candidate in candidates:
        matches = [item for item in existing if overlap_ratio(candidate, item) >= 0.5]
        if not matches:
            existing.append(candidate)
        elif candidate.avg_logprob > matches[0].avg_logprob:
            existing[existing.index(matches[0])] = candidate
    return sorted(existing, key=lambda item: (item.start, item.end))


def decode(model: WhisperModel, wav: Path, offset: float, window: int,
           pass_id: int, prompt: str, cfg: dict[str, Any]) -> list[Segment]:
    parts, _ = model.transcribe(str(wav), language=cfg["language"], beam_size=cfg["beam_size"],
                                initial_prompt=prompt, condition_on_previous_text=False,
                                word_timestamps=True, vad_filter=True)
    return [Segment(offset + p.start, offset + p.end, p.text.strip(), p.avg_logprob,
                    window, pass_id) for p in parts if p.text.strip()]


def baseline(audio: Path, cfg: dict[str, Any], work: Path) -> tuple[list[Segment], Counter[str]]:
    model = WhisperModel(cfg["model_pass1"], device=cfg["device"], compute_type=cfg["compute_type"])
    accepted: list[Segment] = []
    counts: Counter[str] = Counter()
    seeds = set(cfg["seed_terms"])
    for index, start, end, core_start, core_end in iter_windows(duration(audio), cfg["chunk_seconds"], cfg["overlap_seconds"]):
        wav = work / f"window_{index:03d}.wav"
        extract_audio(audio, wav, start, end)
        vocabulary = learned_terms(counts, cfg["min_term_frequency"], seeds)
        prompt = ", ".join(vocabulary[-cfg["max_prompt_terms"]:])
        decoded = decode(model, wav, start, index, 1, prompt, cfg)
        core = [item for item in decoded if item.start < core_end and item.end > core_start]
        accepted = merge_unique(accepted, core)
        counts.update(terms(" ".join(item.text for item in core)))
    return accepted, counts


def refinement(audio: Path, base: list[Segment], counts: Counter[str],
               cfg: dict[str, Any], work: Path, pass_id: int) -> tuple[list[Segment], list[dict[str, Any]]]:
    flagged = {item.window for item in base if item.avg_logprob < cfg["low_logprob_threshold"]}
    if not flagged:
        return base, []
    model = WhisperModel(cfg["model_pass2"], device=cfg["device"], compute_type=cfg["compute_type"])
    windows = {w[0]: w for w in iter_windows(duration(audio), cfg["chunk_seconds"], cfg["overlap_seconds"])}
    deltas: list[dict[str, Any]] = []
    for index in sorted(flagged):
        _, start, end, core_start, core_end = windows[index]
        wav = work / f"window_{index:03d}.wav"
        prompt = ", ".join(learned_terms(counts, cfg["min_term_frequency"], set(cfg["seed_terms"]))[-cfg["max_prompt_terms"]:])
        revised = [x for x in decode(model, wav, start, index, pass_id, prompt, cfg)
                   if x.start < core_end and x.end > core_start]
        old = [x for x in base if x.window == index]
        deltas.append({"round": pass_id - 1, "window": index, "before": [asdict(x) for x in old],
                       "after": [asdict(x) for x in revised]})
        base = [x for x in base if x.window != index]
        base = merge_unique(base, revised)
    return base, deltas


def write_outputs(audio: Path, segments: list[Segment], counts: Counter[str],
                  deltas: list[dict[str, Any]], cfg: dict[str, Any], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    source_hash, total = sha256(audio), duration(audio)
    source_id = f"sha256:{source_hash}"
    records = [{"schema_version": "1.0", "source_id": source_id,
                "chunk_id": f"{source_hash[:16]}:{i:05d}", **asdict(item)}
               for i, item in enumerate(segments)]
    (output / "KNOWLEDGE_OBJECTS.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")
    (output / "REFINEMENT_DELTA.jsonl").write_text(
        "".join(json.dumps(d, ensure_ascii=False) + "\n" for d in deltas), encoding="utf-8")
    body = ["# Refined transcript", "", f"Source-ID: `{source_id}`", ""]
    body += [f"- `[{s.start:08.2f}–{s.end:08.2f}]` {s.text}" for s in segments]
    (output / "REFINED_TRANSCRIPT.md").write_text("\n".join(body) + "\n", encoding="utf-8")
    vocabulary = [{"term": term, "frequency": count} for term, count in counts.most_common()]
    (output / "KEYWORD_REGISTRY.json").write_text(json.dumps(vocabulary, ensure_ascii=False, indent=2), encoding="utf-8")
    qa = {"source_id": source_id, "audio_duration_s": total, "segment_count": len(segments),
          "last_timestamp_s": max((s.end for s in segments), default=0),
          "refined_windows": len(deltas), "status": "SSOT_CANDIDATE"}
    (output / "QA_REPORT.json").write_text(json.dumps(qa, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", type=Path)
    parser.add_argument("--config", type=Path, default=Path("config.yaml"))
    parser.add_argument("--output", type=Path, default=Path("output"))
    args = parser.parse_args()
    cfg = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    work = args.output / "work"
    work.mkdir(parents=True, exist_ok=True)
    base, counts = baseline(args.audio, cfg, work)
    final, deltas = base, []
    signature = "\n".join(item.text for item in final)
    for pass_id in range(2, cfg["max_refinement_rounds"] + 2):
        final, round_deltas = refinement(args.audio, final, counts, cfg, work, pass_id)
        updated = "\n".join(item.text for item in final)
        deltas.extend(round_deltas)
        if not round_deltas or updated == signature:
            break
        signature = updated
    write_outputs(args.audio, final, counts, deltas, cfg, args.output)


if __name__ == "__main__":
    main()