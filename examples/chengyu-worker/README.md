# Chengyu Worker 示例

已验证的 TaskWorker 实现。

## 功能
成语接龙游戏 Agent。

## 测试记录
- 场景1: 正常四字成语 ✅
- 场景2: 非四字拒绝 ✅
- 场景3: 多任务连续处理 ✅
- 场景4: 无任务空闲 ✅

## 使用

```bash
# 创建任务
task add "成语接龙：龙马精神" project:game tags:chengyu,game

# Hook 自动通知 chengyu-1
# Agent 执行后输出: 马到成功
```
