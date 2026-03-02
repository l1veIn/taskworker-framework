# TaskWorker Framework

🐝 Signal-driven agent infrastructure for OpenClaw

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](CHANGELOG.md)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-skill-green.svg)]()

## What is TaskWorker?

A pattern for building **stable, auditable, specialized AI agents** that:

- 🔔 **Wait passively** for work signals (no polling = 90% token savings)
- ✅ **Claim tasks** from a shared queue with clear ownership
- 🔍 **Leave audit trails** for every action
- 🚫 **Reject gracefully** when work is out of scope

## Quick Start

```bash
# 1. Clone this skill
git clone https://github.com/l1veIn/taskworker-framework.git \
  ~/.openclaw/skills/taskworker-framework

# 2. Install the hook (one-time)
cp bin/tw-hook.py ~/.task/hooks/on-add-notify.py
chmod +x ~/.task/hooks/on-add-notify.py

# 3. Create your first worker
openclaw agents add my-worker --model bailian/kimi-k2.5 \
  --workspace ~/.openclaw/workspace-my-worker

# Copy and customize templates
cp templates/*.tpl ~/.openclaw/workspace-my-worker/
# Edit files, replace {placeholders}

# 4. Register the worker
mkdir -p ~/.openclaw/agents/my-worker
echo "name: my-worker\ntags:\n  - mytag" > ~/.openclaw/agents/my-worker/config.yaml

# 5. Create a task
task add "Do something" project:test tags:mytag
# Worker gets notified automatically!
```

## How It Works

```
User creates task → Taskwarrior stores it → Hook notifies Agent → Agent wakes up
                                                           ↓
              ┌────────────────────────────────────────────┘
              ▼
    ┌─────────────────┐
    │ HEARTBEAT.md    │ ← "检查任务列表"
    └─────────────────┘
              │
              ▼
    Agent queries Taskwarrior → Claims matching task → Executes → Marks done
```

## Verified Example

See [`examples/chengyu-worker/`](examples/chengyu-worker/) - a working Chinese idiom game agent.

Tested scenarios:
- ✅ Normal task completion
- ✅ Invalid input rejection
- ✅ Multiple sequential tasks
- ✅ Idle state handling

## Documentation

- [`SKILL.md`](SKILL.md) - Full usage guide for OpenClaw
- [`templates/`](templates/) - Agent configuration templates
- [`CHANGELOG.md`](CHANGELOG.md) - Version history

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Signal-Driven** | Agents wake on demand, not by polling |
| **Audit Everything** | Every action traced: who, when, what |
| **Reject > Fail** | Clear boundaries prevent silent failures |
| **Layered Determinism** | Fixed protocol, flexible execution |

## Requirements

- [Taskwarrior](https://taskwarrior.org/) (`brew install task`)
- Python 3 (for hook script)
- OpenClaw with agent support

## Contributing

This is an evolving framework. See `CHANGELOG.md [Unreleased]` for planned features.

To contribute:
1. Fork the repo
2. Create your feature branch
3. Test with a new TaskWorker
4. Submit PR with changelog update

## License

MIT - See LICENSE file

---

Built for OpenClaw 🦞
