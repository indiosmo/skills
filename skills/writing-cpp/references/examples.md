# C++ Agent Examples

Good/bad code pairs that illustrate the rules in
[`../SKILL.md`](../SKILL.md). Section titles match the rule sections in
the skill body. Load this file on demand when
the rule alone is not enough to shape an edit. Examples use `lib::`
placeholders -- substitute the local project vocabulary.

Each rule leads with the good form: the complete, imitable shape you
should pattern-match. A `Bad:` block appears only where the
anti-pattern is not self-evident from the good form, is reduced to the
fragment that carries the tell, and is followed immediately by the
corrected good form so the rule ends on what to write.

## Tests

The expected value states the intended behavior independently. Derive
it from the domain, not from the implementation under test.

Good:

```cpp
TEST_CASE("rectangle - area", "[geometry]")
{
  const auto r = rectangle{.width = 6, .height = 4};
  CHECK(r.area() == 24);
}
```

## Debugging

Drive the loop from evidence: observe, trace, hypothesize, run one
focused experiment, write the failing regression test, fix the root
cause, then run the relevant test and suite.

Good:

```text
observe the symptom -> trace the source -> state one hypothesis
-> run one focused experiment -> write the failing regression test
-> fix the root cause -> run the relevant test and suite
```

## Domain Ownership

Define domain types inside a nested `types` namespace, keep the
`types::` qualifier even inside the domain, and give each field a
strong type rather than a raw primitive.

Good:

```cpp
namespace order_routing::types {

using user_id = lib::strong_type<std::uint64_t, struct UserIdTag>;
using user_order_id = lib::strong_type<std::uint64_t, struct UserOrderIdTag>;
using symbol = lib::strong_type<lib::fixed_string<8>, struct SymbolTag>;
using quantity = lib::strong_type<std::uint64_t, struct QuantityTag>;

enum class side : std::uint8_t { buy, sell };

} // namespace order_routing::types

namespace order_routing {

struct new_order {
  types::user_id user;
  types::user_order_id order_id;
  types::symbol instrument;
  types::side order_side;
  types::quantity order_quantity;
};

} // namespace order_routing
```

Keep the `types::` qualifier; a `using` that pulls a nested domain type
up into the domain namespace erases the ownership the qualifier makes
visible.

Bad:

```cpp
using types::quantity;
```

Good:

```cpp
types::quantity order_quantity;
```

Two domains owning the same safe representation construct across the
boundary directly; no conversion helper earns its name for a mapping
that adds no domain knowledge.

Good:

```cpp
namespace routing::types {
using order_id = lib::strong_type<lib::fixed_string<36>, struct OrderIdTag>;
}

namespace risk::types {
using order_id = lib::strong_type<lib::fixed_string<36>, struct OrderIdTag>;
}

void submit_to_risk(routing::types::order_id routing_id)
{
  auto risk_id = risk::types::order_id{routing_id};
  risk_engine.submit(risk_id);
}
```

A conversion helper earns its name only when the mapping is semantic,
lossy, fallible, or shape-changing.

Good:

```cpp
auto side_to_fix_char(types::side side) -> char;
auto parse_side(char value) -> lib::result<types::side>;
auto truncate_client_id(external::types::client_id id)
    -> lib::result<internal::types::client_id>;
```

## Forward Dependencies

Each function takes what it needs and returns what it produces; the
call graph reads in one direction with no residue left for a later
call to consume.

Good:

```cpp
column untie(const table& data);
table rank(const table& data, const column& tiebreaker);

table score(const table& data)
{
  return rank(data, untie(data));
}
```

## Function Return Types

Use a leading return type for simple non-template functions with a
short return type.

Good:

```cpp
bool is_market_order(const order& order)
{
  return order.limit_price == types::price{0};
}

lib::result<void> route(const request& request);
```

Use a trailing return type when it needs a name introduced by the
function declaration or when it keeps a dense return type from hiding
the function name.

Good:

```cpp
template <typename Range>
auto first_price(const Range& fills) -> typename Range::value_type::price_type;

auto make_handlers(const request& request)
    -> std::tuple<
      duplicate_order_handler,
      invalid_field_handler,
      unknown_route_handler>;
```

A trailing return type on every short, non-template function turns the
syntax into a habit instead of a readability choice.

Bad:

```cpp
auto is_market_order(const order& order) -> bool;
```

Good:

```cpp
bool is_market_order(const order& order);
```

## Types Carry Proof

Parse untyped input once at the boundary into a refined type; downstream
signatures take the refined type and trust it.

Good:

```cpp
auto parse_symbol(std::string_view raw) -> lib::result<types::symbol>;

void place_order(types::account account, types::symbol symbol, types::quantity qty);
```

A `bool` validator plus raw primitives forces every downstream caller
to remember which strings were checked.

Bad:

```cpp
void place_order(std::string_view account, std::string_view symbol, int qty);
```

Good:

```cpp
void place_order(types::account account, types::symbol symbol, types::quantity qty);
```

## Strong-Type Ergonomics

Same-type arithmetic stays in the strong type, and formatting goes
through the strong type. Use `.get()` only at a real boundary that
needs the primitive.

Good:

```cpp
remaining_quantity -= fill_quantity;
auto residual = order_quantity - filled_quantity; // still a quantity
fmt::format("{}", order_id);
```

Unwrapping with `.get()` to redo arithmetic the strong type already
supports, then rewrapping, is pure noise.

Bad:

```cpp
remaining_quantity = types::quantity{remaining_quantity.get() - fill_quantity.get()};
```

Good:

```cpp
remaining_quantity -= fill_quantity;
```

Accumulate in the strong type across a loop too.

Good:

```cpp
types::quantity total{0};

for (const auto& order : orders) {
  total += order.remaining_quantity;
}

return total;
```

Mixed-domain expressions fall back to the underlying type and stay
visible; an explicit rewrap marks the review point.

Good:

```cpp
auto net = filled_quantity - canceled_quantity; // quantity
auto raw = filled_quantity - limit_price;       // underlying type, visibly mixed
auto suspicious = types::quantity{filled_quantity - limit_price}; // review carefully
```

Reach a member of the underlying type through the wrapper's arrow, so
`.get()` keeps its meaning of "I need the primitive at this exact line."

Good:

```cpp
// secinfo.contract_multiplier : lib::strong_type<lib::decimal, ContractMultiplierTag>
const auto multiplier = secinfo.contract_multiplier->as_double();

// order_state.source_name : lib::strong_type<lib::fixed_string<42>, SourceNameTag>
log_info("source {}", order_state.source_name->to_string_view());
```

`.get().member()` inserts an unwrap where the arrow already names the
underlying member operation.

Bad:

```cpp
const auto multiplier = secinfo.contract_multiplier.get().as_double();
```

Good:

```cpp
const auto multiplier = secinfo.contract_multiplier->as_double();
```

Assign a whole new strong-typed value rather than mutating through a
read-only `.get()` view.

Good:

```cpp
order.symbol = types::symbol{"PETR4"};
```

## Designated Initializers

Use designated initializers with `.field{...}` labels and a trailing
comma; brace-elide non-scalar fields and let the strong type construct
without a rewrap.

Good:

```cpp
auto config = server_config{
  .listen_address = "0.0.0.0",
  .listen_port = 8080,
  .reuse_address = true,
  .backlog = 1024,
};

auto event = order_placed{
  .order_id{"O-12345"},
  .request_id{"R-98765"},
  .leaves_qty{100},
};
```

Positional aggregate init drops the field labels, and a `types::T{...}`
rewrap inside a designated init is the same noise as elsewhere.

Bad:

```cpp
auto config = server_config{"0.0.0.0", 8080, true, 1024};
```

Good:

```cpp
auto config = server_config{
  .listen_address = "0.0.0.0",
  .listen_port = 8080,
  .reuse_address = true,
  .backlog = 1024,
};
```

## Functional Core, Imperative Shell

Domain code is a pure value function; the runtime boundary picks the
provider, fetches the inputs, and calls the pure component.

Good:

```cpp
order_state apply_fill(order_state order, fill fill);

class risk_check {
public:
  lib::result<decision> check(const order& order, const limits& limits);
};

// Near main: choose the provider, fetch the limits, call the pure component.
auto limits = limits_provider.load(account);
BOOST_LEAF_ASSIGN(auto decision, risk.check(order, limits));
```

A domain method that constructs its own provider and reaches out to I/O
has pulled runtime composition into the core.

Bad:

```cpp
auto check(const order& order) -> lib::result<decision>
{
  auto limits = database_limits_provider{config_path_}.load(order.account);
  return check_against_limits(order, limits);
}
```

Good:

```cpp
lib::result<decision> check(const order& order, const limits& limits);
```

## Pipelines

A stage exposes inbound member functions and outbound callback fields
and does not know its consumer or thread policy; wiring near `main`
assigns the callbacks and decides the topology.

Good:

```cpp
class session {
public:
  void send(datagram_view bytes);

  lib::inplace_function<void(request&&)> on_request;
  lib::inplace_function<void(rejection&&)> on_rejected;
};

session.on_request = [&engine, &engine_loop](request&& req) {
  engine_loop.post([&engine, req = std::move(req)]() mutable {
    engine.send(std::move(req));
  });
};
```

A stage that stores a pointer to its consumer has absorbed the topology
the wiring point owns.

Bad:

```cpp
class session {
public:
  engine* engine_;
};
```

Good:

```cpp
class session {
public:
  lib::inplace_function<void(request&&)> on_request;
};
```

For tests, sandboxes, and constructor-failure cleanup, wire an explicit
noop for outputs irrelevant to the scenario.

Good:

```cpp
stage.on_rejected = [](rejection&&) {};
```

## Runtime And Threads

Capture posted work by value so it outlives the posting call, and post
to the owning loop rather than calling cross-thread into unsynchronized
state.

Good:

```cpp
output_loop.post([this, ev = std::move(ev)]() mutable {
  publisher_.send(std::move(ev));
});
```

Capturing by reference lets `ev` dangle once the caller returns.

Bad:

```cpp
output_loop.post([&] { publisher_.send(ev); });
```

Good:

```cpp
output_loop.post([this, ev = std::move(ev)]() mutable {
  publisher_.send(std::move(ev));
});
```

## Error Handling

A structured error payload carries typed domain context through
`code()` and `what()`.

Good:

```cpp
namespace routing::errors {

struct unknown_order {
  types::order_id order_id;

  auto code() const -> std::error_code
  {
    return make_error_code(routing::error_code::unknown_order);
  }

  auto what() const -> std::string
  {
    return fmt::format("unknown order {}", order_id);
  }
};

} // namespace routing::errors
```

A generic error string loses that typed context.

Bad:

```cpp
return lib::make_leaf_error(lib::error_code::generic_error, "unknown routing order");
```

Good:

```cpp
return lib::make_leaf_error(routing::errors::unknown_order{.order_id{order_id}});
```

Inside the domain, fallible helpers return the result type and compose
with the propagation macros; the body reads as the success path.

Good:

```cpp
lib::result<void> route(const new_order& request)
{
  BOOST_LEAF_ASSIGN(const auto& sink, select_sink(request.route));
  BOOST_LEAF_CHECK(orders_.process(request));
  on_routed(routed_order{.sink{sink}, .request = request});
  return {};
}
```

A `bool` return whose failure arms log and `return false` pushes error
handling into a side channel.

Bad:

```cpp
bool route(const new_order& request)
{
  auto sink = select_sink(request.route);
  if (!sink) {
    log("no sink");
    return false;
  }
  return true;
}
```

Good:

```cpp
lib::result<void> route(const new_order& request)
{
  BOOST_LEAF_ASSIGN(const auto& sink, select_sink(request.route));
  BOOST_LEAF_CHECK(orders_.process(request));
  on_routed(routed_order{.sink{sink}, .request = request});
  return {};
}
```

At a public boundary, consume the result with `try_handle_all` and
return the caller's vocabulary; do not leak the LEAF boundary through
the signature.

Good:

```cpp
void engine::handle(const request& request)
{
  boost::leaf::try_handle_all(
    [&]() -> lib::result<void> {
      BOOST_LEAF_CHECK(handle_impl(request));
      return {};
    },
    [&](lib::match_error<errors::duplicate_order>) {
      log_warn("duplicate order {}", request.order_id);
    },
    LIB_RESULT_CATCH_ALL(log_error("unhandled engine error")));
}
```

LEAF handlers are ordered: specific cases first, catch-all last. A
catch-all placed first shadows every following specific handler.

Bad:

```cpp
return std::make_tuple(
  LIB_RESULT_CATCH_ALL(return reject_internal(request);),
  [&](match_error<invalid_field> err) { return reject(request, err.value()); });
```

Good:

```cpp
return std::tuple_cat(
  std::make_tuple(
    [&](match_errors<duplicate_order, duplicate_request> err) {
      log_precondition(err);
      return drop_request();
    }),
  std::forward<Handlers>(handlers)...,
  std::make_tuple(
    [&](match_errors<invalid_field, unknown_route> err) {
      return reject(request, err.matched);
    },
    LIB_RESULT_CATCH_ALL(return reject_internal(request);)));
```

For a typed `enum class`, switch without `default` so the compiler
catches missing enumerators; return a structured error after the
switch for impossible deserialized values.

Good:

```cpp
auto to_wire(types::side side) -> lib::result<char>
{
  switch (side) {
    case types::side::buy: return '1';
    case types::side::sell: return '2';
  }

  return lib::make_leaf_error(errors::invalid_field_value{.field{"side"}});
}
```

For an untyped boundary value the compiler cannot help, so `default` is
required.

Good:

```cpp
auto parse_side(char value) -> lib::result<types::side>
{
  switch (value) {
    case '1': return types::side::buy;
    case '2': return types::side::sell;
    default:
      return lib::make_leaf_error(errors::invalid_field_value{
        .field{"side"},
        .value{std::string{value}},
      });
  }
}
```

When a function has three or more sequential fallible steps, extract
named helpers so the body reads as the success path under one boundary
handler.

Good:

```cpp
lib::result<void> handle_cancel_impl(const cancel_order& request)
{
  BOOST_LEAF_ASSIGN(auto& order, find_order(request.order_id));
  BOOST_LEAF_ASSIGN(auto& book, find_book(order.symbol));
  BOOST_LEAF_CHECK(cancel(book, order));
  return {};
}

void handle(const cancel_order& request)
{
  boost::leaf::try_handle_all(
    [&] { return handle_cancel_impl(request); },
    [&](lib::match_error<errors::unknown_order>) { log_warn("unknown order"); },
    [&](lib::match_error<errors::missing_book>) { log_error("missing book"); },
    LIB_RESULT_CATCH_ALL(log_error("unhandled cancel error")));
}
```

Unwrap a result through the propagation macros, which bind the success
value or forward the failure.

Good:

```cpp
BOOST_LEAF_ASSIGN(const auto& token, format_flag_set(set, exec_inst_table));
process(token);

BOOST_LEAF_CHECK(commit_order(request));
```

`result->member` is unchecked: on an error result `operator->` returns
`nullptr` and the chained call dereferences null.

Bad:

```cpp
fmt::format("{}", format_flag_set(set, exec_inst_table)->to_string_view());
```

Good:

```cpp
BOOST_LEAF_ASSIGN(const auto& token, format_flag_set(set, exec_inst_table));
fmt::format("{}", token.to_string_view());
```

For a `result` wrapping a strong type, unwrap the result with the macro
first, then chain through the strong type's arrow.

Good:

```cpp
BOOST_LEAF_ASSIGN(const auto& order_id, tracker.get_order_id(client_id));
log_info("order {}", order_id->to_string_view());
```

`.value()` throws on an error result at a site that does not expect to
catch, and `.value().get()` stacks two unidiomatic unwraps.

Bad:

```cpp
const auto id = tracker.get_order_id(client_id).value().get().to_string_view();
```

Good:

```cpp
BOOST_LEAF_ASSIGN(const auto& order_id, tracker.get_order_id(client_id));
const auto id = order_id->to_string_view();
```

## Invariants And Rollback

Commit at end: mutate a copy and swap it in on success, so a failing
validation leaves the live state untouched.

Good:

```cpp
auto add(order o) -> lib::result<void>
{
  BOOST_LEAF_CHECK(validate(o));
  auto next = orders_;
  next.emplace(o.id, std::move(o));
  orders_ = std::move(next);
  return {};
}
```

When a later fallible step must observe an earlier mutation, guard each
mutation with a scope exit and dismiss the guards only after the whole
operation commits.

Good:

```cpp
orders_.emplace(request.order_id, build_order_state(request));
auto undo_order = lib::scope_exit([&] { orders_.erase(request.order_id); });

requests_.emplace(request.request_id, build_request_state(request));
auto undo_request = lib::scope_exit([&] { requests_.erase(request.request_id); });

BOOST_LEAF_CHECK(limits_.reserve(request));

undo_request.dismiss();
undo_order.dismiss();
return {};
```

## Declarative Style

Stage derived values and name predicates so the success path reads as
domain steps.

Good:

```cpp
const bool has_residual = order.remaining_quantity > 0;
const bool is_market = order.limit_price == 0;
const bool should_rest = has_residual && !is_market;

if (should_rest) {
  rest(order);
}
```

Bind an optional in the `if` initializer where the branch proves it is
usable, then put the useful path in the body.

Good:

```cpp
for (const auto& fill : fills) {
  if (const auto resting_order = order_book.find_resting(fill.order_id);
      resting_order) {
    apply_fill(*resting_order, fill);
  }
}
```

## Variants, Concepts, And Templates

Dispatch over a variant with `lib::match` and one arm per meaningful
alternative; a missing alternative fails to compile.

Good:

```cpp
void send(const request& req)
{
  lib::match(
    req,
    [this](const new_order& order) { handle(order); },
    [this](const cancel_order& order) { handle(order); });
}
```

A manual `holds_alternative` / `get` chain reimplements the dispatch
and silently admits new alternatives.

Bad:

```cpp
if (std::holds_alternative<new_order>(req)) {
  handle(std::get<new_order>(req));
} else if (std::holds_alternative<cancel_order>(req)) {
  handle(std::get<cancel_order>(req));
}
```

Good:

```cpp
lib::match(
  req,
  [this](const new_order& order) { handle(order); },
  [this](const cancel_order& order) { handle(order); });
```

Use a concept for a public template contract.

Good:

```cpp
template <typename T>
concept ErrorData = requires(T t) {
  { t.code() } -> std::same_as<std::error_code>;
  { t.what() } -> std::same_as<std::string>;
};
```

Prefer capability dispatch over type-name dispatch.

Good:

```cpp
template <typename Alt>
auto request_id_of(const Alt& alt) -> std::optional<types::request_id>
{
  if constexpr (requires { alt.request_id; }) {
    return alt.request_id;
  }

  return std::nullopt;
}
```

Constrain a template that assumes a shape. When the body reads
`Outcome::result_type` and calls `Outcome::error(...)` and
`Outcome::fault()`, name that contract in the signature so misuse fails
at the call site; deduction still works.

Good:

```cpp
template <lib::Outcome Outcome, lib::Tuple... Handlers>
auto make_error_handlers(const new_order& req, Handlers&&... handlers);

// Caller writes the outcome alias once; result/error types are deduced.
auto handlers = make_error_handlers<order_outcome>(req);
```

A bare `typename` hides the contract in the body and pushes misuse into
a deep substitution failure.

Bad:

```cpp
template <typename Outcome, lib::Tuple... Handlers>
auto make_error_handlers(const new_order& req, Handlers&&... handlers);
```

Good:

```cpp
template <lib::Outcome Outcome, lib::Tuple... Handlers>
auto make_error_handlers(const new_order& req, Handlers&&... handlers);
```

Pair the concept with a small trait when the parameter must be a
specific class-template specialisation.

Good:

```cpp
namespace detail {

template <typename T>
struct is_outcome : std::false_type {};

template <typename Result, typename Error>
struct is_outcome<outcome<Result, Error>> : std::true_type {};

template <typename T>
inline constexpr bool is_outcome_v = is_outcome<T>::value;

} // namespace detail

template <typename T>
concept Outcome =
  detail::is_outcome_v<std::remove_cvref_t<T>>
  && requires {
       typename std::remove_cvref_t<T>::result_type;
       typename std::remove_cvref_t<T>::error_type;
       { std::remove_cvref_t<T>::error(
           std::declval<typename std::remove_cvref_t<T>::error_type>()) }
         -> std::same_as<std::remove_cvref_t<T>>;
       { std::remove_cvref_t<T>::fault() }
         -> std::same_as<std::remove_cvref_t<T>>;
     };
```

## State Machines

Model a lifecycle as a Boost.SML transition table in a detail namespace,
with `ev_*` event tags, `st_*` state tags, and an `actions` struct of
injected callbacks.

Good:

```cpp
namespace gateway::detail::session_state_machine_fsm {

struct ev_connect {};
struct ev_closed {};
struct st_closed {};
struct st_connecting {};

struct actions {
  lib::inplace_function<void()> async_connect;
};

struct transitions {
  auto operator()() const noexcept
  {
    namespace sml = boost::sml;
    return sml::make_transition_table(
      *sml::state<st_closed> + sml::event<ev_connect> = sml::state<st_connecting>,
      sml::state<st_connecting> + sml::on_entry<sml::_> /
        [](actions& a) { a.async_connect(); });
  }
};

} // namespace gateway::detail::session_state_machine_fsm
```

Correlated sibling booleans encode one lifecycle as several flags that
can drift into illegal combinations.

Bad:

```cpp
bool connected_ = false;
bool connecting_ = false;
bool retrying_ = false;
```

Good:

```cpp
boost::sml::sm<detail::session_state_machine_fsm::transitions> state_machine_;
```

## Cross-Cutting Services

For a genuine cross-cutting service, keep a variant-backed global
configured once in `main` and dispatch through `lib::match` from free
functions.

Good:

```cpp
using logger = std::variant<console_logger, file_logger, null_logger>;
inline logger global_logger{null_logger{}};

void log(level lvl, std::string_view msg)
{
  lib::match(global_logger, [&](auto& impl) { impl.log(lvl, msg); });
}
```

## Performance Discipline

On a measured hot path, use bounded text, bounded or reserved-once
vectors, and fixed-capacity stored callbacks.

Good:

```cpp
using symbol = lib::strong_type<lib::fixed_string<16>, struct SymbolTag>;

std::vector<order> orders_;
orders_.reserve(config.max_orders);

lib::inplace_function<void(message&&), 256> on_message;
```

On that same path, an unbounded `std::string`, an unreserved vector, and
a `std::function` each allocate where the bounded form does not.

Bad:

```cpp
using symbol = std::string;
std::function<void(message&&)> on_message;
```

Good:

```cpp
using symbol = lib::strong_type<lib::fixed_string<16>, struct SymbolTag>;
lib::inplace_function<void(message&&), 256> on_message;
```

## Comments

Comment present intent and non-obvious flow. A class or header comment
states what the type is and the rules it follows.

Good:

```cpp
/*
 * Typed requests produced by the decoder from wire bytes.
 * Market orders are signaled by limit_price == 0 and follow IOC semantics.
 */
struct new_order {
  types::user_id user;
  types::price limit_price;
};
```

Block-level flow comments read like the function's table of contents.

Good:

```cpp
// Reject duplicates and resolve the destination book up front.
BOOST_LEAF_CHECK(check_duplicate(incoming_key));
BOOST_LEAF_ASSIGN(auto* book_ptr, find_book(request.instrument));
auto& book = *book_ptr;

// Ack precedes trades so receivers see the order id before fills on it.
on_event(order_ack{
  .user{request.user},
  .order_id{request.order_id},
});

// Rest the residual: pool-allocate a node, link it into the book,
// register its identity for future cancels and duplicate checks.
order_node* node = allocate_node(order);
book.place(node);
resting_index_.emplace(incoming_key, node);
```

A negative-documentation comment narrates absent or relocated behavior
instead of the present code.

Bad:

```cpp
// Old implementation used a vector here.
// Dedup moved to the upstream stage.
```

Good:

```cpp
// Index resting orders by incoming key so cancels and duplicate checks resolve in one lookup.
```

Phrase a precondition as the invariant the code relies on.

Good:

```cpp
// precondition: session mutex is held; next_seq is read and incremented without locking here.
auto next = session_.next_seq++;
```

## Namespace Aliases

In a `.cpp` or test file, use short, stable aliases already common in
the project when a file repeatedly mixes domain vocabularies.

Good:

```cpp
namespace md = market_data;
namespace me = matching_engine;
namespace rt = order_routing;

auto trade = md::trade{
  .user = md::types::user_id{request.user},
  .trade_price = md::types::price{request.limit_price},
};
```

A blanket `using namespace` or a `using` declaration pulling a domain
type into the local scope makes lookup depend on include order.

Bad:

```cpp
using namespace order_routing;
using order_routing::types::price;
```

Good:

```cpp
namespace rt = order_routing;
auto price = rt::types::price{request.limit_price};
```

Local aliases inside a function for dense template or FSM namespaces are
fine.

Good:

```cpp
namespace sml = boost::sml;
namespace fsm = gateway::detail::session_state_machine_fsm;
```

## Const Placement

Use west const.

Good:

```cpp
void handle(const request& request);
for (const auto& order : orders) { /* ... */ }
```

East const places `const` after the type.

Bad:

```cpp
void handle(request const& request);
```

Good:

```cpp
void handle(const request& request);
```
