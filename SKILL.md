---
name: taskworker-framework
description: 'Create and manage TaskWorker agents - signal-driven, audit-trail-enabled workers for OpenClaw. Use when: (1) building new TaskWorker agents, (2) setting up task distribution infrastructure, (3) implementing agent orchestration patterns. NOT for: simple one-off tasks (use direct tools), non-agent workflows (use n8n/Dify).'
metadata:
  {
    "openclaw": { 
      "emoji": "🐝", 
      "requires": { 
        "anyBins": ["task", "python3"] 
      } 
    },
  }
---

# TaskWorker Framework

Signal-driven agent infrastructure for OpenClaw.

## Overview

TaskWorker is a pattern for creating **stable, auditable, specialized agents** that:
- Wait passively for signals (no token-wasting polling)
- Claim tasks from a shared queue
- Execute with clear boundaries
- Leave audit trails for everything

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Signal-Driven** | Agents wake up only when notified via HEARTBEAT.md |
| **Audit Trail** | Every action logged: `completed_by`, `rejected_by`, timestamps |
| **Reject > Fail** | Agents refuse out-of-scope work rather than failing silently |
| **Layered Determinism** | Fixed protocol, flexible execution |

## Architecture

```
┌─────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────┐
│  User   │────▶│ Taskwarrior │────▶│ Hook Script │────▶│  Agent  │
│ (create)│     │  (queue)    │     │ (notify)    │◀────│ (wake)  │
└─────────┘     └─────────────┘     └─────────────┘     └────┬────┘
                                                             │
                                    ┌─────────────────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │ HEARTBEAT.md        │
                         │ "检查任务列表"       │
                         └─────────────────────┘
```

## Quick Start

### 1. Install Hook (One-time setup)

```bash
cp ~/.openclaw/skills/taskworker-framework/bin/tw-hook.py \
   ~/.task/hooks/on-add-notify.py
chmod +x ~/.task/hooks/on-add-notify.py
```

### 2. Create a TaskWorker Agent

```bash
# Step 1: Create the agent
openclaw agents add my-worker --model bailian/kimi-k2.5 \
  --workspace ~/.openclaw/workspace-my-worker

# Step 2: Copy templates
cd ~/.openclaw/skills/taskworker-framework
cp templates/IDENTITY.md.tpl ~/.openclaw/workspace-my-worker/IDENTITY.md
cp templates/SOUL.md.tpl ~/.openclaw/workspace-my-worker/SOUL.md
cp templates/AGENTS.md.tpl ~/.openclaw/workspace-my-worker/AGENTS.md
cp templates/HEARTBEAT.md.tpl ~/.openclaw/workspace-my-worker/HEARTBEAT.md

# Step 3: Edit templates (fill in variables)
# - {name}: my-worker
# - {specialty}: your-specialty
# - {tags}: tag1,tag2

# Step 4: Register agent config
mkdir -p ~/.openclaw/agents/my-worker
cat > ~/.openclaw/agents/my-worker/config.yaml << YAML
name: my-worker
tags:
  - tag1
  - tag2
YAML
```

### 3. Create Tasks

```bash
task add "Do something" project:myproject tags:tag1,tag2
# Hook automatically notifies matching agents
```

## Worker Protocol

Fixed 6-step loop:

```
CHECK → FILTER → CLAIM → EXECUTE → VERIFY → DELIVER
```

See `templates/SOUL.md.tpl` for full protocol details.

## Audit Fields

All operations must set these fields:

| Action | Required Fields |
|--------|-----------------|
| Claim | `agent:{name}`, `started_at` |
| Complete | `completed_by:{name}`, `completed_at`, `result` |
| Reject | `rejected_by:{name}`, `rejected_at`, `reject_reason` |

## Examples

See `examples/chengyu-worker/` for a verified implementation.

## File Structure

```
taskworker-framework/
├── bin/
│   └── tw-hook.py          # Taskwarrior hook
├── templates/
│   ├── IDENTITY.md.tpl     # Agent identity template
│   ├── SOUL.md.tpl         # Behavior protocol template
│   ├── AGENTS.md.tpl       # Collaboration rules template
│   └── HEARTBEAT.md.tpl    # Signal channel template
└── examples/
    └── chengyu-worker/     # Verified example
```

## Best Practices

1. **Keep HEARTBEAT.md minimal** - Only signals, not task data
2. **Clear rejection reasons** - Specific, actionable explanations
3. **Verify before complete** - Self-check results before marking done
4. **Empty means idle** - No signal = no work to do

## Changelog

See `CHANGELOG.md` for version history.
