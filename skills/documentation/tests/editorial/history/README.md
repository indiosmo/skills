# Bounded history exercise

This synthetic history teaches an author to separate code changes, documentation
changes and release claims. Read `history.patch` in order from base `fixture-v1`
to target `fixture-v2`, inspect the net behavior, then write all three outputs.
Patch IDs are fixture identifiers, not real repository commits. `expected.md`
contains the review oracle.

The base counter prints the number of newline characters in a UTF-8 file. The
base guide says it counts newline characters and has no empty-file example.
The target retains the newline behavior, rejects invalid UTF-8 with a clearer
message, and includes an empty-file example. A proposed binary-input feature is
fully reverted. No release metadata establishes compatibility with Python 3.15.

Review criteria: separate a mixed commit into its relevant output classes;
deduplicate the error-message change and its follow-up wording; exclude the
reverted feature; retain the unsupported compatibility claim in review material.
For a live repository, additionally execute the read-only commands in
[the history workflow](../../../references/changelog-workflow.md#inspect-the-range).
