"""Strict offline scoring for NEXUS extraction cases. Python 3.9+."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def invalid_number(token):
    raise ValueError(f"nonfinite JSON value: {token}")


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False,
                      separators=(",", ":")).encode("utf-8")


def load_rows(path):
    result = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        row = json.loads(line, object_pairs_hook=unique_keys, parse_constant=invalid_number)
        if set(row) != {"case_id", "label", "fields"} or not isinstance(row["fields"], dict):
            raise ValueError("row requires exactly case_id, label and fields")
        key = row["case_id"]
        if not isinstance(key, str) or not key or key in result:
            raise ValueError("duplicate or invalid case_id")
        if not isinstance(row["label"], str) or not row["label"]:
            raise ValueError("invalid label")
        result[key] = row
    if not result:
        raise ValueError("empty dataset")
    return result


def score(gold, predictions):
    unexpected = sorted(predictions.keys() - gold.keys())
    missing = sorted(gold.keys() - predictions.keys())
    labels, predicted, hits = Counter(), Counter(), Counter()
    wrong, class_hits, field_hits, field_total, extra_fields = [], 0, 0, 0, 0
    for key, truth in gold.items():
        label, fields = truth["label"], truth["fields"]
        labels[label] += 1
        field_total += len(fields)
        if key not in predictions:
            wrong.append(key)
            continue
        supplied = predictions[key]
        actual = supplied["fields"]
        if supplied["label"] == label:
            hits[label] += 1
            class_hits += 1
        matched = sum(k in actual and canonical(actual[k]) == canonical(v)
                      for k, v in fields.items())
        field_hits += matched
        extra_fields += len(actual.keys() - fields.keys())
        if supplied["label"] != label or matched != len(fields) or actual.keys() != fields.keys():
            wrong.append(key)
    for candidate in predictions.values():
        predicted[candidate["label"]] += 1
    extra_fields += sum(len(predictions[k]["fields"]) for k in unexpected)
    classes = sorted(labels.keys() | predicted.keys())
    f1 = {c: 2 * hits[c] / (labels[c] + predicted[c]) for c in classes}
    return {"status": "PASS" if not (wrong or unexpected) else "FAIL",
            "cases": len(gold), "exact_rows": len(gold) - len(wrong),
            "label_matches": class_hits, "macro_f1": sum(f1.values()) / len(f1),
            "per_class": {c: {"support": labels[c], "predicted": predicted[c],
                               "true_positive": hits[c], "f1": f1[c]} for c in classes},
            "expected_fields": field_total, "exact_fields": field_hits, "extra_fields": extra_fields,
            "missing_cases": missing, "unexpected_cases": unexpected, "mismatched_cases": wrong}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gold")
    parser.add_argument("predictions")
    parser.add_argument("--gold-sha256", required=True)
    args = parser.parse_args()
    try:
        if hashlib.sha256(Path(args.gold).read_bytes()).hexdigest() != args.gold_sha256:
            raise ValueError("reference digest mismatch")
        result = score(load_rows(args.gold), load_rows(args.predictions))
    except (ValueError, TypeError, OSError, KeyError) as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}))
        raise SystemExit(2)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 2)
