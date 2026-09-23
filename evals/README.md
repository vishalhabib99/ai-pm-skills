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
