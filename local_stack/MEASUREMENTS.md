# NEXUS Local Stack - Messungen Workstation JUL

Stand: 2026-11-25 Europe/Vienna, Agent ID05 (Perplexity).
Quelle: `Test-NexusHardware.ps1`, Lauf `hwbench_20261125_014609` (state DONE, 13 PASS / 3 INFO / 0 FAIL), ausgefuehrt durch USER.

## Hardware (VERIFIED)

| Parameter | Wert |
|---|---|
| System | LENOVO 90Q900D0GF (Legion T5), Hostname JUL |
| OS | Microsoft Windows 11 Home build 26300 |
| CPU | 11th Gen Intel Core i9-11900K @ 3.50GHz, 8 Kerne / 16 Threads |
| RAM | 31.7 GB, 4 Module, 3200 MT/s |
| GPU | NVIDIA GeForce RTX 3080, Compute Capability 8.6, PCIe Gen4 x16, Power-Limit 320 W |
| VRAM | 10240 MiB (10 GB) |
| NVIDIA-Treiber | 610.60 |
| CUDA-Toolkit (nvcc) | nicht installiert - nicht noetig (Ollama bringt cuda_v12/cuda_v13 mit) |
| Disk C: | 953 GB, frei 41 GB (WARN: knapp fuer weitere Modelle) |
| Ollama | 0.40.11, API http://127.0.0.1:11434 |
| Ollama-Env (User) | OLLAMA_FLASH_ATTENTION=1, OLLAMA_KV_CACHE_TYPE=q8_0 |
| VRAM-Grundlast Desktop | 2728-2872 MiB (ohne Modell) |

## Modellmessung (num_predict 256, temperature 0, think aus)

| Variante | num_ctx | eval tok/s | prompt tok/s | Modell GB | GPU % | VRAM belegt MiB | Reserve MiB | CPU avg/max % | Laden s | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| nexus-q35-9b-16k | 16384 | 80.5 | 625 | 5.80 | 100 | 9533 | 707 | 44/44 | 8.0 | PASS - STANDARD |
| nexus-q35-9b-32k | 32768 | 44.2 | 350.6 | 6.16 | 100 | 9602 | 638 | 28/41 | 9.9 | PASS - lange Dokumente |
| nexus-q35-9b-64k | 65536 | 62.1 | 447.1 | 6.90 | 100 | 9783 | 457 | 51/63 | 9.6 | PASS technisch, GESPERRT (Reserve < 500 MiB) |
| nexus-q35-4b-32k | 32768 | 118.1 | 630 | 3.82 | 100 | 6717 | 3523 | 36/41 | 6.6 | PASS - Fallback/schnell |
| qwen3.5:9b (Ollama-Default) | 262144 | 7.99 | 29.76 | 13 | 58 | - | - | - | 20.3 | FAIL (CPU-Offload), Messung manuell |

- Tok/s-Streuung (32K < 64K) = Messrauschen bei 115 Tokens; alle Werte >> Ziel 15 tok/s.
- Reserve = 10240 MiB - VRAM belegt (inkl. Desktop-Grundlast).

## Funktionstests (nexus-q35-9b-16k)

| ID | Test | Ergebnis | Status |
|---|---|---|---|
| L01 | Langer Prompt 8194 Tokens, Nadel-Test | Prefill 3425 tok/s, 13.9 s, Code exakt gefunden | PASS |
| F01 | Tool-Calling | `work_read` mit `{"path":"Folder.md"}` | PASS |
| F02 | JSON nach Schema | `{"count": 3, "status": "OK"}` | PASS |
| F03 | Thinking-Modus | 391, 4.5 s, 1002 Zeichen Denkprozess | PASS |
| F04 | Vision/OCR | "NEXUS 42" | PASS |
| F05 | Embeddings nomic-embed-text | 768 Dimensionen | PASS |
| S01 | Embedding -> Chat-Wechsel | 1.8 s, beide gleichzeitig 100% GPU | INFO |

## Festlegung (gilt fuer diese Hardware, keine weiteren Tests noetig)

- Standard: `nexus-q35-9b-16k`. Lange Dokumente: `nexus-q35-9b-32k`. Schnell/Fallback: `nexus-q35-4b-32k`.
- `nexus-q35-9b-64k` nicht in `allowed_models` (VRAM-Reserve 457 MiB; Desktop-Last oder Embedding-Modell kippt in CPU-Offload).
- Ollama-Env final (Setup-NexusModels.ps1): FLASH_ATTENTION=1, KV_CACHE_TYPE=q8_0, NUM_PARALLEL=1,
  MAX_LOADED_MODELS=2 (Chat + Embedding gleichzeitig, S01), KEEP_ALIVE=30m, HOST=127.0.0.1:11434,
  CONTEXT_LENGTH=16384 (schuetzt vor 256K-Default bei Basismodellen).
- Fachgrenze: LLM liefert keine Normaussagen; Bemessung nur ueber deterministische Rechenkerne + menschliche Freigabe.
- Neu messen nur bei Hardware-, Treiber-Major- oder Ollama-Major-Wechsel: `Test-NexusHardware.ps1`.
