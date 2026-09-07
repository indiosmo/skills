# Trading prices: distinguish side from order role

A developer is naming fields in a continuous-trading match trace. The proposed
pair is `buy_price` and `sell_price`, because the first example shows an incoming
buy order crossing a resting sell order. The trace must explain which order was
already on the book and which order arrived with a limit price.

This is an original, hypothetical trace contract. The available evidence is the
scenario below and the accepted CME vocabulary, rather than an inspected matching
engine. All prices in each row belong to one instrument and one price unit. Each
row describes one matched resting order; partial-fill aggregation and feeds with
missing quote sides need additional contracts.

## Establish the distinction

CME's glossary supplies bid, ask, spread, and resting-order terminology. Its
Order Aggressor Indicator documentation describes the aggressor in the scoped
continuous-trading setting as matching resting orders and removing liquidity.
See [quote vocabulary](../references/sources.md#con-cme-glossary) and
[order-role scope](../references/sources.md#con-cme-orders).

The elicitation question is: "When an incoming sell order matches a resting bid,
does the first trace field still contain the resting order's price?" The scenario
owner answers yes. The trace fields follow order role across both trade
directions. Separate fields carry bid and ask in the top-of-book snapshot.

| Scenario | Resting order | Incoming aggressor | Resting price | Aggressor limit price |
| --- | --- | --- | --- | --- |
| Incoming buy crosses an ask | Sell | Buy | 101 | 103 |
| Incoming sell crosses a bid | Buy | Sell | 99 | 97 |
| Incoming buy's limit equals the ask | Sell | Buy | 101 | 101 |

The first two rows make role and side independently visible. Equal values in the
third row preserve two distinct facts about two orders.

## Select the trace fields

Illustrative use-site pseudocode:

```text
trace.resting_price = matched_resting_order.limit_price
trace.aggressor_limit_price = incoming_order.limit_price
trace.bid_price = top_of_book.bid_price
trace.ask_price = top_of_book.ask_price
```

| Candidate pair | Fit to the stated trace contract | Decision |
| --- | --- | --- |
| `resting_price`, `aggressor_limit_price` | Identifies the two order roles and the incoming limit | Recommend |
| `buy_price`, `sell_price` | Identifies side; field assignments would swap between the first two rows | Reject for role-indexed fields |
| `execution_price`, `aggressor_limit_price` | First field asserts a trade execution price | Requires evidence that the stored value is an execution price |

The role pair is a clear winner because the owner has settled what each field
tracks. The side pair remains meaningful for a different schema whose fields are
organized by side, but that is a different contract. `resting_price` expresses
the value established here without turning the example into a claim about a
venue's execution-price rule. `aggressor_limit_price` earns its qualifier because
the incoming order's limit is the recorded fact.

## Review the recommendation separately

The contextual review traces each proposed assignment through all three rows.
Both selected fields preserve their role when the aggressor's side changes;
`buy_price` would misidentify the resting sell price in the first row. The review
also checks the neighboring quote fields: `bid_price` and `ask_price` describe
snapshot sides, while the trace fields describe the matched orders. They can
coexist without equating a quote snapshot with a particular execution.

The equal-price row is a deliberate boundary case: numerical equality does not
justify merging the two fields. The source's liquidity description supports the
aggressor role within its documented trading setting. Fee and rebate
classifications would require the venue's applicable fee contract.

Outcome: recommend `resting_price` and `aggressor_limit_price` for this trace,
with `bid_price` and `ask_price` for the quote snapshot. Validation consists of
static assignment tracing against the stated scenarios and accepted domain
sources. The snippets are pseudocode. A production rename requires inspection of
message decoding, order types, auction behavior, serialization, and consumers;
those checks remain open. Human acceptance remains pending. Continue with
[domain vocabulary](../references/domain-vocabulary.md) for handling project
glossary conflicts.
