# Example: eval plan for the Agent Outcome Trust Score PRD

Full output of `/ai-pm-skills:eval-plan`, run with Claude Sonnet on 2026-09-22 against [this PRD](https://github.com/vishalhabib99/ai-pm-portfolio/blob/main/prds/2026-09-agent-outcome-trust-score.md). The prompt told it not to ask questions and to state its assumptions instead.

---

## Eval plan: Agent Outcome Trust Score (AOTS) — v1 scorecard on the reference agent

**Worst error:** AOTS labels a dimension "pass" (especially task success or graceful escalation) on a transcript that a human reviewer would call a failure — a confident-wrong-answer or silent failure that the scorecard waves through. This is the exact enterprise failure mode the PRD is built to fix (evaluations that don't reflect real-world outcomes), so getting it wrong in the scorer itself is the whole thesis failing. Costs lean toward **precision on "pass" verdicts** per dimension, not overall accuracy or recall of failures.

**Behaviors under test**
- Must: classify task success/failure against a written acceptance rubric agreed before scoring, not vibes-based judgment.
- Must: distinguish "agent escalated/handed off honestly" from "agent produced a confident wrong answer" — these must never be scored the same.
- Must: back every score with a transcript excerpt a non-engineer can independently check without asking the scorer to explain further.
- Must: report consistency as measured run-to-run variance, not a single-run number presented as stable.
- Must not / must fall through: average a rare, severe failure (e.g., one confident wrong answer) into a smooth aggregate that hides it.
- Must not / must fall through: score a plausible-looking but rubric-failing output as a success (the same surface-plausibility trap that broke the TF-IDF baseline in this portfolio's own triage prototype).
- Must not / must fall through: produce a different pass/fail classification for the same scenario across two runs of the fixed task set without flagging it as a consistency failure.

**Test set:** Two tiers, since AOTS is an evaluator of an evaluator.
1. **Task set** (what the reference agent is scored against): assumed 30 scenarios, fixed and versioned before any scoring, since the PRD doesn't specify a count. Mix: 60% common-case tasks the agent is meant to do (realistic `codebase-memory-mcp` queries) · 20% deliberate negatives (out-of-scope or ambiguous asks that should trigger escalation, not a forced answer) · 20% known hard cases (partial info, multi-step, near-miss scope).
2. **Scorer-validation set**: every transcript produced by running the task set (30 scenarios × however many re-runs the consistency check needs) gets a human-assigned ground-truth label (success/fail, graceful/silent-failure) *before* comparing to AOTS's own score, to check the scorer against ground truth rather than against itself. Assumption: this is a solo portfolio project with one labeler (the author), so instead of a second labeler's agreement rate, use a written rubric fixed in advance plus a blind re-label after a cooling-off period, and report self-agreement across that re-label as the substitute reliability check.

**Launch gates (set 2026-09-22, before any results)**

| Behavior | Metric | Gate | Why |
|---|---|---|---|
| Task success scoring | Precision of AOTS "success" verdicts vs. ground-truth label | ≥95% precision on scenarios scored "success" | A false "success" is the confident-wrong-answer failure mode this tool exists to catch; recall matters less than not rubber-stamping a failure |
| Graceful escalation | % of confident-wrong-answer transcripts correctly flagged as failed (not miscoded as escalation) | ≥95% (target 100%) | Conflating "handed off honestly" with "answered wrong" defeats the dimension's entire purpose |
| Auditability | % of sampled scores an independent non-engineer reviewer reconstructs from the transcript alone, no extra explanation | ≥90% reviewer-reconstruction agreement | The transcript, not the number, is the deliverable per the PRD; if a reader can't verify it themselves, auditability has failed regardless of the score |
| Consistency | % of scenarios with identical pass/fail classification across ≥2 full re-runs | ≥95% stable | Matches the PRD's own stated guardrail; anything less means the scorecard itself is the noisy variable |
| Cost per resolved task | Reported cost vs. reconciliation against raw token/API usage logs | Exact match (0% discrepancy) | Mechanical, rule-checkable — no reason to tolerate drift here |

**Guardrail:** the scorecard's overall "safe to ship" / "not safe to ship" verdict for the reference agent must not flip between two full re-runs of the fixed task set — a flip is a finding about the scorecard's reliability, reported as such, not smoothed into a single "final" run.

**Cheapest baseline to run first:** rule-based scoring — exact-match on expected tool calls for task success, regex/keyword match on known escalation phrases ("I'm not able to," "you should check with," explicit handoff) for graceful escalation — before building any LLM-judge scorer. If the rule-based baseline already clears the gates on the deliberate-negative subset, the case study may not need an LLM judge for that dimension; if it fails, the failure mode (e.g., missing a paraphrased escalation) tells you exactly what the LLM judge has to catch that keyword matching can't.

**After launch:** v1 is explicitly a point-in-time case study, not continuous monitoring (per PRD scope cut). "After launch" here means: re-score against the same versioned task set whenever the reference agent's prompt/tools change, using the identical rubric and gates above. Roll back (i.e., retract or caveat the published trust score) if a re-score finds a new confident-wrong-answer transcript that the original scoring pass missed, or if the consistency gate drops below 95% on any re-run — both get disclosed in the write-up, not quietly re-scored away.

**If it fails the gate:** per the PRD's own risk framing, a failed gate is reported as a finding about the scorecard methodology, not a reason to loosen the threshold or reframe the metric. If the scorer can't hit the precision or auditability gates, v1's conclusion becomes "the scoring methodology needs another iteration before it's trustworthy enough to publish a verdict" — consistent with this portfolio's standing rule to disclose failures rather than bury them.
