# Naming variables and state

A value name should tell a reader which fact the value represents at its use
site. Start with the declaration, assignments, and readers. Together they establish
the value's role, lifetime, cardinality, and units. The review procedure below is
local engineering policy; linked claims distinguish source-backed conventions
from the original examples.

## Fit the available context

A local variable can draw context from a short expression or enclosing operation.
A field travels with its receiver; a parameter also appears in declarations,
keyword calls, and generated documentation. Choose enough detail for those readers.
Google's C++ guidance relates detail to scope, and Swift's guidance names values
by role and evaluates use sites. These are practitioner conventions with explicit
ecosystem scope ([LANG-01](evidence.md#lang-01),
[LANG-02](evidence.md#lang-02)).

For example, this original illustrative pseudocode computes a price difference
for one instrument, with both prices available in the same currency and price
unit:

```text
bid = top_of_book.bid
ask = top_of_book.ask
spread = ask - bid
```

`bid`, `ask` and `spread` express the roles supported by the
[CME vocabulary](sources.md#con-cme-glossary). Adding `active` would require an
actual state distinction. Where execution logic also contains an incoming limit
and a matched resting order, `aggressor_limit_price` and `resting_price` preserve
the roles even if their numeric values happen to match
([CON-009](evidence.md#con-009)).

Types carry useful context: `shipment: Shipment` can be clear, while
`shipment_string` says little about a string's purpose. A string storing a lookup
key can be `shipment_identifier`; a displayed value can be `shipment_label`.
Keep type decoration conditional on the project convention. See
[language conventions](language-conventions.md) for spelling and framework rules.

Default to full words. Keep established domain abbreviations when the intended
readers recognize them and their scope supports them
([LOCAL-002](evidence.md#local-002)). The
[empirical research](empirical-research.md#full-words-and-familiar-abbreviations)
distinguishes generated abbreviations from familiar ones; it supplies bounded
comprehension findings rather than a universal maximum name length.

## Review related variables as a family

Describe each value's role and its relationship to the others before choosing
spellings. Trace assignments, comparisons, and derived expressions together.
Capacity, occupancy, free space, and a startup threshold can share a numeric type
while answering different questions. A read index describes a position; its
relationship to those quantities comes from the state transitions.

Review the family at three useful contexts: local expressions inside the
component, member access through its containing class, and properties exposed
by that class to callers. The containing receiver can supply context that an
external property needs to spell out. For a stipulated audio buffer,
`self.frame_count`, `self.buffer.frame_count`, and `player.buffered_frames`
can express the same occupancy at those boundaries. An exposed property may
derive a different quantity; name `capacity - occupancy` for free space and
preserve its units when tracing callers.

With a sparse description such as "size, level, and target control buffering,"
keep their possible roles open. Ask for a small scenario: when buffering reaches
the target, does playback begin, do writes stop, or does some other action occur?
The answer distinguishes a startup threshold from a capacity or control target.
Use the actual reader and transition to resolve the next material ambiguity.
Record conditional interpretations using [elicitation](elicitation.md), then
compare coherent naming families for the established relationships. Retain
members whose meaning is already clear in their receiver context.

## Cardinality, optional values and keys

Use the actual representation and the question the reader asks. These original
examples state their contracts; the recommendations apply when those contracts
hold.

| Representation and role | Candidate | What to check |
| --- | --- | --- |
| One shipment record | `shipment` | Accesses use record fields |
| Identifier used to retrieve one shipment | `shipment_identifier` | Lookup key domain matches the indexed records |
| Sequence of shipment records | `shipments` | Iteration yields records; ordering and duplicates follow the contract |
| Integer counting records in that sequence | `shipment_count` | Count is measured at the same point as the sequence |
| Mapping from shipment identifier to a sequence of consignments | `consignments_by_shipment_identifier` | Values can contain several consignments |
| Optional bid price for the instrument | `bid` with an optional price type | Absence means that side is unavailable in the supplied snapshot |

The shipment/consignment distinction follows the scoped
[UN/CEFACT vocabulary](sources.md#con-uncefact-vocabulary); the mapping cardinality
is an example assumption, verified from the modeled mapping when applied.
Plural fields and scalar counts also have explicit Google API conventions
([LANG-09](evidence.md#lang-09), [LANG-10](evidence.md#lang-10)). A count is a
number of items, a capacity is a limit, and an index is a position: use the term
matching the arithmetic and bounds.

An optional type can carry absence without adding `maybe` to every name. Establish
what absence means: unknown, unavailable, unassigned or failed lookup can require
different handling. If several conditions share one empty representation, naming
can expose the ambiguity for a separate modeling decision. For an untyped or
serialized value, document the presence/default contract and inspect readers.
Keep `sorted`, `unique`, `pending` and similar modifiers tied to established
ordering, duplicate handling, or state predicates. A container type can establish
uniqueness under its equality relation; iteration order still needs its own
contract.

## Units, instants, dates and durations

Choose the quantity before choosing a suffix. For raw numeric values, including a
unit can prevent ambiguity at arithmetic and API boundaries. A quantity type or
unit-bearing configuration value can already convey it. AIP-141's suffix rules
are scoped to its API ecosystem ([LANG-10](evidence.md#lang-10)); general use here
is local judgment about information available to the reader.

In this original audio example, one frame contains one sample per channel. A
buffer has 480 frames, the stream has two channels, and `sample_rate` is 48,000
frames per second. These quantities follow
[PortAudio's documented distinctions](sources.md#con-portaudio).

```text
buffer_size_frames = 480
channel_count = 2
sample_rate = 48000
buffer_duration_seconds = buffer_size_frames / sample_rate
sample_count = buffer_size_frames * channel_count
```

The computed duration is 0.010 seconds and the scalar sample count is 960.
`buffer_size_samples` would misdescribe the value 480 in this scenario.
`buffer_duration_seconds` describes the buffer's time span; a latency name needs
measurement endpoints such as capture-to-playback plus evidence of what is
measured. Verify dimensions, integer versus fractional arithmetic, and conversion
boundaries independently of spelling ([CON-011](evidence.md#con-011)). This is
illustrative pseudocode with fractional division.

For time fields, state the represented fact and temporal type. A field
`received_at: Instant` can represent a recorded receipt instant;
`collection_date: Date` can represent a calendar date; `retry_delay: Duration`
can represent an interval. These are original type sketches, with types defined
by the receiving project. Raw representations may need names such as
`retry_delay_milliseconds` or `received_at_unix_seconds` when those encodings are
verified. Inspect time zone, epoch, precision, and clock source where they affect
meaning. A deadline, elapsed duration, and observation time answer different
questions even if their storage types coincide.

## Boolean meaning and polarity

First describe the condition represented by true. Separate a configured policy,
permission, current capability, observed state, and a decision derived from them.
Then read the predicate in branches and at call sites. Prefix and polarity rules
vary: Swift favors assertion grammar; AIP-140 omits `is` on boolean fields and
allows `disabled` ([LANG-02](evidence.md#lang-02),
[LANG-09](evidence.md#lang-09)). Neither establishes a universal positive-name rule.

This original example defines `retry_disabled` as a policy setting and
`connection_available` as current state. Its decision is explicitly:

```text
should_retry = not retry_disabled and connection_available
```

| retry_disabled | connection_available | should_retry |
| --- | --- | --- |
| false | false | false |
| false | true | true |
| true | false | false |
| true | true | false |

Renaming `retry_disabled` to `retry_enabled` while preserving its stored values
would invert the reader's interpretation. An explicit inverted representation
requires transforming producers, consumers and defaults; classify that work
separately from a spelling-only rename. Naming this policy `can_retry` would also
suggest capability beyond the policy fact. Retaining `retry_disabled` is a clear
choice under this contract, verified against all four rows. The example's policy
is deliberately small; real decisions need their actual inputs and truth table.
See [LOCAL-006](evidence.md#local-006) and
[renaming](renaming.md) for preservation checks.

State enums can express several mutually exclusive lifecycle states directly.
Several booleans may instead express independent facts. Inspect legal combinations
before recommending either representation. A naming review can describe an
inconsistent state model; changing that model is a separate design decision.

## Review a proposed value name

1. Trace assignments and reads; state the represented fact and valid values.
2. Check type, absence, cardinality, key domain, units, and time boundary.
3. Compare neighboring names and read representative expressions or keyword calls.
4. Verify every modifier against the producing behavior. For a predicate, check
   the true proposition, false proposition and relevant truth-table rows.
5. Record the recommendation and a separate verification result naming the code,
   contract or description examined. Keep implementation checks pending when only
   a description is available.

Continue with [functions and methods](functions-and-methods.md) for operation and
parameter roles, [types and messages](types-and-messages.md) for modeled state,
and [contextual validation](contextual-validation.md) for independent review.
