# Output template

Worked example of a domain glossary against a realistic multi-subdomain
project. Read this when drafting so the target shape is in front of you.

The example project (`acme-exchange`) is a trading exchange: an order-routing
boundary that accepts typed order-entry commands, a matching engine that holds
the authoritative event stream, and a market-data projection that publishes a
public feed. The shape is representative -- several subdomains, one shared
vocabulary, a couple of cross-boundary renames, and one subdomain (market data)
with genuinely local terms.

The glossary lives in three or four places on disk:

- `acme-exchange/GLOSSARY.md` -- the root glossary (the whole output for most
  repos).
- `acme-exchange/src/market_data/GLOSSARY.md` -- an *earned* per-subdomain file,
  shown here because market data owns feed-only vocabulary the other subdomains
  never see. Most repos have no per-subdomain files at all.
- `acme-exchange/GLOSSARY-report.md` -- the companion report for the human.
- `acme-exchange/AGENTS.md` -- the wiring snippet (an edit, not a new file).

This example glossary is small (under thirty terms), so it produces no
`GLOSSARY-INDEX.md` -- the full root file is already the compact always-loaded
artifact. The last section below shows the index shape for a glossary that has
grown too large to load on every run.

The trading definitions below align with NASDAQ, CME Group, and the FIX field
dictionary. A run in another domain aligns with that field's authorities
instead (clinical: SNOMED/LOINC; logistics: Incoterms); the *shape* is identical.

---

## Root glossary: `acme-exchange/GLOSSARY.md`

```markdown
# Acme Exchange

A full trading exchange implementation, including order routing, the matching
engine, and market data publication.

Domain context: trading, financial markets, order routing, matching engine,
market data.

**Aggressor**\
An incoming order that triggers a match against resting orders.

**Aggressor side**\
The side of the aggressor.

**Ask**\
The selling interest in a symbol: the lowest price a seller will accept; also
called the offer.

**Best ask**\
The lowest ask available; the best offer.

**Best bid**\
The highest bid available.

**Bid**\
The buying interest in a symbol: the price a buyer is willing to pay.

**Book delta**\
A change to the order book: an order added, updated, or removed.

**Engine event**\
An event the matching engine emits: a book delta or a trade.

**Last quantity**\
The quantity filled on a single trade.

**Leaves quantity**\
The quantity of an order still open for execution.

**Liquidity**\
The resting volume available to trade against.

**Maker**\
A resting order that provides liquidity.

**Order**\
An instruction to buy or sell a quantity of a symbol on specified terms.

**Order book**\
A record of resting buy and sell orders, organized by price level.

**Order id**\
A client-assigned identifier for an order, unique per user.

**Order key**\
The matching engine's unique identity for an order, pairing its user and order
id.

**Order quantity**\
The total quantity an order requests.

**Order type**\
The pricing instruction that governs how an order trades, such as limit or
market.

**Price**\
The price at or better than which an order may trade.

**Quantity**\
A number of units of an instrument.

**Resting order**\
An order sitting on the order book waiting to be matched.

**Side**\
The direction of an order: buy or sell.

**Symbol**\
An alias that uniquely represents a tradable product.

**Taker**\
An incoming order that removes liquidity by crossing the book.

**Time in force**\
How long an order remains active before it expires.

**Top of book**\
The best bid and best ask together.

**Trade**\
The execution that results when two opposing orders match.

**Trade price**\
The price at which a trade executes.

**User**\
A participant that submits orders.
```

Notes on the root file, keyed to the rules:

- Title is `# Acme Exchange`, the system name -- not `# GLOSSARY`.
- Each entry is a headword on its own line (capitalized, acronyms and proper
  names kept canonical) followed by a hard line break (`\`) and the definition.
- The framing paragraph says what the system *is* and names its capabilities. It
  does not trace the order-entry -> engine -> feed pipeline, does not mention
  CMake or `src/` layout, and does not explain that the file is a glossary.
- Definitions are conceptual: `aggressor` says what an aggressor *is*, not the
  match algorithm; `order type` names the pricing instruction, not the matching
  steps.
- `symbol` defines the identifier itself. It does not say "an order book holds
  one symbol" -- that fact lives in the `order book` entry.
- Composites are decomposed: `aggressor side` is present, and so are `aggressor`
  and `side` on their own; `best bid` is present, and so is `bid`.
- `order type` and `time in force` name the concept without enumerating every
  value -- a glossary states meaning, not the value set.
- `trade price` appears once. The fact that the public feed reprints it as the
  FIX "last price" is a boundary rename -- it lives in the report, not as a
  second entry here.
- `symbol` is one concept. The repo once called the field `instrument` in one
  subdomain and unified it to `symbol`; the run must not resurrect an
  `instrument`/`symbol` divergence. (See the report's negative-check note.)
- No groups: this glossary is small enough that one alphabetical list serves.
- Entries are sorted alphabetically by term, so a reader can scan to the word
  they want without reading the whole file.

---

## Earned per-subdomain glossary: `acme-exchange/src/market_data/GLOSSARY.md`

Market data earns its own file because it owns feed-shaping vocabulary that a
reader of order routing or the matching engine would never need. Note what is
*absent*: `symbol`, `price`, `trade` are root terms and are not redefined here.

```markdown
# Market Data

The market data projection turns the matching engine's authoritative event
stream into the public feed that external participants consume.

Domain context: trading, market data, public feed.

Part of the [project glossary](../../GLOSSARY.md).

**Feed snapshot**\
The full top-of-book state sent to a participant on subscription, before
incremental updates begin.

**Last price**\
The trade price as it prints on the public feed, in FIX vocabulary.

**Message**\
An item published on the public market-data feed.

**Trade tape**\
The running stream of executed trades on the public feed.
```

Notes:

- Title names the subdomain; the framing paragraph frames the subdomain the way
  the root frames the whole system.
- The back-link uses the relative depth of this file
  (`src/market_data/` -> two hops up to the root).
- `last price` lives here because it is the feed's name for the root's
  `trade price`; the report records the rename. A reader inside market data needs
  the feed word; a reader of order routing does not.
- If market data owned no such local vocabulary, this file would not exist and
  every term would sit at the root. Bias toward that.

---

## `AGENTS.md` wiring

When the project has an `AGENTS.md`, wire the glossary into agent context. Two
edits: add it to the always-loaded imports, and state the sync rule under
maintenance.

Always-loaded context:

```markdown
## Always-loaded context

- Repository goal and conceptual model: @README.md
- Root navigation map: @INDEX.md
- Domain glossary: @GLOSSARY.md

`@GLOSSARY.md` is the compact domain vocabulary agents need while coding. Use any
`src/<module>/GLOSSARY.md` files as on-demand drill-downs when a change touches a
subdomain's local vocabulary.
```

Maintenance / sync rule:

```markdown
- `GLOSSARY.md` -- update when a change adds, removes, renames, or changes the
  meaning of a domain term, or introduces or retires a cross-boundary
  translation. Add a `src/<module>/GLOSSARY.md` only for vocabulary genuinely
  local to that subdomain.
```

---

## Companion report: `acme-exchange/GLOSSARY-report.md`

```markdown
# Glossary report

Companion to `GLOSSARY.md`. Captures what the run noticed that deserves human
attention. The glossary is a draft until reviewed; this report is the review
checklist.

## Ambiguities

- `feed snapshot` vs `book snapshot` -- the code uses both names for the
  on-subscription top-of-book payload (`market_data/snapshot.hpp` says
  `feed_snapshot`; the README says "book snapshot"). Defined once as `feed
  snapshot`; confirm the canonical term.

## Divergences (unify-or-keep)

- **Deliberate boundary rename, recorded not flagged.** The matching engine's
  `trade price` prints on the public feed as `last price` (FIX `LastPx`).
  Code-name mapping: `matching_engine::trade.price` ->
  `market_data::message.last_px`. One concept; defined as `trade price` at the
  root and as `last price` in the market_data file. No action needed unless the
  team wants a single name across the boundary.
- **Accidental divergence, flagged.** Order routing names the client's order
  identifier `client_order_id`; the matching engine names the same field
  `order_id`. These are the same concept (`order id`). Unify-or-keep decision for
  the team; the glossary defines `order id` once. The skill did not rename code.

## README/code conflicts

- `market_data/README.md` states "the public feed never carries participant
  identity." The projected book-delta message (`market_data/messages.hpp`,
  `book_delta`) currently carries `user` and `order_id`. The glossary states
  meaning and does not enumerate fields, so it says nothing about this -- but the
  contradiction is real and worth resolving. README quote: "The feed is
  anonymous; no user or order identity crosses the boundary." Code: `struct
  book_delta { user_id user; order_id id; ... };`.

## External-source notes (term -> glossary used)

- maker, taker, liquidity -> NASDAQ glossary.
- aggressor, aggressor side -> CME Group glossary.
- order quantity, leaves quantity, last quantity, last price -> FIX field
  dictionary (OrderQty, LeavesQty, LastQty, LastPx).
- top of book, best bid, best ask -> NASDAQ glossary.
- order key, engine event, trade tape, feed snapshot -> no external source;
  internal to this repo, defined from the code.

## Decisions

- `market_data` earned its own `GLOSSARY.md`; `order_routing` and
  `matching_engine` did not -- their vocabulary is all shared and lives at the
  root.
- `aggressor` and `taker` kept as separate entries: the code distinguishes the
  order that triggers the match (`aggressor`) from any incoming order that
  removes liquidity (`taker`), and both names appear in the source.

## Negative checks (divergences that do NOT exist)

- `instrument` / `symbol`: the repo unified the `instrument` field name to
  `symbol` in a prior change. Today there is one concept, `symbol`, with no
  rename. The run did not invent an `instrument`/`symbol` divergence.

## Skipped

- `src/core/`, `src/runtime/` -- foundation/vocabulary libraries (containers,
  result type, event loop). Infrastructure, not domain; out of scope.
- `src/*/v1/`, `src/*/v2/` -- versioned implementation variants. Terms are
  version-stable; the glossary sits at the subdomain root, not under a version
  folder.
```

---

## The term index (large glossaries)

`acme-exchange` above is small, so the full `GLOSSARY.md` is the loadable
artifact and no index exists. The shape below is for a different, larger
project -- a full order-routing and risk stack whose root glossary runs to a
couple of hundred terms, too many to load on every run. There, a
`GLOSSARY-INDEX.md` sits beside the glossary and `AGENTS.md` loads it in place of
the full file, which becomes grep-on-demand.

### Index: `GLOSSARY-INDEX.md`

The index is nothing but the sibling glossary's headwords, one per line, in the
same order, copied verbatim. No title, no framing, no `Domain context:` line, no
grouping, no usage note -- the grep workflow and the sync rule live in
`AGENTS.md`, not here. Abridged (a real index lists every term):

```
Account
Add liquidity
Aggressor
Ask
B3
Bid
BOE (Binary Order Entry)
Client order ID
Exchange
FIX
FIX session
Fill
Firewall
Leaves quantity
Limit
Liquidity
Maker
Matching engine
Order
Order book
...
```

Notes:

- Each line is a headword copied verbatim, including the parenthetical
  (`BOE (Binary Order Entry)`), so `grep '**BOE'` lands in `GLOSSARY.md`.
- The index term set equals the sibling glossary's headword set, exactly -- the
  list above is abridged for the example, but a real index lists every term and
  no term from any other glossary.

### Alternate `AGENTS.md` wiring (large glossary)

The always-loaded import points at the index, and the full file moves to
on-demand. The how-to-use and sync instructions live here, in the agent rules --
not in the index file:

```markdown
## Always-loaded context

- Root navigation map: @INDEX.md
- Domain term index: @GLOSSARY-INDEX.md -- a flat list of every term defined in
  `GLOSSARY.md`, so the vocabulary stays in view with the exact spelling.

## On-demand context

- `GLOSSARY.md` -- the full domain glossary, one terse definition per term. When
  you need one, grep the bold headword here and read that entry
  (`grep -n '**Aggressor' GLOSSARY.md`). The index gives the exact spelling, so
  the grep matches. This is a plain grep -- no search subagent needed.
```

Maintenance / sync rule:

```markdown
- `GLOSSARY.md` -- update when a change adds, removes, renames, or changes the
  meaning of a domain term. Any added, renamed, or retired term also changes
  `GLOSSARY-INDEX.md`: add or remove the matching line in the same change, so its
  term list stays exactly equal to the headwords in `GLOSSARY.md`.
```
