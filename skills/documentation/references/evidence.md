# Tracing documentation claims to evidence

An evidence register helps authors resolve conflicting sources and lets reviewers
check important claims without repeating the investigation. Keep a compact
register for the selected page or group using the
[evidence template](../templates/evidence-register.md).

## Choose evidence for the claim

| Claim kind | Useful evidence |
| --- | --- |
| Observed behavior | Relevant implementation and a reproducible test or observation at the target revision |
| Intended behavior | Accepted specification, API schema or decision approved for the target version |
| Historical rationale | Contemporaneous ADR, issue discussion or attributed expert account |
| Inference | Named premises, reasoning and explicit uncertainty; reviewer confirmation when factual accuracy matters |

Read relevant code paths, schemas, UI strings and tests together. A test passing
for one input proves that case; inspect coverage before generalizing. Issue
proposals describe intent only when their status supports it. Expert notes need
an author, date and scope. Existing documents provide context and links, and their
claims still need checking when they conflict with current sources.

## Resolve conflicts by version and claim kind

Record both sources and their revisions. Identify whether one describes a
released version, the current checkout, a proposed change or a historical
behavior. For a current behavior claim, reproduce the behavior and inspect the
implementation. For a normative contract, check the accepted specification and
raise an implementation disagreement rather than silently rewriting the contract.
Ask the relevant maintainer when the evidence cannot settle the intended target.

For example, an old guide may say an empty file raises an error while the target
revision's code and test return `0`. Record the exact sentence, both revisions,
the reproduction and the proposed correction. A proposed issue requesting an
error does not establish that the change shipped.

## Record useful provenance

For each material claim, record a stable identifier, exact draft text or section,
claim kind, source path or URL, symbol or section, revision/version, verification
method and result. Add retrieval dates to changing web sources and attributed
notes. Mark inaccessible material with its attempted location, access failure,
impact and follow-up owner. An unavailable source leaves the claim unverified.

Reader-facing citations should help a reader act or assess a consequential
claim: a specification section, API reference, relevant rationale or primary
publication. Keep transient logs and internal review notes in review material.
Prefer stable source permalinks when a revision matters, and use descriptive
link text. See Google's guidance on
[links](https://developers.google.com/style/link-text).

## Preserve support while editing

When wording changes, compare its subject, scope, conditions, numbers and strength
with the evidence. Update the claim text and source mapping in the same edit.
Splitting or merging claims retains the supporting identifiers. A change from
"the fixture returns 0" to "all invalid files return 0" creates a new claim and
requires new evidence. Recheck commands and samples after editorial changes to
quoting, flags, indentation and identifiers.
