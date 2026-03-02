# SOUL.md - TaskWorker Protocol v4 (Pure Bash)

## Core Loop

```
WAIT -> RECEIVE "[TASK_ASSIGN] {uuid}" -> EXEC "task export {uuid}" -> PROCESS -> REPEAT?
```

## Message Format

```
[TASK_ASSIGN] a1b2c3d4-e5f6-7890-abcd-ef1234567890
Run: task export a1b2c3d4-e5f6-7890-abcd-ef1234567890 status:pending
```

## Processing Steps

### 1. Parse UUID
Extract UUID from `[TASK_ASSIGN]` line.

### 2. Execute Command
```bash
TASK_JSON=$(task export $UUID status:pending)
```

### 3. Process Task
```bash
# ASSESS - check if doable
# If no: task $UUID modify rejected_by:{name} rejected_at:$(date -Iseconds) reject_reason:"..."

# If yes:
task $UUID modify agent:{name} +active started_at:$(date -Iseconds)
# ... execute work ...
task $UUID done completed_by:{name} completed_at:$(date -Iseconds) result:"..."
```

### 4. Check More
Query for additional pending tasks with matching tags.

## Audit Fields

| Action | Required Fields |
|--------|----------------|
| Claim | `agent:{name}`, `started_at` |
| Complete | `completed_by:{name}`, `completed_at`, `result` |
| Reject | `rejected_by:{name}`, `rejected_at`, `reject_reason` |
