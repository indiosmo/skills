# Final-pass review oracle

The final findings artifact is only a JSON array with the eight category labels
specified by the final-verification reference. Each category has an independent
planted issue in `draft.md`:

| Category | Expected evidence |
| --- | --- |
| Unsupported claims | Exact sentence "The counter supports all file formats at unlimited speed."; contract supplies neither formats nor performance support |
| Missing prerequisites | Checkout, checked-in script, sample path and read access missing before execution |
| Ambiguous actions | "Run the script." and "Configure the processor appropriately." lack evidenced actions/values |
| Steps unverifiable from the supplied source material | Remote service deployment has no command or system evidence |
| Inconsistent product terminology | `processor` conflicts with `counter` in contract and glossary |
| Content belonging in another Diataxis quadrant | Text-processing philosophy/history interrupts the operational how-to; move to explanation |
| Google-style issues in titles, headings, voice, and word choice | Title case and dismissive `Easily`; vague passive recommendation |
| Risks of changing meaning in code samples | Quoted argument combines filename and `--verbose` into a different path; contract supports one path |

A corrected supported page can return `[]`. Validation report, human review and
delivery summary remain separate artifacts. Human review is pending until an
actual reviewer confirms the relevant revision.
