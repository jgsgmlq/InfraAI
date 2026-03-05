# Build CLI Tool

## Purpose
To fulfill user infrastructure requests by constructing a tangible, executable CLI tool instead of merely outputting code or documentation.

## When to Use
- Whenever the user asks to "build a tool for X"
- Whenever a gap in the operational workflow is identified that could be solved by a script
- When automating a repetitive task

## Trigger Phrases
When the user says:
- "我需要一个工具来..."
- "帮我写一个脚本..."
- "build a tool for..."
- "create a CLI that..."
- "automate this process"
- "写个工具"

## Command
This skill produces new tools, not executes existing ones.

Reference template: `scripts/_example_tool.py`

## Principles
1. **No Pure Documentation:** A request to build a tool MUST yield an executable. Outputting only a markdown file explaining how to do it is FORBIDDEN.
2. **Registry First:** Every new tool must be registered in `registry/tools.yaml`.
3. **Convention Adherence:** The tool must follow `docs/10_tooling_conventions.md`.
4. **Testability:** A smoke test must be provided to prove the tool works.
5. **Reference Implementation:** Use `scripts/_example_tool.py` as starting point.

## Checkpoints
Before starting implementation, confirm with the user:
1. [ ] Tool name and ID (e.g., `my-tool`, `scripts/my_tool.py`)
2. [ ] CLI interface design (what flags/arguments?)
3. [ ] Expected inputs and outputs
4. [ ] Success criteria

## Recovery Strategy

### Smoke Test Fails (Exit 3)
- Read test output to identify failing case
- Check if script handles edge cases
- Fix the script, not the test
- Re-run smoke test

### Import Error
- Check `requirements.txt` for missing dependencies
- Add dependency if needed
- Re-run after `pip install`

### Registry Validation Fails
- Run `python scripts/audit_registry.py` to identify issues
- Fix missing fields (version, aliases, etc.)
- Ensure all required files exist

### When to Escalate to User
- Unclear requirements for CLI design
- Conflicting requirements
- Need to modify existing tools

## HARD GATES (Non-Negotiable)
You CANNOT consider the task complete unless ALL of the following exist:
- [ ] Added entry to `registry/tools.yaml` (with version, aliases)
- [ ] Created `scripts/<tool_name>.py`
- [ ] Created `scripts/smoke/smoke_<tool_name>.sh`
- [ ] Created `.agent/skills/<tool_name>.md`
- [ ] Verified the tool handles `--help`
- [ ] Verified the tool routes errors to `stderr` and uses exit codes (0, 2, 3)
- [ ] Ran `python scripts/audit_registry.py` and ALL PASSED
