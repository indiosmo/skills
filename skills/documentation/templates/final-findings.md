# Final findings format

The findings artifact is a JSON array using the category labels in
[final verification](../references/final-verification.md#findings-only-output).
Remove this instruction and emit only the array. A clean result is `[]`.

```json
[
  {
    "category": "Unsupported claims",
    "location": "document.md:line",
    "text": "Exact sentence from the draft.",
    "problem": "What the supplied evidence fails to establish.",
    "evidence_needed": "Specific evidence needed to verify the claim."
  }
]
```
