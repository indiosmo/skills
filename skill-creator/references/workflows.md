# Workflow Patterns

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. It is often helpful to give Claude an overview of the process towards the beginning of SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

## Conditional Workflows

For tasks with branching logic, guide Claude through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

## Feedback Loop Pattern

For skills that produce outputs requiring validation, implement a validate-fix-repeat cycle:

```markdown
## Output validation workflow

1. **Generate** initial output using the appropriate method
2. **Validate** the output:
   - Run `scripts/validate_output.py <output-file>`
   - Check for errors or warnings in the validation report
3. **If validation fails**:
   - Review the specific errors reported
   - Fix each issue in the output
   - Return to step 2
4. **If validation passes**: Proceed to delivery/next step
```

This pattern is essential for skills producing structured outputs (code, documents, data files) where correctness matters.

## Skill Effectiveness Checklist

Use this checklist when reviewing skill quality:

**Core requirements:**
- [ ] SKILL.md has valid frontmatter with name and description
- [ ] Description explains what the skill does AND when to use it
- [ ] SKILL.md is under 500 lines
- [ ] All referenced files exist and paths are correct

**Design quality:**
- [ ] Only includes information Claude doesn't already know
- [ ] Uses appropriate degrees of freedom (not over-specified or under-specified)
- [ ] Complex details moved to reference files (progressive disclosure)
- [ ] Scripts are tested and work correctly

**Usability:**
- [ ] Clear workflow steps for multi-step tasks
- [ ] Examples provided where helpful
- [ ] No unnecessary documentation files (README, CHANGELOG, etc.)