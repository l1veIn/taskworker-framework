#!/bin/bash
# 直接通知 Agent（替代 HEARTBEAT.md 方案）
# Usage: tw-notify.sh <agent-name> <task-uuid>

AGENT=$1
TASK_UUID=$2

if [ -z "$AGENT" ] || [ -z "$TASK_UUID" ]; then
    echo "Usage: tw-notify.sh <agent-name> <task-uuid>"
    exit 1
fi

# 直接发送消息到 Agent
openclaw agent \
    --agent "$AGENT" \
    --message "[TASK] $TASK_UUID" \
    --deliver \
    --timeout 10 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ Notified $AGENT about task $TASK_UUID"
else
    echo "✗ Failed to notify $AGENT"
    # 失败时静默处理，Agent 下次活跃时会检查任务队列
fi
