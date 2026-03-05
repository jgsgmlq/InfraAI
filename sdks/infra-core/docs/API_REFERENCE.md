# infra-core API Reference

## Overview

`infra-core` SDK provides Python APIs for registry management and project auditing.

---

## Registry Module

### `load_registry(path)`

Load a YAML registry file.

**Parameters:**
- `path` (str | Path): Path to the registry YAML file

**Returns:**
- `List[Dict[str, Any]]`: List of tool entries

**Raises:**
- `RegistryNotFoundError`: If the file doesn't exist
- `RegistryError`: If the file can't be parsed

**Example:**
```python
from api.registry import load_registry

tools = load_registry("registry/tools.yaml")
for tool in tools:
    print(f"{tool['id']}: {tool['name']}")
```

---

### `validate_registry(tools, strict=False)`

Validate registry entries for required fields and duplicates.

**Parameters:**
- `tools` (List[Dict]): List of tool entries to validate
- `strict` (bool): If True, treat missing recommended fields as warnings

**Returns:**
- `Tuple[bool, List[str]]`: (is_valid, list_of_issues)

**Example:**
```python
from api.registry import load_registry, validate_registry

tools = load_registry("registry/tools.yaml")
is_valid, issues = validate_registry(tools, strict=True)

if not is_valid:
    for issue in issues:
        print(issue)
```

---

## Audit Module

### `audit_sdk(sdk_path)`

Audit an SDK package for completeness and correctness.

**Checks:**
- Required files exist (`__init__.py`, `version.py`, `manifest.yaml`, `README.md`, `CHANGELOG.md`)
- Required directories exist (`api/`, `tests/`)
- Recommended directories exist (`cli/`, `skills/`, `examples/`)
- `manifest.yaml` has required fields

**Parameters:**
- `sdk_path` (str | Path): Path to the SDK directory

**Returns:**
- `AuditResult`: Result object with `passed`, `findings`, `errors`, `warnings`

**Example:**
```python
from api.audit import audit_sdk

result = audit_sdk("sdks/my-sdk")

if result.passed:
    print("SDK audit passed!")
else:
    for error in result.errors:
        print(f"[ERROR] {error.message}")
```

---

### `audit_skills(skills_dir, sdk_dir=None)`

Audit skills configuration for valid frontmatter.

**Checks:**
- Entry skills have YAML frontmatter
- Required fields present (`name`, `description`)
- Implementation files exist (if `sdk_dir` provided)

**Parameters:**
- `skills_dir` (str | Path): Path to `.claude/skills/` directory
- `sdk_dir` (str | Path, optional): Path to `sdks/` directory for cross-reference

**Returns:**
- `AuditResult`: Result object with findings

**Example:**
```python
from api.audit import audit_skills

result = audit_skills(".claude/skills", sdk_dir="sdks")

for finding in result.findings:
    print(f"[{finding.severity.value}] {finding.message}")
```

---

### `audit_docs(docs_dir)`

Audit documentation for consistency.

**Checks:**
- Empty files (< 10 characters)
- Code blocks without language tags

**Parameters:**
- `docs_dir` (str | Path): Path to documentation directory

**Returns:**
- `AuditResult`: Result object with findings

**Example:**
```python
from api.audit import audit_docs

result = audit_docs("docs")

print(f"Errors: {len(result.errors)}")
print(f"Warnings: {len(result.warnings)}")
```

---

## Data Classes

### `AuditResult`

Result of an audit operation.

**Attributes:**
- `passed` (bool): True if no errors found
- `findings` (List[AuditFinding]): All findings

**Properties:**
- `errors`: List of ERROR severity findings
- `warnings`: List of WARNING severity findings

---

### `AuditFinding`

Single audit finding.

**Attributes:**
- `severity` (AuditSeverity): ERROR, WARNING, or INFO
- `category` (str): Category of the finding (structure, manifest, skills, docs)
- `message` (str): Description of the issue
- `path` (str, optional): File path related to the finding
- `suggestion` (str, optional): Suggested fix

---

### `AuditSeverity` (Enum)

Severity levels for audit findings.

**Values:**
- `ERROR`: Critical issue that fails the audit
- `WARNING`: Non-critical issue that should be addressed
- `INFO`: Informational message

---

## Exceptions

### `RegistryError`

Base exception for registry operations.

### `RegistryNotFoundError`

Raised when registry file doesn't exist.

### `RegistryValidationError`

Raised when registry validation fails.

---

## CLI Commands

The SDK also provides CLI commands via `sdks/infra-core/cli/main.py`:

```bash
# Audit SDK
python sdks/infra-core/cli/main.py audit-sdk sdks/infra-core

# Audit documentation
python sdks/infra-core/cli/main.py audit-docs docs

# Audit skills
python sdks/infra-core/cli/main.py audit-skills .claude/skills --sdk-dir sdks
```

**Exit Codes:**
- `0`: Audit passed
- `2`: Parameter error
- `3`: Audit failed (errors found)
