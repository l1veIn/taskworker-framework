#!/bin/bash
# Taskwarrior on-add hook - v0.5.0 (Strict Single-Task)
# Sends ONE task UUID to matching agent

read TASK_JSON

UUID=$(echo "$TASK_JSON" | grep -o '"uuid":"[^"]*"' | head -1 | cut -d'"' -f4)
TAGS=$(echo "$TASK_JSON" | grep -o '"tags":\[[^]]*\]' | sed 's/.*\[//;s/\].*//' | tr ',' ' ' | tr -d '"')

for CONFIG in ~/.openclaw/agents/*/config.yaml; do
    [ -f "$CONFIG" ] || continue
    
    AGENT=$(grep "^name:" "$CONFIG" | awk '{print $2}')
    [ -z "$AGENT" ] && continue
    
    for TAG in $TAGS; do
        if grep -q "^- $TAG$" "$CONFIG" 2>/dev/null; then
            # Send ONLY the UUID, agent handles one task
            openclaw agent \
                --agent "$AGENT" \
                --message "[TASK_ASSIGN] $UUID" \
                --deliver \
                --timeout 10 2>/dev/null
            break
        fi
    done
done

echo "$TASK_JSON"
