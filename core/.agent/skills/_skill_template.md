# [Skill Name]

## Purpose
[What does this skill do? Brief description of the tool's function.]

## When to Use
[Under what conditions should the AI trigger this skill?]

## Trigger Phrases
When the user says:
- "[Example phrase 1]"
- "[Example phrase 2]"
- "[中文触发短语]"

## Command
```bash
# Basic usage
python scripts/<tool>.py

# With options
python scripts/<tool>.py --flag value
```

## Principles
1. [Core rule 1]
2. [Core rule 2]

## Checkpoints
Before executing, confirm with the user:
1. [ ] [Key decision point 1]
2. [ ] [Key decision point 2]

## Recovery Strategy

### Exit 0 (Success)
- Proceed to next step
- No action needed

### Exit 2 (Parameter Error)
- Check command syntax
- Run `--help` to see valid options
- Verify argument values
- Retry with corrected parameters

### Exit 3 (Runtime Error)
- Read stderr for error details
- Common causes:
  - File not found: Check path spelling
  - Permission denied: Check file permissions
  - Invalid format: Validate input data
- Fix the underlying issue before retrying
- Maximum 1 retry attempt

### When to Escalate to User
- After 1 failed retry
- When error cause is unclear
- When fix requires user decision

## HARD GATES (Non-Negotiable)
[Conditions that MUST be met for the skill to be considered complete]
- [ ] [Required condition 1]
- [ ] [Required condition 2]
