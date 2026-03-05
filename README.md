# Infra Foundation

A Python + CLI infrastructure foundation engineered for SDK and Agent tools.

## Core Principles

1. **Explicit Tools**: All tools are registered in a central registry (`registry/tools.yaml`).
2. **CLI Native**: All commands utilize CLI architectures via python scripts with unified conventions (`--help`, `stderr`, standard exit codes).
3. **Action-Oriented**: "Requests -> Tools -> Integration". Every request creates a runnable capability, not just a document. 

## Structure

- `docs/`: Operating manuals and tool conventions.
- `registry/`: The singular source of truth for tools.
- `scripts/`: Tool implementations and Command Palette.
- `.agent/`: Skills and prompts for AI extension.

## Getting Started

```bash
pip install -r requirements.txt
python scripts/list_tools.py
```

```
CLI LOGO :

  ╔══════════════════════════════════════════════════════════════════════╗
  ║    ▄▄▄▄▄▄▄      ▄▄▄▄▄▄▄                                              ║
  ║   █       █    █       █   ██╗███╗   ██╗███████╗██████╗  █████╗ ██╗  ║
  ║   █   ▄▄▄▄█    █▄▄▄▄   █   ██║████╗  ██║██╔════╝██╔══██╗██╔══██╗██║  ║
  ║   █                    █   ██║██╔██╗ ██║█████╗  ██████╔╝███████║██║  ║
  ║   █   ██          ██   █   ██║██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║██║  ║
  ║   █   ██    ▄▄    ██   █   ██║██║ ╚████║██║     ██║  ██║██║  ██║██║  ║
  ║   █        █  █        █   ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ║
  ║    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀            AI-Native Infrastructure          ║
  ╚══════════════════════════════════════════════════════════════════════╝

```