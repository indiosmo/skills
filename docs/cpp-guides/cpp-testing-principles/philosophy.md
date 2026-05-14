# Testing philosophy

A test encodes an independent statement of expected behavior, derived from the
domain and the contract -- not from the implementation.

## Test behavior, not implementation

A test verifies the **intended semantics** of the code: its contract,
invariants, and expected outcomes. A test that re-derives what the
implementation already does is a tautology -- it catches nothing, because the
same bug in the production code and in the test will line up and produce a
green run.

A contract is the visible agreement between caller and callee: preconditions
the caller must satisfy, postconditions the callee can rely on afterward, and
invariants the component preserves. These guides use the term broadly; it is
not limited to the C++ language feature.

The first question to ask of any test is: "if someone introduced a subtle bug
here, would this test fail?" If the answer is "only if the bug also rewrites
the test", the test catches nothing.

```cpp
// BAD - tautological. The test re-runs the implementation formula.
// A bug in either side of the subtraction would still produce a passing test.
TEST_CASE("rectangle - area")
{
  rectangle r{.width = 6, .height = 4};
  CHECK(r.area() == r.width * r.height);
}
```

```cpp
// GOOD - the expected value comes from the specification, not from the code.
TEST_CASE("rectangle - area")
{
  rectangle r{.width = 6, .height = 4};
  CHECK(r.area() == 24);  // 6 * 4, derived from the definition of area
}
```

```cpp
// BAD - tautological. Replicates the encoding formula instead of citing the spec.
// A bug in the lookup table would produce the same wrong output on both sides.
TEST_CASE("url - percent encode")
{
  CHECK(percent_encode(" ") == "%" + hex_byte(' '));
}
```

```cpp
// GOOD - expected values come from the relevant specification.
TEST_CASE("url - percent encode")
{
  CHECK(percent_encode(" ") == "%20");
  CHECK(percent_encode("/") == "%2F");
  CHECK(percent_encode("?") == "%3F");
}
```

The corollary: **never encode buggy behavior into a test**. Write the test
against the correct expected behavior and let it fail -- a failing test is a
precise bug report, while a passing test that asserts the bug is correct locks
it in place.

## Understanding intent before writing tests

**Start from the domain, not the code.** Every function, type, and module
serves a purpose -- a file format, a network protocol, a user-facing workflow,
a mathematical definition, an API contract. Correctness, edge cases,
invariants, and error conditions all derive from that domain. Without the
domain, the only available expected value is the implementation's own output,
and the test collapses into the tautology above. Read the spec, the RFC, the
standard, the API documentation; talk to someone who understands the problem
when written sources fall short.

With the domain understood, the reading order through the code follows:

1. **Read the interface first.** Headers, doc comments, and type signatures
   describe the contract the code claims to honor.
2. **Read the surrounding context.** Callers reveal what the code is for.
   Related types, enums, and error codes describe the shape of the problem
   as the codebase models it.
3. **Read the implementation last.** Understand the algorithm, but do not let
   it dictate the tests. The implementation is the thing under test.

Where bugs concentrate:

- **Boundary conditions** -- off-by-one, empty inputs, capacity limits,
  zero/negative values, maximum and minimum representable values.
- **State transitions** -- invalid transitions, missing guards, double
  transitions.
- **Error paths** -- what happens when preconditions are violated? Are
  errors propagated? Is state rolled back?
- **Implicit assumptions** -- sorted input, non-null pointers, valid UTF-8,
  non-empty ranges. Test what happens when those assumptions break.
- **Combinatorial interactions** -- input type x option flag x mode. Some
  combinations are easy to overlook.
- **Semantic correctness** -- does `clear` actually leave the container
  empty? Does `copy` preserve the fields it should not change?

## Component vs integration tests

Component tests verify a single function or class in isolation; integration
tests verify that several components cooperate through a realistic workflow.
The distinction sets the scope of what a failure implicates: a component
failure points at an algorithm or contract, an integration failure points at
coordination between parts. When tests share setup but branch at a decision
point -- happy path vs. rejection, initial state vs. post-transition --
`SECTION` keeps the common setup from being duplicated while naming each
outcome explicitly.

## See also

- `test-patterns.md` -- choosing the Catch2 construct that matches the
  behavior under test.
- `error-path-testing.md` -- success paths, failure paths, and rollback
  assertions.
- `../cpp-design-principles/invariants.md` -- invariants, transactions, and
  rollback in production code.
