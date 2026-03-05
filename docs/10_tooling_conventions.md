# CLI Tooling Conventions

Standardize all Python scripts to ensure uniform command construction.

## CLI Core Rules

1. **Help Document**: All CLIs MUST support `--help` for comprehensive documentation.
2. **Error Output**: All errors MUST be routed to `stderr` (e.g., `sys.stderr.write()`).
3. **Standard Exit Codes**:
   - `0`: Success
   - `2`: Parameter Error / Bad Invocation
   - `3`: Runtime Error / Execution Failure

## Recommended Flags

Consider implementing the following where appropriate:
- `--dry-run`: Test execution without modifying state.
- `--out`: Specify an output file path for results.
- `--log-level`: Control log verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`).

## Tool Registration & Requirements

Every newly created tool must fulfill the following:

1. **Registry**: Must be included as a YAML entry in `registry/tools.yaml`.
2. **Skill Documentation**: Must add an accompanying skill under `.agent/skills/`.
3. **Testing**: Must have a functional smoke test (usually `.sh` wrapper checking exit codes).
4. **Version**: Must include a `version` field (semantic versioning: MAJOR.MINOR.PATCH).

## Registry Schema

Each tool entry in `registry/tools.yaml` MUST include:

```yaml
- id: tool-id                    # kebab-case identifier (REQUIRED)
  name: Human Readable Name      # Display name (REQUIRED)
  version: "1.0.0"               # Semantic version (REQUIRED)
  changelog: "Description"       # What changed in this version
  deprecated: false              # Set to true if deprecated
  type: cli                      # Tool type (REQUIRED)
  entry: python scripts/xxx.py  # Command to execute (REQUIRED)
  description: What it does      # Brief description (REQUIRED)
  aliases:                       # Natural language aliases (RECOMMENDED)
    - "中文别名"
    - "english alias"
  depends_on:                    # Tool dependencies (OPTIONAL)
    - other-tool-id
  examples:                      # Usage examples (RECOMMENDED)
    - "command example 1"
  flags:                         # CLI flags (REQUIRED if applicable)
    - name: --flag
      description: "What it does"
      required: false
  exit_codes:                    # Exit codes (REQUIRED)
    0: Success
    2: Parameter Error
    3: Runtime Error
```

## Verification

After creating a tool, run the audit to verify completeness:

```bash
python scripts/audit_registry.py
```
