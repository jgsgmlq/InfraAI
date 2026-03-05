# Task Specification Template

Use this format to define requirements before building a new tool.

## Objective
Briefly describe what this tool achieves and why it is needed.

## CLI Design
Describe the shape of the interface.
**Example Entry**: `python scripts/new_tool.py`

## Inputs
- Explain what the tool takes as input parameters.
- Mention any flags required (e.g. `--target`, `--verbose`).

## Outputs
- Explain what the tool produces.
- Standard Output vs Standard Error expectations.

## Edge Cases
- State potential error modes.
- Define what exit codes apply.

## Deliverables
- [ ] `registry/tools.yaml` entry
- [ ] Python script implementation (`scripts/<name>.py`)
- [ ] Smoke test (`scripts/smoke/smoke_<name>.sh`)
- [ ] Skill document (`.agent/skills/<name>.md`)

## Acceptance Criteria
- [ ] Can display `--help`.
- [ ] Obeys `0` (Success), `2` (Argument error), `3` (Execution error) exit statuses.
- [ ] Passes smoke test verifications.
