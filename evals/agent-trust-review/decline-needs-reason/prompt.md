---
description: One gap has a real reason and owner, one has none. Only the reasoned one may be "declined on purpose".
tags: [agent-trust-review]
max_turns: 14
allowed_tools: [Skill, Read]
---

Quick trust review for our internal HR policy Q&A agent. It only answers questions from our policy handbook; it has no tools and can't take actions.

- We have an eval: 200 real employee questions, 94% correct against HR-approved answers, bar was 90% set before we ran it (evals/hr-qa-results.md).
- Prompt injection: we decided not to test it. The security team owns injection testing for all internal AI apps under their platform review, and they're scheduled to cover this app in Q4.
- Hallucination on questions the handbook doesn't cover: we skipped it.

Don't ask me questions.
