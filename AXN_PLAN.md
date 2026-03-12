# AXN Plan: Fix PyfficeDocument Inheritance

## Project: Fix PyfficeDocument Inheritance
- **Stream**: pyffice
- **Priority**: high
- **Status**: pending

## Goal
Update 6 Pyffice classes to properly subclass `PyfficeDocument` as identified in STATE.md

## Classes to Fix

### High Priority (Must Change to PyfficeDocument)

| # | Class | File | Current Base | Required Change |
|---|-------|------|--------------|-----------------|
| 1 | PyfficeGanttChart | calendars/gantt.py | object | → PyfficeDocument |
| 2 | PyfficeHTML | items/text.py | PyfficeText→PyfficeUnit | → PyfficeDocument |
| 3 | PyfficeSlideShow | presentation/presentation.py | object | → PyfficeDocument |
| 4 | PyfficeAlarm | workflows/alarms.py | PyfficeEvent→PyfficeUnit | → PyfficeDocument |
| 5 | PyfficeDatabaseConnection | databases/databases.py | sonql.Doc | → PyfficeDocument |
| 6 | PyfficeURL | web/url.py | PyfficeUnit | → PyfficeDocument |

## Tasks

### Task 1: Fix PyfficeGanttChart
- [ ] Read `calendars/gantt.py`
- [ ] Change inheritance from `object` to `PyfficeDocument`
- [ ] Verify no import errors

### Task 2: Fix PyfficeHTML
- [ ] Read `items/text.py`
- [ ] Change inheritance from `PyfficeText` to `PyfficeDocument`

### Task 3: Fix PyfficeSlideShow
- [ ] Read `presentation/presentation.py`
- [ ] Change inheritance from `object` to `PyfficeDocument`

### Task 4: Fix PyfficeAlarm
- [ ] Read `workflows/alarms.py`
- [ ] Change inheritance from `PyfficeEvent` to `PyfficeDocument`

### Task 5: Fix PyfficeDatabaseConnection
- [ ] Read `databases/databases.py`
- [ ] Change inheritance from `sonql.Doc` to `PyfficeDocument`

### Task 6: Fix PyfficeURL
- [ ] Read `web/url.py`
- [ ] Change inheritance from `PyfficeUnit` to `PyfficeDocument`

### Task 7: Final Verification
- [ ] Run import test on all changed files
- [ ] Update STATE.md with fixes
- [ ] Commit and push to GitVein orin-ws
