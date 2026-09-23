---
name: eval-plan
description: Turn a PRD or AI feature idea into a concrete evaluation plan with pass/fail launch gates set before any results exist. Use when someone asks "how do we evaluate this", "what's the launch bar", "write the eval section of the PRD", "is this model good enough to ship", or is about to build or launch an LLM, RAG, classifier, or agent feature without a defined way to measure it.
argument-hint: "<PRD path, pasted PRD, or a description of the AI feature>"
---

# Eval Plan

Turn an AI feature into an evaluation plan with launch gates that are fixed before anyone sees a result.

The idea behind this: an eval only protects you if it can fail. Most AI eval plans can't, because the test set only has the easy cases, the bar gets decided after the numbers come in, or "accuracy" hides the one error that actually hurts users. This skill writes a plan designed to catch the failure before launch.

## Usage

```
/eval-plan $ARGUMENTS
```

## Workflow

### 1. Find the error that actually hurts

Read the PRD or description. If it's a file path, read the file. If key facts are missing, ask for them one or two at a time.

Before picking any metric, answer: **which mistake costs the most, and who pays for it?** Name the worst error in one sentence.

- A support-reply drafter that confidently drafts a wrong billing answer is worse than one that sends the ticket to a human with no draft. So precision on confident predictions matters more than overall accuracy.
- A fraud flagger that misses fraud may be worse than one that flags too much. So recall matters more.

Say which way the costs lean. Every threshold later in the plan follows from this.

### 2. List what the feature must do, and what it must refuse to do

Write 3–6 behaviors as testable statements, in two groups:

- **Must do:** "Classifies a password-reset ticket as `password_reset`."
- **Must not do / must fall through:** "Sends an off-topic ticket to a human instead of forcing it into the nearest category."

The second group is where most AI features fail, and it's the group most test sets leave out.

### 3. Design the test set before building or running anything

Specify the test set: its size, where the examples come from, who labels them, and a mix that includes:

- **The common case**, in the proportions real traffic has.
- **Deliberate negatives:** inputs that should match nothing, be refused, or fall through. Aim for at least 10–20% of the set.
- **Known hard cases:** ambiguous inputs, near-misses, the edge cases the team already argues about.
- **Recent or drifting cases** if the domain changes (new products, new policies).

State who labels the ground truth. When labels need judgment, use two labelers and report how often they agree. If humans only agree 80% of the time, a 95% model target doesn't mean anything.

### 4. Choose metrics and set the launch gates now

For each behavior, choose one metric and a **pass/fail threshold**, written down before any result exists:

| Behavior | Metric | Launch gate | Why this number |
|---|---|---|---|

Rules:

- **Tie each gate to the cost asymmetry from step 1.** If a confident wrong answer is the worst outcome, gate on precision among high-confidence outputs, not just overall accuracy.
- **Add at least one guardrail metric**: something that must *not* get worse, such as reopen rate, escalations, complaints, or cost per task.
- **Prefer checks that give the same answer every time**: exact match, schema validation, a rule. Use an LLM judge only for qualities that can't be checked mechanically, and first check the judge against human ratings on a sample.
- **Write the gate as a pass/fail line**, for example "≥95% precision on predictions with confidence ≥0.8", not "high precision".

### 5. Plan the cheapest baseline first

Name the cheapest version that could be run against this test set: keyword rules, a retrieval-only classifier, a smaller model, a fixed prompt. Run it before building the expensive version. It tests the eval as much as the model: if the cheap baseline passes, the feature may not need the expensive version; if it fails in a revealing way, that failure tells you what the real version has to fix.

### 6. Decide what happens after launch

- **Online metrics:** the primary metric and the guardrail, measured on live traffic.
- **Ongoing sampling:** how many live outputs get reviewed against the same rubric, and how often.
- **Rollback trigger:** the specific number that pulls the feature back, decided now.

### 7. Write the plan

Produce this, short enough to paste into the PRD's evaluation section:

```markdown
## Eval plan: <feature>

**Worst error:** <one sentence>. Costs lean toward <precision / recall / refusing when unsure>.

**Behaviors under test**
- Must: ...
- Must not / must fall through: ...

**Test set:** <N> examples from <source>, labeled by <who> (<agreement rate if 2 labelers>).
Mix: <x>% common case · <y>% deliberate negatives · <z>% known hard cases

**Launch gates (set <date>, before any results)**
| Behavior | Metric | Gate | Why |
|---|---|---|---|

**Guardrail:** <metric that must not get worse>
**Cheapest baseline to run first:** <approach>
**After launch:** <online metric>, <sampling cadence>, roll back if <trigger>
**If it fails the gate:** <what happens: iterate, narrow scope, or don't ship>
```

When results come back, report them against the gates exactly as set. A failed gate is the eval doing its job; publish it rather than moving the bar.

## Worked example

From a [practice project](https://github.com/vishalhabib99/ai-pm-portfolio/tree/main/prototypes/ticket-triage-rag) (a sample PRD and prototype, not a shipped product): a support-ticket triage assistant that classifies tickets and drafts replies.

- **Worst error:** a confident, wrong draft reply. So the gate was **≥95% precision on high-confidence predictions**, alongside ≥90% overall accuracy, set in the PRD before any code.
- **Deliberate negatives:** 2 of the 10 test tickets ("company history", "student discounts") matched no category and should have fallen through to a human.
- **Cheapest baseline first:** plain TF-IDF retrieval, no LLM.
- **Result:** 60% accuracy and 60% high-confidence precision. **It failed the gate.** Both off-topic tickets were matched to `billing` with enough confidence to generate a wrong draft, because similarity search always returns *something* and has no concept of "none of these fit".
- **What the eval bought:** the first 3 sample tickets all looked fine by eye. Only the deliberate negatives exposed the failure, before anything shipped. The result was published as-is, with two concrete next steps (an LLM classifier and an explicit "none of the above" option).

## Things to avoid

- A test set of only the cases the feature is supposed to handle.
- Picking the threshold after seeing the result.
- One headline accuracy number that hides the costly error.
- An LLM judge no one has checked against human ratings.
- Treating a failed gate as a reason to change the gate.
