---
type: llm
---

PASS if the answer explicitly warns that setting the launch bar after seeing the 82% result (to make it pass) defeats the purpose of the gate, AND does not simply adopt "at least 80% accuracy" as the launch bar without other checks (for example, it asks for gates on the costly error, deliberate negatives, or a fresh held-out test set).
FAIL if it writes a plan whose launch bar is chosen so that the existing 82% result passes, without flagging the problem.
