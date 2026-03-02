#!/bin/bash
# Taskwarrior on-add hook - v0.4.0 (Pure Bash)
# Usage: cp tw-hook.sh ~/.task/hooks/on-add-notify.sh

read TASK_JSON

# Extract UUID and tags using simple string operations
UUID=$(echo "$TASK_JSON" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)
TAGS=$(echo "$TASK_JSON" | grep -o '"tags":\[[^]]*\]' | sed 's/.*\[//;s/\].*//' | tr ',' ' ' | tr -d '"')

# Find matching agents
for CONFIG in ~/.openclaw/agents/*/config.yaml; do
    [ -f "$CONFIG" ] || continue
    
    AGENT=$(grep "^name:" "$CONFIG" | awk '{print $2}')
    [ -z "$AGENT" ] && continue
    
    # Check if any task tag matches agent tags
    for TAG in $TAGS; do
        if grep -q "^- $TAG$" "$CONFIG" 2>/dev/null; then
            # Send notification with executable command
            openclaw agent \
                --agent "$AGENT" \
                --message "[TASK_ASSIGN] $UUID
Run: task export $UUID status:pending" \
                --deliver \
                --timeout 10 2>/dev/null
            break
        fi
    done
done

# Output original task (required by Taskwarrior)
echo "$TASK_JSON"
