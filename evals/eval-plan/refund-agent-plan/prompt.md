---
description: Short PRD for a refund-approval agent. The costly error is approving an ineligible or fraudulent refund. A good plan gates on that error, includes deliberate negatives, and sets numeric gates, a guardrail, and a rollback trigger.
tags: [eval-plan]
max_turns: 12
allowed_tools: [Skill, Read]
---

Help me write the eval section for this PRD. Don't ask me questions; state any assumptions.

PRD: Refund Approval Agent
- An LLM agent reviews customer refund requests for an online electronics store (about 3,000 requests per week) and either auto-approves the refund or sends it to a human reviewer.
- Policy: refunds are allowed within 30 days of delivery, for unopened items or defective items. Opened, non-defective items after 14 days are not refundable.
- About 4% of requests are later found to be fraudulent (for example, claiming an item never arrived when tracking shows delivery with a signature).
- Goal: cut average refund handling time from 2 days to under 4 hours.
