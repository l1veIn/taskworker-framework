# TaskWorker Framework

一套用于创建和管理 TaskWorker 类型 Agent 的基础设施。

## 核心理念

- **信号驱动**: Agent 被动唤醒，不主动轮询
- **审计追踪**: 所有操作留痕，可追溯
- **拒绝优于失败**: 明确边界，不硬撑
- **分层确定性**: 框架固定，执行灵活

## 快速开始

### 1. 安装 Hook（一次性）

cp ~/.openclaw/skills/taskworker-framework/bin/tw-hook.py ~/.task/hooks/on-add-notify.py
chmod +x ~/.task/hooks/on-add-notify.py

### 2. 创建 TaskWorker Agent

创建 Agent:
  openclaw agents add NAME --model MODEL --workspace ~/.openclaw/workspace-NAME

复制模板:
  cp templates/IDENTITY.md.tpl ~/.openclaw/workspace-NAME/IDENTITY.md
  cp templates/SOUL.md.tpl ~/.openclaw/workspace-NAME/SOUL.md
  cp templates/AGENTS.md.tpl ~/.openclaw/workspace-NAME/AGENTS.md
  cp templates/HEARTBEAT.md.tpl ~/.openclaw/workspace-NAME/HEARTBEAT.md

编辑模板，填充变量后注册:
  mkdir -p ~/.openclaw/agents/NAME
  echo "name: NAME" > ~/.openclaw/agents/NAME/config.yaml

### 3. 创建任务

task add "任务描述" project:PROJECT tags:TAG1,TAG2

Hook 会自动通知匹配的 Agent。

## 示例

见 examples/chengyu-worker/ - 已验证的成语接龙 Worker
