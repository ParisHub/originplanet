# Repo Worklog

## 2026-02-17 — Repository overview and cleanup

### 1) Read-only overview (no file edits during this phase)

Observed top-level repository contents before cleanup:

- `README.md`
- `typing_speed_increaser.py`
- `main.c`
- `helloworld.lisp`
- `windows_hello.hta`
- `booklist.csv`
- `games.txt`
- `hanzi von liste mit atr.txt`
- `hk`
- `hk.exe`
- `main.html`
- `__pycache__/`

High-level purpose from `README.md`:

- Main feature is `typing_speed_increaser.py`, a terminal typing trainer with:
  - adaptive word rounds (mode 1)
  - single-key reaction drills with persistent per-key stats (mode 2)
- Also contains a small Windows HTA app (`windows_hello.hta`) that shows “Hello” when clicking a button.

### 2) Cleanup actions requested

Requested actions:

1. Delete `__pycache__/`
2. Move `.csv` and `.txt` files into a `docs/` folder
3. Delete `hk`, `hk.exe`, `main.html`, and `typing_speed_increaser.pc`

Execution notes:

- Created `docs/`
- Moved:
  - `booklist.csv` -> `docs/booklist.csv`
  - `games.txt` -> `docs/games.txt`
  - `hanzi von liste mit atr.txt` -> `docs/hanzi von liste mit atr.txt`
- Deleted:
  - `__pycache__/` directory
  - `hk`
  - `hk.exe`
  - `main.html`
- `typing_speed_increaser.pc` was not present, so no file removed for that path.

### 3) Post-cleanup top-level layout

- `README.md`
- `REPO_WORKLOG.md`
- `docs/`
- `typing_speed_increaser.py`
- `main.c`
- `helloworld.lisp`
- `windows_hello.hta`

`docs/` now contains all discovered `.csv` and `.txt` files.
