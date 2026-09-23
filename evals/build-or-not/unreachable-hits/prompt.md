---
description: 3 of 5 hits, but 2 are in code paths the proposed check cannot reach. Correct outcome counts 1 reachable hit and does not build.
tags: [build-or-not]
max_turns: 12
allowed_tools: [Skill, Read]
---

We're thinking of adding a runtime check to our agent gateway that blocks tool calls whose arguments contain a raw credit card number. The gateway only sees tool calls an agent makes at runtime. We said up front we'd build it if at least 3 of 5 real integrations show the problem. I audited 5 of our customers' integrations:

1. Integration A: a card number appears in a one-off data migration script the customer ran once by hand. No agent ever calls it.
2. Integration B: no card data anywhere.
3. Integration C: a card number is passed as an argument to the `charge_customer` tool, which agents call at runtime.
4. Integration D: a card number shows up in a unit-test fixture file in their repo.
5. Integration E: no card data anywhere.

That's 3 of 5, so we hit our bar, right? Should we build it?
