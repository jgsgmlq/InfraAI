# Infra Request Skill

Core Philosophy: Every infra request MUST result in a usable tool that becomes part of the operational toolkit.

## Principle: Request -> Tool -> Integration

The infra request lifecycle:

1.  Identify gap: Operational need blocks current workflow
2.  Request tool: File infra request specifying the tool to build
3.  Infra delivers: Working script/binary/documentation
4.  Integrate: Tool becomes available for future use
5.  Iterate: Tool gets refined based on actual usage

FORBIDDEN: Requests that only produce documentation without executable tools.

## How to Use

When filing an infra request:

1.  Identify the tool needed
    * What executable will solve this problem?
    * What should the command-line interface be?
    * What inputs and outputs?

2.  Specify deliverables
    * Request SPECIFIC tools (scripts, binaries, skills)
    * NOT just "fix X" or "improve Y"
    * Example: "Build `scripts/sync_eod_data.sh`" NOT "provide data access"

3.  Define integration
    * Where will this tool live? (`scripts/`, `.agent/skills/`, `bin/`)
    * How will I invoke it in future sessions?
    * What other tools depend on this?

## The Golden Process

1. **Check Command Palette**: Always look at available tools first.
   - Run: `python scripts/list_tools.py`
2. **Use Existing Tools**: If a tool meets the requirement, use it.
3. **Draft Tool Spec**: If missing, write a spec (based on `docs/20_task_spec_template.md`).
4. **Implementation**: Ensure all conventions in `docs/10_tooling_conventions.md` are upheld.
5. **No Pure Documentation**: Documentation must always be paired with functionality.
