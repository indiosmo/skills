# The Design Interview

Discovery fills the brief with open items: terms that are not yet defined, questions whose answer would change the design, and decision points without decisions. The interview is how those items get closed. It runs after the brief is first written and surfaced in chat, and it continues until the brief has no open items left.

The technique is a relentless but structured design review: walk every branch of the design tree until each leaf is resolved, explicitly declared out of scope, or moved to a separate follow-up brief. Nothing stays vague by default.

## How to run it

### One question at a time

Ask a single question. Wait for the answer. Fold the answer into the brief -- define the term, promote the open question, record the decision -- then ask the next question. A message with ten questions in it gets one skimmed answer that addresses two of them; a message with one question gets a real answer to that one.

### Recommend an answer with every question

The interview is not a blank survey handed to the user. For each question, state the answer you would give and the reason, then ask the user to confirm, correct, or override. You have read the code; the user has the intent and the constraints that live outside it. A recommendation the user rejects is still progress -- the rejection surfaces the constraint you were missing.

Good: "I would put the OAuth callback in a new `oauth/` module rather than extending `web/auth/`, because the callback's lifecycle (token exchange, refresh) is distinct from session handling and `web/auth/` is already 600 lines. Does that fit how you think about the boundary, or is there a reason to keep auth in one place?"

Weak: "Where should the OAuth callback live?"

### Explore the codebase instead of asking, when the codebase can answer

A question the code settles is a question you answer yourself, not one you put to the user. "Does the rate limiter already scope per-tenant?" is answered by reading the rate limiter. Reserve the user's attention for what the code cannot tell you:

- **Intent** -- what outcome they actually want, which the code does not record.
- **Priorities** -- which of two correct designs matters more here (speed to ship vs. future flexibility).
- **Constraints outside the repo** -- a partner API contract, a compliance rule, a deadline, a team convention.

When you do reach into the code mid-interview, say so briefly ("checking whether the session store already persists across restarts -- it does, `session.ts:88`") so the user sees the question was answered, not dropped.

### Walk dependencies in order

Decisions are coupled. Where the OAuth callback lives depends on whether `oauth/` exists as a module; whether to add a feature flag depends on how tight the migration window is. Resolve the upstream decision first -- the downstream one often dissolves, reshapes, or splits once the upstream is settled. Asking them out of order forces the user to answer the same uncertainty twice.

### Stress-test fuzzy terms and boundaries with concrete scenarios

When a domain relationship or a term's boundary is unclear, do not ask the user to define it in the abstract. Invent a specific scenario that forces the boundary to show itself:

- "A customer cancels after the carrier scans the parcel but before it leaves the depot -- is that a cancellation or a return?" forces a precise line between two terms.
- "Two tenants share an email; one signs in with Google, the other with GitHub -- do they get one account or two?" forces the identity model to be explicit.

The edge case is where the vague term breaks, and breaking it on a scenario is faster than arguing about the definition.

### Challenge usage against the glossary

When the user uses a term in a way that conflicts with its `GLOSSARY.md` definition, call it out the moment it happens rather than quietly adopting their reading. "The glossary defines a session as a server-side auth record, but you just used it for the provider's token grant -- those are two concepts. Which one do you mean here, and do we need a second word for the other?" The glossary is the arbiter; a conflict is a fork the user has to resolve, not one the brief should paper over.

## Every item lands in one of three states

An item is not resolved until it reaches one of these. "We'll figure that out later" without one of the three is not a resolution -- it is the item still being open, wearing a different label.

1. **Resolved.** The answer is now recorded in its durable home: a definition in the Terminology block (and `GLOSSARY.md` if it is domain vocabulary), an entry in Assumptions, a Decision block, a decision matrix, or an ADR. The open item is removed from the brief's open lists.
2. **Explicitly out of scope.** The user rules it out for this change. Record it as out of scope -- a one-line note in Assumptions or the relevant section -- so a later reader knows it was considered and deliberately excluded, not forgotten. An excluded option is information; a silently-dropped one is a gap.
3. **Deferred to a follow-up brief.** The item is real but belongs to a later change. Create or name a linked follow-up brief and move the item there, so the thread is not lost. Do not let a deferred item sit unresolved in the current brief's open lists -- move it out, leave a link.

## Where resolutions go

As each item closes, write it to every place it belongs. The brief is the working surface; the durable artifacts outlive it.

| Resolution | Durable home |
|---|---|
| A defined domain term | `GLOSSARY.md` (via the [glossary](../../glossary/SKILL.md) skill's entry schema), referenced from the brief's Terminology block |
| A change-local clarification | the brief's Terminology block only |
| An answered open question | the brief's Assumptions block |
| An obvious call | a one-line Decision inside the decision-point block |
| A non-obvious trade-off | an embedded [decision matrix](../../decision-matrix/SKILL.md) with its Decision block |
| A hard-to-reverse, surprising, real-trade-off call | an ADR under `docs/adr/` (via the [documentation](../../documentation/SKILL.md) skill), with the decision matrix as its front matter, referenced from the brief |
| An excluded option | an out-of-scope note in the brief |
| A real but later concern | a linked follow-up brief |

After writing a resolution, re-read the rest of the brief against it. A resolved term may make a requirement that used the old reading wrong; a resolved decision may close one open question and open another. Fix the drift in the same pass -- the brief stays internally consistent at every step, not only at the end.

## When the interview is done

The brief is settled when:

- every Terminology entry carries a definition (none flagged unresolved);
- the Open Questions list is empty (each promoted to Assumptions, ruled out of scope, or deferred);
- every decision point carries a Decision block, at the right weight of record.

At that point the design is clear enough that the implementation plan is rote. The user can ask for the plan, and Claude reads the brief -- plus the glossary entries and ADRs it produced -- the same way it reads any other input.
