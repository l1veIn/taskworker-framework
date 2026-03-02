#!/usr/bin/env python3
"""
Taskwarrior on-add hook - 直接通知 TaskWorker Agent (v0.3.0)

发送可直接执行的命令给 Agent，Agent 收到后立即执行。
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


def notify_agent(agent_name, task_uuid, task_tags):
    """发送可直接执行的命令到 Agent"""
    # 构建可直接执行的检查命令
    tags_filter = ','.join(task_tags)
    command = f"task export {task_uuid} status:pending"
    
    message = f"""[TASK_ASSIGN] {task_uuid}
TAGS: {tags_filter}
ACTION: Run `{command}` to fetch and process this task.
"""
    
    try:
        result = subprocess.run(
            ['openclaw', 'agent',
             '--agent', agent_name,
             '--message', message,
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
    
    for agent_name in get_matched_agents(tags):
        notify_agent(agent_name, uuid, tags)
    
    print(json.dumps(task))


if __name__ == '__main__':
    main()
