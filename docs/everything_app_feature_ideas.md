# OriginPlanet "Everything App" Feature Ideas

A practical backlog of small, composable tools you can ship inside this HTA so the app becomes a personal productivity cockpit.

## 1) Quick Capture
- **Inbox note box**: one text field + save button to append timestamped notes.
- **Scratchpad**: a persistent plaintext area for temporary thoughts.
- **Clipboard history (manual)**: paste current clipboard into a list with one click.

## 2) Day Planning
- **Today board**: 3 sections (`Must`, `Should`, `Could`) with drag-less up/down ordering.
- **Top 3 priorities widget**: lock in the three most important tasks.
- **Time-block planner**: quick start/end entries for your day plan.

## 3) Task / Todo Utilities
- **Recurring tasks**: simple rules like daily/weekly reset.
- **2-minute tasks list**: dedicated micro-task lane to clear quickly.
- **Context tags**: `@home`, `@work`, `@errands`, etc. for filtering.

## 4) Focus + Energy
- **Pomodoro timer**: preset work/break durations and session counter.
- **Deep work streak tracker**: count uninterrupted focus sessions.
- **Break reminders**: periodic prompt to stretch/hydrate.

## 5) Launcher Improvements (current module extension)
- **Categories/folders** for launchers (Work, Personal, Study).
- **Pin to top** for frequently-used launchers.
- **Usage count + last opened** metadata.
- **Search/filter field** for large launcher lists.
- **Import/export launcher entries** to backup/share setups.

## 6) Knowledge + Reference
- **Snippet manager**: reusable templates for replies/commands.
- **Cheat-sheet panel**: keyboard shortcuts, CLI commands, playbooks.
- **Reading queue** with status (`to read`, `reading`, `done`).

## 7) Personal Ops
- **Habit tracker**: daily checkbox streaks.
- **Simple budget log**: quick expense capture to CSV.
- **Meal/health log**: water, sleep, weight snapshots.

## 8) Automation Helpers
- **One-click routines**: open work apps, folders, docs in one action.
- **Template file generator**: create dated note/task/report files.
- **End-of-day shutdown checklist**: review + cleanup shortcuts.

## 9) Review + Reflection
- **Daily review form**: wins, blockers, tomorrow plan.
- **Weekly review summary** generated from entries.
- **Retro prompts** for projects (start/stop/continue).

## 10) Nice-to-have UX foundations
- **Global search** across modules.
- **Keyboard-first controls** (Enter to submit, Esc to cancel).
- **Module toggles** so only useful tools are visible.
- **Single backup file** with version stamp.

---

## Suggested implementation order (low risk -> high leverage)
1. Inbox notes + scratchpad
2. Pomodoro + Top 3 priorities
3. Launcher search + categories
4. Snippet manager
5. Daily review form + weekly summary

This order gives immediate daily value while keeping implementation complexity manageable in HTA/JScript.
