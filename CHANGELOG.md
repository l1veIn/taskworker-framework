# Changelog

## [0.2.0] - 2026-03-03

### Changed
- **BREAKING**: 移除 HEARTBEAT.md 信号机制，改用 `openclaw agent --message` 直接通知
- Agent 不再需要检查 HEARTBEAT.md，保持为空即可
- Hook 脚本直接调用 `openclaw agent` 发送消息
- 更及时、更可靠的任务通知

### Migration from v1
```bash
# 旧版 (v1): Agent 需要读取 HEARTBEAT.md
# 新版 (v2): Agent 被动接收消息，HEARTBEAT.md 保持为空

# 无需手动迁移，只需更新 hook:
cp bin/tw-hook.py ~/.task/hooks/on-add-notify.py
```

## [0.1.0] - 2026-03-02

### Added
- 初始版本，基于 chengyu-worker 验证
- Taskwarrior hook 脚本 (tw-hook.py)
- Agent 配置模板 (4个 MD 文件)
- 工作协议: CHECK → FILTER → CLAIM → EXECUTE → VERIFY → DELIVER
- 审计追踪机制: completed_by / rejected_by / started_at / etc.
- HEARTBEAT.md 信号机制

### Verified
- ✅ 信号驱动架构可行
- ✅ 被动唤醒节省 token
- ✅ 审计字段可追溯
- ✅ 拒绝优于失败原则有效
