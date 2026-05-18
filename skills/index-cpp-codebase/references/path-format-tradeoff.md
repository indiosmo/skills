# Path format trade-off

Two options for how file paths appear inside a module's file list. The
skill picked Option B. This note exists so a future reader who feels the
itch to switch back understands why we did not.

## Option A -- full path from repo root on every line

```
- (P) <project>/src/<module>/<module>/entry.hpp -- ...
```

- **Pro**: every line is a copy-pasteable `Read` argument with no
  concatenation. Reliability is independent of section context.
- **Pro**: same-named files across modules (`types.hpp`, `errors.hpp`)
  are unambiguous at the line level.
- **Con**: high token cost. With ~80 char paths repeated across 100+
  headers, the repetition dominates the file.
- **Con**: visually noisy. The interesting part of each line (the file
  name + description) sits at the end of a long prefix.

## Option B -- base path once per section, then module-relative paths (chosen)

```
Base path: `<project>/src/<module>/<module>/`

- (P) entry.hpp -- ...
- (I) detail/state.hpp -- ...
```

- **Pro**: dense, scannable, low-token.
- **Pro**: same-named files are still unambiguous because each file
  appears under its module's section -- the section header carries the
  disambiguator.
- **Con**: the agent has to concatenate base path + relative path to
  call `Read`. Trivial in principle, one extra step in practice.
- **Con**: if the section header is dropped (copy-paste of a fragment
  into another context), the relative paths lose their anchor.

## Why B

The token savings on a realistic codebase are large enough to justify the
concat step, and the section header keeps the anchor close. The
"fragment copy-paste" failure mode is rare enough to accept, and it can
be mitigated by **keeping the base path repeated on the first line of
each module's file list** so a copied section always brings its anchor.

If the failure mode hits in practice, switching to Option A is a
mechanical rewrite of the file.
