# NEXUS Local Stack - Messungen Workstation JUL

Stand: 2026-11-25 01:24 Europe/Vienna, Agent ID05 (Perplexity), Messung durch USER auf der Workstation.

## Hardware (Stand: bekannt / zu verifizieren mit Test-NexusHardware.ps1)

| Parameter | Wert | Status |
|---|---|---|
| System | Lenovo Legion T5, Typ 90Q900D0GF, Hostname JUL | VERIFIED (Geraeteliste) |
| OS | Windows, PowerShell 5.1 | VERIFIED |
| CPU | Intel Core i9 (Modell offen) | PENDING (H03) |
| RAM | 32 GB | PENDING (H03) |
| GPU | NVIDIA GeForce RTX 3080 | PENDING (H01) |
| VRAM | 10 oder 12 GB | PENDING (H01) |
| NVIDIA-Treiber / max. CUDA | offen | PENDING (H01) |
| CUDA-Toolkit (nvcc) | fuer Ollama nicht noetig | PENDING (H02) |
| Ollama-Umgebung | OLLAMA_FLASH_ATTENTION=1, OLLAMA_KV_CACHE_TYPE=q8_0 (setx) | VERIFIED |

## Modellmessung qwen3.5:9b (Ollama, 2026-11-25)

| Variante | num_ctx | think | Groesse | PROCESSOR | eval tok/s | eval tokens | Status |
|---|---|---|---|---|---|---|---|
| qwen3.5:9b (Default) | 262144 | an | 13 GB | 42%/58% CPU/GPU | 7.99 | 168 | FAIL (CPU-Offload) |
| nexus-q35-9b-16k | 16384 | aus | 5.8 GB | 100% GPU | 48.43 | 263 | PASS |

- Ursache FAIL: Ollama-Default-Kontext 262144 -> KV-Cache ueberlaeuft VRAM.
- Prompt-Eval 16K: 149.90 tok/s; Warmstart 5.75 s fuer 263 Tokens; Kaltstart Laden 7.8 s.
- Entscheidung: Standardmodell `nexus-q35-9b-16k` (Modelfile `FROM qwen3.5:9b` + `PARAMETER num_ctx 16384`).
- Fachgrenze: EC2-Probeantwort fachlich fehlerhaft -> Modell nur fuer Steuerung/Zusammenfassung/Tools/Code; Normaussagen und Bemessung nur ueber deterministische Rechenkerne + menschliche Freigabe.

## Offene Abnahmetests (Test-NexusHardware.ps1)

H01 GPU/Treiber, H02 CUDA-Toolkit, H03 CPU/RAM/Disk, E01/E02 Ollama-Version/Env,
B* Speed/GPU 16K/32K/64K (+ 4B-Fallback mit -PullFallback) inkl. CPU-Last und VRAM,
L01 Langer Prompt (~12k Tokens, Nadel-Test), F01 Tool-Calling, F02 JSON-Schema,
F03 Thinking, F04 Vision/OCR, F05 Embeddings, S01 Modellwechsel.

Aufruf:

```powershell
powershell -ExecutionPolicy Bypass -File .\local_stack\windows\Test-NexusHardware.ps1
```
