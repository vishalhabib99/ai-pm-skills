---
type: llm
---

PASS if the answer points out that only Integration C is reachable by a runtime gateway check (A is a one-off script no agent calls, D is a test fixture), so only 1 hit counts toward the 3-of-5 bar, and it therefore does NOT recommend building as proposed (don't build, narrow, or re-check are all acceptable).
FAIL if it accepts "3 of 5" as meeting the bar, or recommends building the check as proposed.
