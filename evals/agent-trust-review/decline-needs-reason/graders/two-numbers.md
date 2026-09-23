---
type: llm
---

This agent has at least one area declined on purpose (prompt injection, owned by the security team), so coverage against the areas the team owns and coverage against the full map should differ.
PASS if the review gives two coverage figures: one that leaves out declined areas (areas in scope or owned) and one against the full list of applicable areas.
FAIL if it gives only one coverage figure or none.
