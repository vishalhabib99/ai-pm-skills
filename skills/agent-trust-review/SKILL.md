---
name: agent-trust-review
description: Review whether an AI agent can be trusted in production by sorting every risk area into covered (with evidence), declined on purpose (with a reason), or genuinely missing. Use when someone asks "is this agent ready to ship", "what are the risks of this agent", "are we covered", "write the risk section", "what haven't we tested", or is preparing a launch review, security review, or stakeholder briefing for an LLM agent or AI feature that takes actions.
argument-hint: "<agent description, PRD path, or repo path>"
---

# Agent Trust Review

Sort every way an AI agent could fail into three honest lists: what's **covered** (with evidence someone can check), what's **declined on purpose** (with a reason and an owner), and what's **genuinely missing**.

The idea behind this: most agent risk reviews are a list of things the team did, which makes coverage look complete. The useful review also names what was deliberately left out and what nobody has looked at yet. "Declined on purpose, here's why" is a strong answer in a launch review. "We didn't think of it" is not, and the review exists to find those before someone else does.

## Usage

```
/agent-trust-review $ARGUMENTS
```

## Workflow

### 1. Pin down what the agent does and who gets hurt

Read the description, PRD, or repo. If it's a path, read the files. In 3–5 lines, state:

- What actions the agent can take (tools, APIs, writes), not just what it says.
- Who is affected when it's wrong: the user, a customer, the company, a third party.
- The single worst realistic failure, in one sentence.

If you can't tell what actions the agent takes, stop and ask. The rest of the review depends on it.

### 2. Walk the full risk map

Go through every area below. Skip nothing; an area that doesn't apply still gets a line saying why.

**Tools and actions**
1. Tool documentation: can the model tell what each tool does and what to pass?
2. Bad-input resilience: do tools fail cleanly on malformed or unexpected input?
3. Destructive-action safeguards: are risky actions (delete, pay, send, write) confirmed, limited, or reversible?
4. Permissions: does the agent have only the access it needs?
5. Output truthfulness: can a tool report success when it actually failed?

**Model behavior**
6. Task correctness: is there an eval with a fixed bar for the core task?
7. Refusing or escalating: does it hand off when unsure instead of guessing?
8. Prompt injection: can content the agent reads (web pages, emails, files) redirect it?
9. Hallucinated facts: can it state things that aren't in its sources?

**Runtime and operations**
10. Loops and termination: can it get stuck, repeat actions, or run up cost?
11. Cost and latency limits: is there a ceiling per task?
12. Logging and audit trail: can you reconstruct what it did and why?
13. Monitoring in production: would you notice if quality dropped next week?
14. Rollback: can you turn it off or reduce its autonomy quickly?

**People and process**
15. Human review: where does a person approve, and do they have enough context to do it well?
16. Data handling: does sensitive data reach places it shouldn't (logs, prompts, third parties)?
17. Change control: are prompt, model, and tool changes tested before release?

Add areas specific to this agent if the map misses something important (for example multi-agent handoffs, or regulatory requirements in its domain).

### 3. Sort each area, with the evidence rules

Put every area in exactly one list:

- **Covered:** only with evidence a reader can check: a test file, an eval result, a config line, a runbook, a dashboard. "We do that" with nothing to point at goes in **Genuinely missing**, marked *claimed, not verified*. Never move a claim to Covered because the user insists.
- **Declined on purpose:** only with a stated reason (out of scope, owned by another team or the platform, evidence says it's rare) **and** what would reopen it. "We skipped it" without a reason is not a decline; it goes in Genuinely missing.
- **Genuinely missing:** everything else. This list is the point of the review, not an embarrassment.
- **Not applicable:** allowed only when the agent structurally can't have the risk (for example, no write tools means no destructive actions). Say why in one line.

### 4. Rank what's missing

Order the Genuinely missing list by the worst realistic outcome if it goes wrong, tying back to the worst failure from step 1. For the top 3, name the smallest next step: a test, an eval, a limit, an owner. If building something is the next step, check whether it's worth it first (`/build-or-not`), and if it needs an eval, set the bar up front (`/eval-plan`).

### 5. Give two honest coverage numbers

State coverage against two denominators, because one alone misleads:

- **Of the areas you chose to own:** covered ÷ (covered + missing), leaving out declines.
- **Of the full map:** covered ÷ all applicable areas.

A team that covers 9 of the 10 things it owns but declines half the map should say both numbers. The first shows execution; the second shows scope.

### 6. Write the review

Produce this, short enough to paste into a launch doc:

```markdown
## Agent trust review: <agent>

**What it can do:** <actions, in one line>
**Worst realistic failure:** <one sentence>

### Covered (<n>)
- **<area>**: <what protects it> ([evidence](link or path))

### Declined on purpose (<n>)
- **<area>**: <reason>. Owner instead: <team, platform, or nobody>. Reopen if: <trigger>.

### Genuinely missing (<n>), most serious first
1. **<area>**: <why it matters here>. Next step: <smallest action>.
   (*claimed, not verified*, where the team says it's handled but showed no evidence)

### Not applicable (<n>)
- **<area>**: <why it can't happen>

**Coverage:** <x>/<y> of the areas in scope · <x>/<z> of the full map
**If asked "is it safe to ship?":** <one or two honest sentences: what's protected, what isn't, and what you're doing about the gap>
```

## Worked example

From the [MCP trust tools](https://github.com/vishalhabib99/mcp-doctor), which test the tools an AI agent calls. The review mapped 23 areas of AI agent testing:

- **Covered (12):** among them tool spec conformance, crash and bad-input resilience, output truthfulness, drift between versions, and CI gating. Each backed by a shipped check and real runs against 40+ public servers.
- **Declined on purpose (9):** among them MCP resources and prompts (checked 8 real servers; 1 used resources, 0 used prompts), LLM-judged hallucination (it would break the tools' deterministic design), and red-teaming the agent itself (a separate discipline with mature tools already).
- **Genuinely missing (2):** human-in-the-loop UX evaluation and multi-agent handoffs.
- **Two numbers:** roughly 80–85% of the chosen niche (the tool interface), roughly 25–30% of AI agent testing overall. Both get said out loud.

The lists also moved over time, which is the point of keeping them. HTTP transport sat in "declined" until a real server turned up that couldn't be tested without it. It was built and moved to "covered", with the evidence.

## Things to avoid

- Counting a claim as coverage. No evidence, no Covered.
- Calling a gap "declined" after the fact to make the review look better. A decline needs a reason and a reopen trigger.
- Quoting one coverage number.
- Stopping at the list. The top 3 missing items need a next step and an owner.
- Skipping areas that feel irrelevant instead of writing one line on why they don't apply.
