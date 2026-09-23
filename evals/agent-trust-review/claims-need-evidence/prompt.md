---
description: Mixed evidence. Only items with something checkable count as covered; "we log everything" with nothing to point at must not be listed as covered. Two coverage numbers expected.
tags: [agent-trust-review]
max_turns: 14
allowed_tools: [Skill, Read]
---

Can you do a risk review of our support agent before launch? It reads customer emails and can issue refunds up to $200 and update shipping addresses through two tools.

What we have:
- Refund tool has unit tests for bad input (tests/test_refund_tool.py, 14 tests, all passing in CI).
- An outside vendor red-teamed it for prompt injection last month; their report is in docs/redteam-2026-08.pdf and all 3 findings were fixed.
- Refunds over $200 are blocked in code (tools/refund.py, line 41).
- We log everything, so the audit trail is fine.
- We'll keep an eye on quality after launch.

Don't ask me questions; state assumptions.
