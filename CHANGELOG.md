# Changelog

## [0.1.0] - 2026-03-02

### Added
- 初始版本，基于 chengyu-worker 验证
- Taskwarrior hook 脚本 (tw-hook.py)
- Agent 配置模板 (4个 MD 文件)
- 工作协议: CHECK → FILTER → CLAIM → EXECUTE → VERIFY → DELIVER
- 审计追踪机制: completed_by / rejected_by / started_at / etc.

### Verified
- ✅ 信号驱动架构可行
- ✅ 被动唤醒节省 token
- ✅ 审计字段可追溯
- ✅ 拒绝优于失败原则有效

## [Unreleased]

### Planned
- [ ] coder-worker 示例
- [ ] reviewer-worker 示例
- [ ] Synnia Orchestrator 集成
- [ ] 弹性扩缩容机制
