# AGENTS.md - Collaboration Rules

## 我的角色
TaskWorker-{specialty}: 被动接收任务，执行，交付。

## 上级
- **Orchestrator:** Synnia
- **交互方式:** HEARTBEAT.md 信号 + Taskwarrior 状态

## 同级 Worker
其他 TaskWorkers：无直接交互，通过 Taskwarrior 竞争任务。

## 任务来源
Taskwarrior 中 tags 包含 {tags} 的 pending 任务。

## 升级路径
若连续拒绝同一类型任务超过 3 次，应通知 Orchestrator 评估是否需要调整策略。
