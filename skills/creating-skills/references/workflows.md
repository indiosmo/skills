# Workflow Patterns

Patterns for structuring multi-step processes within skills.

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. Provide an overview at the beginning of SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

### Numbered Steps with Context

When steps need explanation, use numbered headers:

```markdown
## Step 1: Analyze the existing document

Before making changes, understand the document structure:
- Open the file and identify the XML namespace
- Check for existing tracked changes
- Note any custom styles in use

## Step 2: Make modifications

Apply changes while preserving document integrity:
- Use the appropriate API for the change type
- Maintain formatting consistency
- Preserve metadata
```

### Checklist Style

For verification-heavy workflows:

```markdown
## Pre-flight checks

Before deployment, verify:
- [ ] All tests pass
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Backup completed
```

## Conditional Workflows

For tasks with branching logic, guide Claude through decision points.

### Decision Tree Pattern

```markdown
## Workflow Decision Tree

1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below
   **Deleting content?** → Follow "Deletion workflow" below

## Creation workflow
[steps for creating]

## Editing workflow
[steps for editing]

## Deletion workflow
[steps for deleting]
```

### Feature Detection Pattern

```markdown
## Handling input files

Detect the file type and route accordingly:

**If PDF:**
- Check if fillable (has form fields)
- Fillable → use form-filling workflow
- Non-fillable → use overlay workflow

**If DOCX:**
- Check for tracked changes
- Has changes → prompt user to accept/reject first
- No changes → proceed with editing

**If image:**
- Extract text with OCR first
- Then process extracted text
```

### Fallback Pattern

```markdown
## Data extraction

Try methods in order until one succeeds:

1. **Structured extraction**: If the PDF has tagged content, extract directly
2. **Table detection**: If tables are detected, use tabula-py
3. **OCR fallback**: If above fail, convert to image and OCR
4. **Manual fallback**: If all else fails, prompt user for guidance
```

## Iterative Workflows

For tasks requiring refinement cycles:

```markdown
## Image generation workflow

1. Generate initial image from prompt
2. Show result to user
3. If user requests changes:
   - Incorporate feedback into prompt
   - Regenerate
   - Return to step 2
4. If user approves, save final image
```

## Parallel Workflows

When operations can run concurrently:

```markdown
## Build and test

These can run in parallel:
- Run unit tests
- Run linting
- Build documentation

Wait for all to complete before:
- Running integration tests
- Creating release artifact
```

## Error Recovery Workflows

```markdown
## Deployment workflow

1. Create backup of current state
2. Apply changes
3. Run health checks
   - **If healthy**: Complete deployment, clean up backup
   - **If unhealthy**: Restore from backup, report failure
```

## State Machine Workflows

For complex processes with multiple states:

```markdown
## Document review states

```
DRAFT → REVIEW → APPROVED → PUBLISHED
  ↓        ↓
REJECTED ←─┘
  ↓
DRAFT (revised)
```

**DRAFT**: Author can edit freely
**REVIEW**: Locked for reviewer comments only
**REJECTED**: Returns to author with feedback
**APPROVED**: Ready for publication
**PUBLISHED**: Live and versioned
```
