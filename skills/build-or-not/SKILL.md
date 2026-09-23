---
name: build-or-not
description: Decide whether to build a proposed feature by checking a small sample of real, in-the-wild examples before writing a spec or any code. Use when someone says "we should add X", "should we build this", "is this worth building", "what should we build next", or proposes a new check, integration, or capability based on intuition rather than evidence. Produces a decision record: build, don't build, or narrow and re-check.
argument-hint: "<the feature or capability being proposed>"
---

# Build or Not

Decide whether a proposed feature is worth building by checking it against a small sample of real examples before anyone writes a spec or any code.

The idea behind this: most bad builds are not badly executed, they are features for a problem that turns out to be rare, unreachable, or already solved. You can usually find that out in an hour by looking at 4–8 real cases. A clear "don't build, and here's the evidence" is a deliverable, not a failure.

## Usage

```
/build-or-not $ARGUMENTS
```

## Workflow

### 1. Turn the idea into a claim you could be wrong about

Restate the proposal as a claim about the real world that the sample can confirm or refute. Push back on a proposal that can't be stated this way.

- Vague: "We should add a governance/compliance check."
- Checkable: "Real MCP servers that handle financial data log account identifiers unredacted in code paths an agent can trigger."

If the proposal is a whole category ("governance", "observability", "better onboarding"), it is too broad to check directly. Narrow it to **one concrete, observable pattern** first, and say that you narrowed it. A broad category that can't be narrowed to something observable is itself a signal: note it in the record.

### 2. Choose the sample *before* looking at it

Pick 4–8 real examples that the feature would act on: real repos, real customer accounts, real support tickets, real transcripts, real competitor products. Choose them with a stated rule so you don't pick the ones that confirm the idea:

- Prefer real, in-the-wild cases over your own projects, demos, or hypotheticals.
- Spread the sample over the variation that matters (size, language, customer segment, vendor).
- Write down the selection rule and the list before checking any of them.

If you have tools (web search, `gh`, code search, file access, a connected analytics or ticketing tool), gather the sample yourself. If not, ask the user for the examples and don't invent any.

### 3. Set the bar in advance

Before looking, write down:

- **What counts as a hit**, precisely enough that two people would score the same case the same way.
- **The build threshold**: how many hits out of the sample justify building. A reasonable default is 3+ out of 8 for a common-case feature, or 1 severe, reachable hit for a safety or security feature.
- **What would change your mind** in the other direction.

Setting the bar afterwards lets the result decide the bar. Don't do that.

### 4. Check each example and record evidence

For each example, record:

| # | Example | Hit / Miss / N/A | Evidence | Reachable? |
|---|---|---|---|---|

- **Evidence** must be something a reader can check: a file and line, a link, a quote, a screenshot, a query result. "Seems like it" is not evidence.
- **Reachable?** asks whether the hit sits where the feature would actually act. A real problem in a setup script, an internal admin path, or a deprecated flow may not be something your feature can see or fix. Count only reachable hits toward the threshold, and list the unreachable ones separately.
- Use **N/A** when the example turns out not to fit the question (for example, a repo that only serves public data can't test a PII check). Replace it with another example if you can, and say so.

### 5. Decide

Compare reachable hits against the threshold you set in step 3 and pick exactly one outcome:

- **Build.** Name the smallest version that serves the hits you found, and point to the real examples that will serve as its first test cases.
- **Don't build.** State the evidence in one sentence ("1 of 8 real servers used the feature; the check would mostly report nothing"). Add it to a "declined on purpose" list so the question doesn't get relitigated from scratch next quarter.
- **Narrow and re-check.** The broad idea failed but a narrower claim looks promising. Restate it and repeat from step 1. Allow this at most twice before deciding.

Never report a decision the evidence doesn't support. If the sample was too small or too skewed to decide, say that plainly and name the extra examples that would settle it.

### 6. Write the decision record

Produce this, and keep it short enough to paste into a PRD, a ticket, or a Slack thread:

```markdown
## Build or not: <feature>

**Claim checked:** <the falsifiable claim from step 1>
**Sample:** <N> real examples, chosen by <selection rule>
**Bar (set before checking):** hit = <definition>; build if <threshold>

| # | Example | Result | Evidence | Reachable? |
|---|---|---|---|---|
| 1 | ... | Hit | link / file:line | Yes |

**Result:** <reachable hits>/<N> reachable hits (<unreachable hits> more that the feature couldn't reach)
**Decision:** Build / Don't build / Narrow and re-check
**Why, in one sentence:** ...
**What would reopen this:** <the evidence that would change the decision>
```

## Worked examples

These come from building the [MCP trust tools](https://github.com/vishalhabib99/mcp-doctor), where each of these decisions was actually made this way.

**Don't build: an audit for MCP resources and prompts.** Claim: real MCP servers use the resources/prompts primitives enough that auditing them matters. Sample: 8 real servers. Result: 1 of 8 used them. Decision: don't build. The audit would have reported "nothing to check" on almost every server.

**Narrow, then don't build: a governance/compliance check.** "Governance" was too broad to check, so it was narrowed to one observable pattern: a financial or personal identifier logged unredacted. Sample: 4 real servers handling regulated-looking data (one was later marked N/A because it only serves public data). Result: exactly 1 real hit, a bank account number and holder name logged in a sync script, but outside any code path an agent's tool call could trigger. Reachable hits: 0. Decision: don't build. It went on the "declined on purpose" list with that evidence.

**Build: remote (HTTP) transport for the runtime testers.** Claim: stdio-only support blocks testing real servers. Evidence found in work already underway: a real CRM server that supports HTTP could only be reached over stdio. Decision: build the smallest version (connect over HTTP with custom headers). The first real run over HTTP immediately exposed a crash-handling bug that stdio had hidden.

## Things to avoid

- Checking only your own projects or the examples the requester suggested.
- Moving the threshold after seeing the results.
- Counting hits the feature could never reach.
- Treating "don't build" as a failure. It saves the most time of the three outcomes.
- Reporting "we checked everything" when you checked 6 examples. Say how many were checked.
