# Apply language and ecosystem conventions

Choose the meaning of a name from its behavior and domain, then express it in
the convention of the code being changed. Casing can make a name look familiar;
accuracy determines whether the reader's resulting expectation is justified.
Each section below can be read independently for its language. The linked
sources are official language or organizational guidance, with their scope
preserved in [the evidence register](evidence.md#language-and-artifact-claims).

## Establish the project's convention

Read applicable project guidance, linter settings, nearby declarations and
representative callers. Give explicit project rules precedence over an external
organization's preference. Preserve externally defined names where they are
contracts. Record inconsistencies and choose the rule governing the touched
surface; a naming task need not turn into a repository-wide casing change.

This guide's local policy defaults to full words and permits accepted domain
abbreviations in appropriate local scope. Familiarity and the reader's context
matter; the [empirical review](empirical-research.md#full-words-and-familiar-abbreviations)
explains the limited findings behind that default. Mechanical truncation such
as `export_resp` gains little clarity over `export_response`. An established
term such as `http` can be appropriate when the local readers know it.

All fenced use sites on this page are original, unexecuted pseudocode shaped
like the named language. They illustrate grammar and stipulated behavior;
compilation, framework compatibility, and runtime behavior require an actual
implementation and its checks.

## C++: distinguish the language from an adopted style guide

For code following Google's C++ guide, types and ordinary functions use
capitalized words, variables use snake case, and class data members carry a
trailing underscore. Namespaces use snake case. Struct data members and accessors
have their own rules; consult the precise category before applying a global
replacement. The C++ language supports other conventions, including APIs shaped
like the standard library. Google's
[Choosing Names](https://google.github.io/styleguide/cppguide.html#General_Naming_Rules),
[Type Names](https://google.github.io/styleguide/cppguide.html#Type_Names),
[Variable Names](https://google.github.io/styleguide/cppguide.html#Variable_Names)
and [Function Names](https://google.github.io/styleguide/cppguide.html#Function_Names)
state its organizational choices.

Original C++-shaped pseudocode for a predicate that reads a configured policy:

```text
RetryPolicy retry_policy;
if (retry_policy.ShouldRetry(attempt_count)) {
  ScheduleRetry(retry_delay);
}
```

The receiver establishes policy context, and `ShouldRetry` describes the decision
rather than transport capability. Verify the predicate against attempts, limits
and configured policy. Choose a capability name only for behavior that actually
answers that capability question. Google-style capitalized words make this
spelling consistent; they supply no evidence about the predicate's truth table.

Use scope to decide detail. A local `attempt_count` can fit a retry function;
a publicly exposed value may need more domain context. Inspect namespace-qualified
use sites before repeating the namespace inside every member name. See
[modules, packages and files](modules-packages-and-files.md).

## Python: use PEP 8 with project and protocol context

[PEP 8](https://peps.python.org/pep-0008/#naming-conventions) recommends snake case
for functions, methods and variables, CapWords for most classes, and uppercase
underscore names for constants. Modules use lowercase names; underscores can
improve readability there, while package names discourage them. Existing project
consistency is an explicit consideration. `self` and `cls` have established
method roles. A leading underscore marks a non-public interface convention;
double-leading underscores in a class engage name mangling, and documented
special names such as `__iter__` belong to language protocols.

Original Python-shaped pseudocode for a policy query and scheduling effect:

```text
if retry_policy.should_retry(attempt_count=attempt_count):
    schedule_retry(delay=retry_delay)
```

The keyword argument makes the number's role visible. Inspect keyword calls as
well as positional calls when judging parameter names. PEP 8 supplies no general
requirement that booleans begin with `is_`; establish assertion grammar and truth
conditions using the actual readers and surrounding names. See
[variables and state](variables-and-state.md) for polarity and policy distinctions.

PEP 8's [exception naming](https://peps.python.org/pep-0008/#exception-names)
uses `Error` for exceptions representing errors. Signaling exceptions can have
other names, as `StopIteration` demonstrates. An `ExportFormatError` therefore
requires an actual format-error contract; select and verify the exception type
against raises and handling sites. See [types and messages](types-and-messages.md).

## Rust: name ownership and method category accurately

Rust's [RFC 430](https://rust-lang.github.io/rfcs/0430-finalizing-naming-conventions.html#general-naming-conventions)
is the historical casing proposal. The API Guidelines'
[C-CASE](https://rust-lang.github.io/api-guidelines/naming.html#casing-conforms-to-rfc-430-c-case)
uses UpperCamelCase for types, traits and enum variants, snake case for modules,
functions and methods, and uppercase underscore forms for constants and statics.
Acronyms form one word in type names, such as `HttpClient`. RFC 430's crate row
prefers a single word; the current API Guidelines mark crate casing unclear.
Inspect package conventions and existing crate imports for a concrete choice.

The API Guidelines, rather than RFC 430, own the detailed
[C-CONV table](https://rust-lang.github.io/api-guidelines/naming.html#ad-hoc-conversions-follow-as_-to_-into_-conventions-c-conv).
Its scoped convention for ad-hoc conversion methods is:

| Prefix | Cost category | Input and output ownership |
| --- | --- | --- |
| `as_` | Free | Borrowed input, borrowed view |
| `to_` | Expensive | Borrowed input and borrowed output; borrowed input and owned non-Copy output; or owned Copy input and owned output |
| `into_` | Variable | Consumed owned non-Copy input, owned output |

Allocation is one possible cost. `to_` can perform validation while returning a
borrowed result; `into_` can consume a value through cheap or costly work.
Select the prefix from the actual ownership and cost contract.

Original Rust-shaped pseudocode: this stipulated buffer wrapper supports a free
borrowed frame view, a copied frame vector, and consumption into owned frames.

```text
let borrowed_frames = audio_buffer.as_frames();
let copied_frames = audio_buffer.to_frames();
let owned_frames = audio_buffer.into_frames();
```

These names require the described signatures and effects. Review borrowing,
copying, consumption, and validation before accepting them.

[C-GETTER](https://rust-lang.github.io/api-guidelines/naming.html#getter-names-follow-rust-convention-c-getter)
usually omits `get_`; exceptions include a single obvious stored value and checked
indexing. [C-ITER](https://rust-lang.github.io/api-guidelines/naming.html#methods-on-collections-that-produce-iterators-follow-iter-iter_mut-into_iter-c-iter)
assigns `iter`, `iter_mut` and `into_iter` to homogeneous collection methods with
borrowed, mutably borrowed, and owned elements. Text can expose `bytes` and
`chars`; free iterator-producing functions have their own descriptive names.
Inspect the method category before enforcing a prefix.

## Swift: judge the full call and its argument labels

Swift's [API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/)
prioritize clarity at use sites. Types and protocols use UpperCamelCase; other
names use lowerCamelCase. Names describe roles, while argument labels and the
base name cooperate to form a readable call. Inspect the labels as part of the
API rather than judging the function name alone. Follow
[Promote Clear Usage](https://www.swift.org/documentation/api-design-guidelines/#promote-clear-usage),
[Strive for Fluent Usage](https://www.swift.org/documentation/api-design-guidelines/#strive-for-fluent-usage),
and [Use Terminology Well](https://www.swift.org/documentation/api-design-guidelines/#use-terminology-well).

Original Swift-shaped pseudocode for inserting a frame at a buffer position:

```text
frameBuffer.insert(frame, at: insertionIndex)
```

The label `at` communicates the position's relationship to insertion. Assess it
with the parameter type, index validity, and actual mutation. Repeating the whole
operation in each argument label would add words without adding that relation.

Swift favors imperative names for effectful methods and value-oriented names
for queries. Mutation and derived-value pairs such as `sort` and `sorted` express
an ecosystem convention; adopt the form that matches the implementation. A
nonmutating boolean use should read as an assertion. `intersects` illustrates
that assertion grammar can work without `is`. Preserve the truth conditions
when changing grammar. The guidelines' capability-protocol and acronym rules
also have Swift-specific scope; consult their general conventions when naming
those artifacts. See [functions and methods](functions-and-methods.md) for the
underlying effects and result distinctions.

## JavaScript and TypeScript: identify the organization and framework

Google's [JavaScript naming guidance](https://google.github.io/styleguide/jsguide.html#naming)
uses UpperCamelCase for types and lowerCamelCase for methods, fields and
parameters. Its boolean accessors permit `get`, `is` and `has`. Private trailing
underscores are optional. Constant case depends on the value's constant semantics
and observable immutability; a `const` declaration alone does not settle it.
These are Google's JavaScript/Closure conventions.

Google's [TypeScript naming guidance](https://google.github.io/styleguide/tsguide.html#naming)
uses UpperCamelCase types, lowerCamelCase values and module aliases, and snake-case
filenames. It avoids type decorations and private underscores, accommodates
established framework conventions, and leaves Observable `$` suffixes to teams.
Its constant rule permits intended immutability, while the JavaScript guide asks
for a stronger observable-immutability property. Inspect the guide adopted by
the actual project before classifying a declaration.

Even official organizational guides differ. Google's TypeScript enum members
use constant case; the Microsoft TypeScript compiler
[contributor guidelines](https://github.com/microsoft/TypeScript/wiki/Coding-guidelines#names)
use PascalCase. Microsoft's page states its compiler-contributor scope. Language
validity and organization style are separate review questions.

Original JavaScript/TypeScript-shaped pseudocode for a retry policy:

```text
if (retryPolicy.shouldRetry(attemptCount)) {
  scheduleRetry(retryDelay);
}
```

The predicate concerns a decision under policy. Neither lowerCamelCase nor a
possible `is` prefix establishes that meaning. Read calls, returned values and
nearby methods to confirm it. When the interface exposes JSON fields or framework
callbacks with prescribed spellings, preserve that external contract and inspect
the mapping to internal names. See
[APIs, schemas and configuration](apis-schemas-and-configuration.md).

## Additional languages and final review

For another ecosystem, identify the compiler/runtime version and project guide,
then inspect the official naming sections for the artifact at hand. Separate
language constraints, standard-library conventions, framework contracts and
organization preferences. Inspect a few representative definitions and use
sites, plus linter or generator diagnostics where available. Mark any remaining
choice as a local recommendation with its rationale.

After selecting a spelling, review the name's fit against behavior, callers,
neighboring concepts, and documentation. Run the project's syntax and behavior
checks when applying it. A formatter can verify formatting within its scope;
semantic naming judgments need the actual context. Record these distinct results
using [contextual validation](contextual-validation.md), and follow
[renaming](renaming.md) for changes to affected references or public spellings.
