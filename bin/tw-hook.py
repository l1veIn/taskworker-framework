#!/usr/bin/env python3
"""
Taskwarrior on-add hook - 自动通知匹配的 TaskWorker Agent

安装: cp this_file ~/.task/hooks/on-add-notify.py
      chmod +x ~/.task/hooks/on-add-notify.py
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def get_matched_agents(task_tags):
    """根据任务标签匹配 Agent"""
    agents_dir = Path.home() / '.openclaw' / 'agents'
    if not agents_dir.exists():
        return []
    
    matched = []
    for agent_dir in agents_dir.iterdir():
        config_file = agent_dir / 'config.yaml'
        if not config_file.exists():
            continue
        
        # 解析 YAML
        agent_name = None
        agent_tags = []
        
        with open(config_file) as f:
            for line in f:
                line = line.rstrip()
                if line.startswith('name:'):
                    agent_name = line.split(':', 1)[1].strip()
                elif line.strip().startswith('- '):
                    tag = line.strip()[2:].strip()
                    agent_tags.append(tag)
        
        if agent_name and set(task_tags) & set(agent_tags):
            matched.append(agent_name)
    
    return matched


def notify_agent(agent_name, task_uuid):
    """在 Agent HEARTBEAT.md 中写入信号"""
    workspace = Path.home() / f'.openclaw/workspace-{agent_name}'
    workspace.mkdir(parents=True, exist_ok=True)
    
    heartbeat = workspace / 'HEARTBEAT.md'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(heartbeat, 'a') as f:
        f.write(f'[{timestamp}] NEW_TASK: {task_uuid}\n')
        f.write('ACTION: 检查任务列表\n\n')


def main():
    # 读取 stdin 的 JSON
    line = sys.stdin.readline()
    task = json.loads(line)
    
    uuid = task.get('uuid', 'unknown')
    tags = task.get('tags', [])
    
    # 匹配并通知 Agents
    for agent_name in get_matched_agents(tags):
        notify_agent(agent_name, uuid)
    
    # 必须输出原始任务
    print(json.dumps(task))


if __name__ == '__main__':
    main()
