# AI-Native Infrastructure Framework

> A portable IDE platform providing stable toolkits and flexible project workspaces for AI-assisted development.

**English | [简体中文](README.md) | [日本語](README.ja.md)**

```
       ✩           ·  ★                    *          ☆     ★
   *        ★                    ✩                ·               *
  ╭──────────────────────────────────────────────────────────────────────╮
  │    ▄▄▄▄▄▄▄      ▄▄▄▄▄▄▄                                              │
  │   █       █    █       █   ██╗███╗   ██╗███████╗██████╗  █████╗ ██╗  │
  │   █   ▄▄▄▄█    █▄▄▄▄   █   ██║████╗  ██║██╔════╝██╔══██╗██╔══██╗██║  │
  │   █                    █   ██║██╔██╗ ██║█████╗  ██████╔╝███████║██║  │
  │   █   ██          ██   █   ██║██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║██║  │
  │   █   ██    ▄▄    ██   █   ██║██║ ╚████║██║     ██║  ██║██║  ██║██║  │
  │   █        █  █        █   ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  │
  │    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀            AI-Native Infrastructure          │
  ╰──────────────────────────────────────────────────────────────────────╯
        ☆      *           ✩          ★      ·            ★       .
```

## 🎯 Core Philosophy

**User speaks naturally → AI codes with Skills → Tools assist execution**

This is a working environment framework designed for AI-assisted development:
- **User**: Issues commands in natural language, no technical details needed
- **AI**: Codes following Skills guidance, calls SDK tools for assistance
- **Tools**: Provide stable, predictable capabilities

## 🏗️ Architecture

This is a **portable IDE platform** with two layers:

### 📦 Framework Layer (Stable, not modified casually)
- `sdks/` - SDK toolkits
- `scripts/` - Framework tools
- `.claude/` - Claude Code configuration
- `docs/` - Specification documents
- `core/` - Framework core (portable template)
- `registry/` - Tool registry

### 💼 Project Layer (User workspace, flexible development)
- Create project subdirectories in root
- Examples: `my-web-app/`, `data-analysis/`
- Call framework layer SDK tools
- Implement business logic flexibly

**Architecture Analogy**:
- SDK Framework = npm package library (provides reusable tools)
- User Project = App using npm packages (calls tools, doesn't modify tool source)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Project

Run in Claude Code:

```
/init
```

Or run manually:

```bash
python scripts/list_tools.py    # View available tools
python scripts/list_skills.py   # View available skills
python scripts/audit_all.py     # Health check
```

### 3. Create Your First Project

Tell AI in natural language:

```
"Help me create a web application"
"Create a data analysis project"
"Implement user login functionality"
```

AI will automatically:
1. Ask for project name
2. Create project subdirectory in root
3. Set up project in project directory
4. Call SDK tools for assistance

## 🎯 Work Modes

### 🟢 Project Development Mode (Default)

AI defaults to this mode, working in project subdirectories:

```
"Create a new project"
"Implement user login functionality"
"Add data validation"
"Fix this bug"
```

### 🔧 SDK Development Mode (Explicit trigger)

Only enters this mode when explicitly stated:

```
"Modify infra-core SDK"
"Create a new SDK tool"
"Extend framework functionality"
```

## 📁 Directory Structure

```
infra_demo/                      # Portable IDE platform
│
├── [Framework Layer - Stable, not modified casually]
├── sdks/                        # SDK toolkits
│   └── infra-core/              # Core framework SDK
│       ├── api/                 # Python API
│       ├── cli/                 # CLI entry
│       ├── skills/              # Skills implementation
│       └── tests/               # Tests
│
├── scripts/                     # Framework tools
├── .claude/                     # Claude Code configuration
│   ├── commands/                # Custom commands
│   └── skills/                  # Skills entry
│
├── docs/                        # Specification documents
├── core/                        # Framework core (portable template)
├── registry/                    # Tool registry
│
├── [Project Layer - User workspace]
├── my-web-app/                  # User project example 1
│   ├── src/
│   └── ...
│
├── data-analysis/               # User project example 2
│   ├── notebooks/
│   └── ...
│
└── <project-name>/              # Other user projects
    └── ...
```

## 🛠️ Core Principles

### 1. SDK Stability Principle

- **Framework layer is stable**: SDK toolkits not modified casually
- **Project layer is flexible**: User projects can be developed freely
- **New features implemented in projects first**: Consider migrating to SDK after validation

### 2. Work Mode Recognition

- **Default project development mode**: AI works in project subdirectories
- **Explicit trigger for SDK development mode**: Only modifies framework layer when explicitly stated
- **Ask user when uncertain**: AI confirms user intent first

### 3. Request → Tool → Integration

- Every request should produce executable tools
- Not allowed to only output documentation without creating tools
- Tools must support `--help`, errors output to stderr

## 📚 Documentation Index

| Document | Purpose |
|----------|---------|
| `CLAUDE.md` | AI project context (auto-loaded) |
| `BOOTSTRAP.md` | New project initialization guide |
| `docs/60_sdk_specification.md` | SDK specification |
| `docs/TROUBLESHOOTING.md` | Troubleshooting |
| `core/docs/00_operating_manual.md` | Operating principles |
| `core/docs/10_tooling_conventions.md` | CLI conventions |
| `core/docs/50_skills_system.md` | Skills system |

## 🔧 Common Commands

### SDK CLI (New Architecture)

```bash
# Audit SDK
python sdks/infra-core/cli/main.py audit-sdk sdks/infra-core

# Audit documentation
python sdks/infra-core/cli/main.py audit-docs docs

# Audit Skills
python sdks/infra-core/cli/main.py audit-skills .claude/skills
```

### Standalone Tools (Legacy Architecture Compatibility)

```bash
# View tools
python scripts/list_tools.py

# View skills
python scripts/list_skills.py

# Health check
python scripts/audit_all.py
```

## 💡 Usage Examples

### Create New Project

```
User: "Help me create a web application"

AI: "Sure, what's the project name?"

User: "my-web-app"

AI:
1. Create project directory: mkdir my-web-app
2. Switch to project directory: cd my-web-app
3. Set up web application in project
4. Call SDK tools (if needed)
```

### Implement Functionality

```
User: "Implement user login functionality"

AI:
1. Check existing SDK capabilities
2. Implement login functionality in project
3. Call SDK tools for assistance
4. Don't modify framework layer files
```

### Modify SDK (Explicit Trigger)

```
User: "Modify infra-core SDK, add new audit functionality"

AI:
1. Recognize explicit SDK modification command
2. Enter SDK development mode
3. Modify sdks/infra-core/api/audit.py
4. Update related tests and documentation
5. Run audit-sdk for validation
```

## 🎓 Best Practices

### For Users

1. **When creating projects**: Say "create a XXX project"
2. **When developing features**: Say "implement XXX functionality"
3. **When modifying framework**: Explicitly say "modify SDK" or "extend framework"
4. **When uncertain**: Express intent in natural language, AI will guide you

### For AI

1. **Default project development mode**: Work in project subdirectories
2. **Prioritize SDK tools**: Rather than reimplementing
3. **Ask about migration after maturity**: Don't migrate project code to SDK without permission
4. **Ask user when uncertain**: Rather than making assumptions

## 🤝 Contributing

### Adding New Tools

1. Implement and validate in project
2. Consider migrating to SDK after maturity
3. Follow `docs/60_sdk_specification.md` specification
4. Run `audit-sdk` for validation

### Creating New SDK

1. Follow SDK package specification
2. Include API, CLI, Skills, Tests
3. Update manifest.yaml
4. Create corresponding entry skills

## 📄 License

MIT License

## 🔗 Related Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude/docs)
- [SDK Specification](docs/60_sdk_specification.md)
- [Skills System Guide](core/docs/50_skills_system.md)

---

**Tip**: This is an AI-Native development environment. Just tell AI what you want to do in natural language, and it will guide you through!
