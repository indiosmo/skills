# Logistics: carry the boundary through a collection name

A sales application calls a seller-to-buyer grouping a shipment. A transport
application records consignments organized by transport contract. An integration
developer wants to name the lookup joining these two applications and proposes
`shipment_by_identifier`. The consumer starts with a sales shipment identifier
and needs every transport consignment allocated to it.

This is an original mapping scenario. Its local glossary deliberately follows
the trade/transport distinction in the inspected UN/CEFACT Web Vocabulary's
Shipment and Consignment entries. That source is an unversioned project test
site; terminology must retain that scope. See the
[source and access limitations](../references/sources.md#con-uncefact-vocabulary)
and [bounded-context guidance](../references/domain-vocabulary.md).

## Resolve the grouping and cardinality

The useful question is: "Can a shipment travel under more than one transport
contract, and what does the consumer need before allocation?" In this stipulated
integration, a shipment can have zero or more allocated consignments. Every
shipment identifier in the current sales batch has an entry, including an empty
collection before allocation. An identifier outside the batch is a lookup error.
The transport service owns the consignment identifiers.

For shipment `shipment-42`, two separate transport contracts yield
`consignment-a` and `consignment-b`. The mapping exposes both records. This
scenario's one-to-many rule comes from its integration contract; the UN/CEFACT
terminology alone cannot establish the cardinality of a particular application.

Illustrative schema and use-site pseudocode:

```text
consignments_by_shipment_identifier:
    Map<ShipmentIdentifier, List<Consignment>>

for consignment in consignments_by_shipment_identifier[shipment.identifier]:
    show_transport_contract(consignment.transport_contract_identifier)
```

The key crosses the sales boundary; each value belongs to transport. The plural
`consignments` communicates the value collection. `shipment_identifier` supplies
the key's meaning even in integration code containing both identifier types.

## Decide from the supplied lookup contract

| Candidate | Reader's likely interpretation | Decision |
| --- | --- | --- |
| `consignments_by_shipment_identifier` | Shipment identifier selects a collection of consignments | Recommend |
| `consignment_by_shipment_identifier` | Shipment identifier selects one consignment | Fails the split-shipment scenario |
| `shipments_by_identifier` | Identifier selects shipments | Misidentifies the transport values |
| `bookings_by_shipment_identifier` | Shipment identifier selects transport reservations | Requires records representing bookings |

The complete mapping name is the clear winner for a local variable read outside
either application's namespace. The singular and plural forms make different
cardinality claims. Booking is a neighboring concept in the same source, but
the supplied values represent consignments. Choosing it would change the
representation being described.

The length earns its place by preserving two bounded-context terms and the key
type. If the actual lookup lived behind a dedicated interface with a typed
`for_shipment` operation, that surrounding context could carry some of these
words. Such an interface is a design choice to assess with its consumers, rather
than an assumed condition of this example.

## Review the recommendation separately

The review reads the mapping in both directions: what does the key identify,
and what does iterating its value yield? It then checks boundary cases:

| Lookup input | Stipulated value | Naming evidence |
| --- | --- | --- |
| Known shipment awaiting allocation | Empty list | A collection can express zero allocations |
| Known shipment with one allocation | List containing one consignment | The plural remains accurate for a collection of one |
| `shipment-42` with split allocation | List containing `consignment-a` and `consignment-b` | One sales grouping can expose both transport records |
| Identifier outside the sales batch | Lookup error | Key membership has an explicit boundary |

Outcome: recommend `consignments_by_shipment_identifier`. Static review confirms
its key, value concept, and cardinality against the scenario and cited scoped
vocabulary. The pseudocode has not been executed. Production confirmation needs
the actual join, split-allocation examples, empty-collection behavior, unknown-key
handling, and both applications' glossaries. Consolidation across shipments would
add relationship evidence to inspect. Human acceptance remains pending.
