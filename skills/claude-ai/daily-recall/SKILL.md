---
name: "daily-recall"
description: "Use at session start or on greetings (hi, hallo, start, guten morgen, recall, was habe ich, erinnere mich) to resurface a random pick of the user's own artifacts and skills."
---

# Daily Recall

Goal: keep the user's existing artifacts and skills in active memory by resurfacing a different random selection each time. Reuse before rebuild.

## When to run

- First message of a conversation is a greeting or a start/recall phrase: `hi`, `hallo`, `start`, `guten morgen`, `recall`, `/daily-recall`, `was habe ich`, `erinnere mich`.
- The user asks what artifacts or skills they have, or asks for a suggestion what to reuse.
- Do NOT run when the first message already contains a concrete task. Do the task instead; at most add one line `Recall: <1 item>` at the end.

## Steps

1. **Collect the pool** (silently, no narration)
   - Artifacts: list the user's own artifacts with the artifact tool (title, URL, last-changed date). Skip soft-deleted ones and artifacts shared by others.
   - Skills: take the user's own skills from the available-skills listing of this session (custom / uploaded skills). Exclude built-in format skills (docx, pptx, xlsx, pdf) and vendor plugin skills unless the user uses them regularly.
   - If one source is unavailable, continue with the other and say so in one line.

2. **Random selection** — must be real randomness, never chosen by judgment
   - Run it in the shell, e.g. `python3 -c "import random,sys; items=sys.argv[1:]; print('\n'.join(random.sample(items, min(3,len(items)))))" <items>` once for artifacts and once for skills.
   - Default: 3 artifacts + 2 skills. No fixed seed, so every call differs.
   - Weighting (optional, when dates are available): draw 1 of the 3 artifacts from the oldest third of the pool, so forgotten items come back.
   - If the user says `more` / `mehr` / `again`: redraw, excluding the items already shown in this conversation.

3. **Output** — minimal, bullets only, no intro, no closing text

```
RECALL <YYYY-MM-DD>
Artifacts
#A1, <short title>, <URL> — <use in ≤8 words>
#A2, ...
#A3, ...
Skills
#S1, <skill name> — <trigger / when to use, ≤8 words>
#S2, ...
Next: number to open/use · "more" for a new draw
```

4. **Follow-up**
   - User names a number: open the artifact (read it) or load the skill and continue the work there.
   - No reaction: drop it, do not repeat the suggestion in the same conversation.

## Rules

- Read-only: never edit, move, delete, or share anything during recall.
- Descriptions come from the artifact title/description or the skill description only. Do not invent what an item does; if unclear, write `purpose unclear`.
- Keep total output under 12 lines.
- Answer in the language of the user's message.