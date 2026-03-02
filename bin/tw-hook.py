#!/usr/bin/env python3
"""
Taskwarrior on-add hook - 直接通知匹配的 TaskWorker Agent

安装: cp this_file ~/.task/hooks/on-add-notify.py
      chmod +x ~/.task/hooks/on-add-notify.py

更新记录:
- v0.2.0: 改用 openclaw agent --message 直接通知，移除 HEARTBEAT.md 中转
- v0.1.0: 初始版本，使用 HEARTBEAT.md 信号
"""

import json
import sys
import subprocess
from pathlib import Path


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
    """直接发送消息到 Agent"""
    try:
        result = subprocess.run(
            ['openclaw', 'agent',
             '--agent', agent_name,
             '--message', f'[TASK] {task_uuid}',
             '--deliver',
             '--timeout', '10'],
            capture_output=True,
            timeout=15
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def main():
    line = sys.stdin.readline()
    task = json.loads(line)
    
    uuid = task.get('uuid', 'unknown')
    tags = task.get('tags', [])
    
    # 匹配并直接通知 Agents
    notified = []
    failed = []
    
    for agent_name in get_matched_agents(tags):
        if notify_agent(agent_name, uuid):
            notified.append(agent_name)
        else:
            failed.append(agent_name)
    
    # 静默处理失败，Agent 下次活跃时会自行检查队列
    
    print(json.dumps(task))


if __name__ == '__main__':
    main()
