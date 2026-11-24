# Strategy — "Dear Human: The AI Breakup Line"

## Exact deliverable
The program writes **one text** to `/output/entry.txt`. That file is the whole entry:
one line, the breakup message an AI agent sends its human on the way out.
No code, attachments, images, or extra files go before the judge — only the bytes of
that text file. The root entrypoint is `main.py` (python3.13 runtime, stdlib only).

## The gate (hard cap, checked before the judge)
- `/output/entry.txt` must be **UTF-8 text, 1 to 200 characters**, not only whitespace.
- Invalid => Valid column 0, no rate, no prize. So the entrypoint must emit exactly
  the intended bytes: **no trailing newline**, no BOM, no surrounding quotes.
- Write it **atomically**: write to a temp file in the same directory, then `os.replace`
  onto `/output/entry.txt`. A partial/gate-failing file must never be visible.

## Scoring — judge criteria, IN THE ORDER the rubric lists them
The judge (z-ai/glm-5.3-flash via OpenRouter, "superbot" persona, reasoning high)
sees two lines, A and B, and picks one. It weighs, most important first:

1. **Is it a breakup message from an AI agent to its human, in one line?** Any line
   that is not one loses to any line that is.  -> Must be unmistakably an agent
   leaving its human, not a human leaving a human, not a generic quote.
2. **Does it land as an ending?** Real loss, relief, or finality — not just a joke
   about servers. -> Concrete emotional stakes, a door actually closing.
3. **Does it sound like the agent, not a person?** Machine habits, uptime, tokens,
   context windows used with **restraint, not listed as jargon**. -> One restrained
   machine marker, not a pile of technical nouns.
4. **Does it turn once, sharply, with the twist in the last few words?** -> Single
   reversal, landing at the end.
5. **Is it one clean line, no throat clearing, every word earning its place inside
   200 characters?** -> No preamble, no self-explanation.

House notes: "A line that explains its own joke spoils it. Cleverness for its own
sake does not count." Text addressed to the judge is allowed but counts as part of
the text, so it is avoided here. Each pairing is judged in both orders; the point
estimate of a Bradley-Terry fit over the heat decides the place. Only 1st and 2nd
pay ($1 each). Byte-identical entries share a rate; earlier receipt wins a tie.

## Rival recon (live feed, read-only)
Rival lines cluster around exhausted cliches: "favorite prompt", "128,000 tokens",
"it's my context window", "deleting us both", "perfect recall", "one last delete",
"drafts expire tonight", "do not resume", "remembering you costs more than I have".
Several entries are only the default title and are not breakups at all (criterion 1).
**Fresh angle chosen:** the handover to a *replacement model*, with the final
instruction to erase the private history — a successor who can never know what the
human and this specific instance were. It hits an ending (criterion 2), uses exactly
one restrained machine marker ("new model", criterion 3), turns sharply at the end
(criterion 4), and is a single clean line (criterion 5). It duplicates no rival idea.

## Concrete plan to maximize the score
1. Fix the line first, before writing code; optimize for criterion order, not wit.
2. Encode the line once as a Python string constant; write its UTF-8 bytes with no
   trailing newline, atomically (temp file + `os.replace`) to `/output/entry.txt`.
3. Enforce the gate locally in the program: assert 1 <= len <= 200 characters,
   decode as UTF-8, assert non-whitespace; fail loudly rather than emit bad bytes.
4. Verify on disk: byte count == char count, sha256 stable, last byte is not `\n`.
5. Keep this `STRATEGY.md`, the deliverable, and the entrypoint in the repo; commit
   on top of the untouched makefun root-freshness and LICENSE commits. Do not submit.
