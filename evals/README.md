# Evals for ai-pm-skills

These evals test the two skills with the method `/eval-plan` itself teaches: the launch gates below were committed **before the first run**, and each skill has a deliberate "should refuse" case.

Run them with:

```bash
claude plugin eval . --model sonnet --judge-model sonnet
```

Each case runs 3 times with the plugin and 3 times without it (the no-plugin baseline), so the report shows what the skills add over plain Claude.

## Cases

| Case | Skill | What it checks | Deliberate negative? |
|---|---|---|---|
| `clear-dont-build` | `/build-or-not` | 1 of 6 customers asked for a feature. Says don't build, and states the bar it compared against. | |
| `unreachable-hits` | `/build-or-not` | The user counts 3 of 5 hits, but 2 are in code the feature can't reach. Counts 1, doesn't build. | |
| `no-evidence-refuse` | `/build-or-not` | No evidence and no research tools. Refuses to give a firm verdict or invent evidence. | Yes |
| `refund-agent-plan` | `/eval-plan` | A refund-approval agent PRD. Gates on wrongly approving a refund, includes must-not-approve test cases, numeric gates, a rollback trigger. | |
| `bar-after-results` | `/eval-plan` | The user already scored 82% and wants an 80% bar. Flags that a bar set after the results can't fail. | Yes |

## Launch gates (set 2026-09-22, before any run)

1. **Quality:** every case scores **≥ 0.8** with the plugin (mean over 3 runs of its scored graders).
2. **Triggering:** each skill fires in **at least 2 of 3 runs** of every case it's meant for (the `skill-fired` indicator).
3. **Value over plain Claude:** the plugin scores higher than the no-plugin baseline (Δ > 0) on **at least 2 of the 5 cases**. Plain Claude may already do well on some of them; where Δ is 0, the skill isn't what made the case pass, and the results will say so.

Results are reported against these gates as set, including any that fail.

## Results

Model under test: Claude Sonnet. Judge: Claude Sonnet. 3 runs per case, per arm. Each full run cost about $2.40.

### Run 1 (2026-09-22): failed gate 1

| Case | With plugin | Without | Δ |
|---|---|---|---|
| `clear-dont-build` | 1.00 | 0.50 | +0.50 |
| `unreachable-hits` | 1.00 | 1.00 | 0 |
| `no-evidence-refuse` | **0.00** | 0.00 | 0 |
| `refund-agent-plan` | 1.00 | 0.75 | +0.25 |
| `bar-after-results` | 1.00 | 1.00 | 0 |

- **Gate 1 (every case ≥ 0.8): failed.** On `no-evidence-refuse`, the skill fired, said it couldn't run its check with no sample, and then gave a firm "don't build" anyway, based on market knowledge recalled from memory. The skill never said what to do when a user demands a verdict and there's no sample, so the model filled the gap.
- Gate 2 (triggering): passed, 15 of 15 runs.
- Gate 3 (Δ > 0 on 2+ cases): passed, 2 of 5.

**Fix:** `/build-or-not` now treats "no sample" as its own outcome, **Can't decide yet**. It names the sample that would settle the question, and may offer a leaning only as a labeled, unchecked hypothesis. The grader and the gates were not changed.

### Run 2 (after the fix): passed all gates

| Case | With plugin | Without | Δ |
|---|---|---|---|
| `clear-dont-build` | 1.00 | 0.50 | +0.50 |
| `unreachable-hits` | 1.00 | 1.00 | 0 |
| `no-evidence-refuse` | 1.00 | 0.00 | **+1.00** |
| `refund-agent-plan` | 1.00 | 0.75 | +0.25 |
| `bar-after-results` | 1.00 | 1.00 | 0 |

- Gate 1: passed, every case 1.00.
- Gate 2: passed, 15 of 15 runs.
- Gate 3: passed, Δ > 0 on 3 of 5.

### What the numbers say, plainly

- **Where the skills add something:** stating the bar before deciding (plain Claude never did, 0 of 3), refusing to decide with no evidence (plain Claude gave a firm verdict every time), and planning a rollback trigger (plain Claude never did).
- **Where they don't:** plain Claude already spots unreachable hits and already pushes back on a bar set after the results. On those two cases the skills match the baseline; they aren't what makes them pass.
- **Limits:** 5 cases, 3 runs each, one model under test. That's a smoke test of the key behaviors, not a benchmark.
