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

## 2026-02-17 — Follow-up cleanup after review feedback

### 1) Request implemented

Follow-up request was to:

1. Delete the typing Python program (`typing_speed_increaser.py`).
2. Move `.c` and `.lisp` files into a folder named `bad programs`.

### 2) Execution details

Actions performed:

- Created folder: `bad programs/`
- Moved:
  - `main.c` -> `bad programs/main.c`
  - `helloworld.lisp` -> `bad programs/helloworld.lisp`
- Deleted:
  - `typing_speed_increaser.py`

Additional maintenance for future consistency:

- Updated `README.md` to remove stale run instructions for the deleted Python typing tool.
- Added a short “Repository status notes” section describing the cleanup outcome.

### 3) Post-change repository shape

Top-level now focuses on:

- `windows_hello.hta` as the active runnable app in this repo
- `docs/` for text/csv data files
- `bad programs/` for archived `.c`/`.lisp` experiments
- `REPO_WORKLOG.md` as the running maintenance log

## 2026-02-17 — HTA app launcher feature pass

### 1) Request interpreted

Implemented an in-window App Launcher flow in `windows_hello.hta` with these constraints:

- Keep using the first HTA window (no second window created).
- Do **not** embed launcher controls into the existing home/start content directly.
- Add a button on the initial panel that opens the launcher view.
- Inside launcher view, add a `Create` action that opens a small context dialog area.
- Dialog accepts:
  - display name
  - folder path
- Confirm action adds a launcher button in the launcher view.

### 2) UI and behavior changes made

- Reworked HTA page into two panels:
  - `homePanel`: original hello interaction + new `Open App Launcher` button.
  - `launcherPanel`: hidden by default and shown only after opening launcher.
- Added `Create` button inside launcher panel.
- Added inline dialog (`createDialog`) with:
  - `App Name` field
  - `Folder Path` field
  - `Confirm` and `Cancel` actions
  - inline validation error area
- Implemented button creation behavior:
  - trims inputs
  - validates both fields are non-empty
  - appends a new launcher button to the launcher button area
  - stores folder path as metadata/title for reference
- Implemented launch behavior for created buttons:
  - attempts to open folder path through `WScript.Shell` + `explorer`
  - shows alert if launching fails

### 3) Internal implementation notes for future edits

- Script language changed to JavaScript (`<script language="javascript">`) to simplify dynamic DOM creation and event handlers.
- Existing hello behavior preserved via `sayHello()`.
- Dialog is not a separate OS window; it is a contextual inline container toggled in the launcher panel.
- Entry persistence is currently in-memory only (session-scoped). If persistence is needed later, consider:
  - writing to local file through `Scripting.FileSystemObject`, or
  - storing in registry/profile-backed storage depending on HTA deployment constraints.

### 4) Validation performed

- Confirmed file edit contents via local file inspection and diff review.
- No automated runtime test harness exists in this repository for HTA UI; behavior validation is based on deterministic DOM/script logic in source.

## 2026-02-17 — Launcher entry deletion + persistence pass

### 1) Request interpreted

Follow-up implementation goals:

- Add a way to delete launcher entries from the in-window launcher UI.
- Make launcher entries persistent across app restarts.
- Keep the design in the same HTA window and maintain the existing create flow.

### 2) Persistence design decision

Chose a **separate data file** in the same folder as the HTA:

- File name: `launcher_entries.txt`
- Format: one line per entry, `escapedName|escapedFolderPath`
- Why this approach:
  - keeps data separate from executable UI code
  - avoids self-modifying `.hta` file edits (safer/cleaner maintenance)
  - straightforward file IO in HTA via `Scripting.FileSystemObject`

### 3) Implementation details in `windows_hello.hta`

#### Data model + lifecycle

- Added in-memory state:
  - `launcherEntries` array
  - `nextEntryId` counter
- Added startup loading:
  - `window.onload` calls `loadLauncherEntries()`
  - existing entries are read from `launcher_entries.txt` and rendered immediately

#### Entry creation and rendering

- Reworked creation flow so it appends objects to `launcherEntries` (instead of creating one-off DOM buttons directly).
- Added `renderLauncherEntries()` to rebuild launcher UI from state.
- Added status line (`launcherStatus`) for user-facing feedback.

#### Deletion support

- Each launcher row now renders:
  - launch button (entry name)
  - `Delete` button
- Added `removeLauncherEntry(entryId)`:
  - confirms delete with `confirm(...)`
  - removes entry from in-memory array
  - re-renders list
  - persists updated file

#### Disk persistence helpers

- Added `getDataFilePath()` to resolve `launcher_entries.txt` next to the `.hta` file.
- Added `saveLauncherEntries()` and `loadLauncherEntries()` using `Scripting.FileSystemObject`.
- Added value encoding helpers:
  - `escapeValue(...)`
  - `unescapeValue(...)`
- Added path normalization helper:
  - `decodePath(...)` to convert HTA URL path into Windows path format for FileSystemObject operations.

### 4) UX updates

- Launcher entries are now rendered as row items with explicit delete affordance.
- Added `launcherStatus` text area to surface load/save/add/delete feedback.
- Empty state now displays: “No entries yet. Click Create to add one.”

### 5) Validation performed

- Verified source-level correctness by reviewing full updated HTA file and checking key function wiring:
  - startup load
  - create -> render -> save chain
  - delete -> render -> save chain
- Performed `git diff --check` to ensure clean formatting.
- There is no automated HTA runtime test harness in this repository; runtime behavior still needs manual validation inside an HTA-capable Windows environment.

## 2026-02-17 — Persistence reload fix + HTA rename to `originplanet.hta`

### 1) Request interpreted

Addressed two follow-up issues:

1. Existing `launcher_entries.txt` data was not reliably reloading after closing/reopening the HTA.
2. Rename app file from `windows_hello.hta` to `originplanet.hta`.

### 2) Root-cause notes for reload issue

Likely failure points in the previous implementation:

- Data-file path resolution depended on `window.location.pathname` assumptions that are brittle in HTA host path formats.
- Line parsing used `indexOf("|")`, which can split incorrectly when escaped pipes are present.

### 3) Fixes implemented in `originplanet.hta`

- Renamed file via git move:
  - `windows_hello.hta` -> `originplanet.hta`
- Hardened data path resolution:
  - Added `getCurrentFilePath()` based on `window.location.href`.
  - Added `decodeUriValue(...)` with fallback to `unescape(...)`.
  - Added fallback directory resolver `getCurrentDirectoryFallback()` via `WScript.Shell.CurrentDirectory`.
  - Updated `getDataFilePath()` to use the robust path helpers.
- Hardened entry line parsing:
  - Replaced naive delimiter split with `splitEscapedPair(...)` that locates first **unescaped** pipe.
  - Updated loader to consume parsed `{ left, right }` pair.

### 4) Documentation updates

- Updated `README.md` run instructions and implementation references to use `originplanet.hta`.

### 5) Validation performed

- Verified modified file paths and helper wiring through source inspection.
- Ran `git diff --check` to ensure clean patch formatting.
- Verified expected file rename is tracked by Git.

## 2026-02-17 — Home navigation + Apple-style delete mode

### 1) Request interpreted

Follow-up UX changes requested:

1. Add a `Home` button from launcher view back to the home/start screen.
2. Replace always-visible per-entry delete controls with a single top toggle button (Apple-style edit/delete mode) that reveals/hides delete buttons for all entries.

### 2) Implementation approach

- Introduce global `deleteMode` state (default `false`).
- Add `Home` button in launcher header row.
- Add `Delete` toggle button in launcher header row:
  - toggles `deleteMode`
  - updates button label to `Done` while active
  - causes re-render so per-entry delete buttons are conditionally shown/hidden.
- Keep deletion confirmation logic as-is once delete mode is active and user taps an item delete control.

### 3) Additional maintenance while editing

- Removed duplicate `var folderPath` declaration in `getDataFilePath()` to keep function clean and reduce future confusion.

### 4) Validation plan

- Confirm source wiring for:
  - launcher -> home navigation
  - delete toggle label/state transitions
  - conditional delete button rendering
- Run `git diff --check`.
- Attempt screenshot capture with browser tool (expected limitations in this environment may still apply).

## 2026-02-17 — Reload reliability hotfix after user retest

### 1) Problem report

User retest indicated persisted launcher entries still were not reloading after reopening the HTA.

### 2) Additional hardening implemented

Updated persistence path handling to resolve common HTA path inconsistencies across runtime contexts:

- Added `activeDataFilePath` state so save operations continue using the same discovered file path that load resolved.
- Added candidate-based path discovery (`getDataFilePathCandidates()`):
  1. `window.location.pathname`-derived file path
  2. `window.location.href`-derived file path
  3. `WScript.Shell.CurrentDirectory` fallback
- Added candidate deduplication helper (`pushUnique(...)`).
- Updated loader to choose the first existing candidate path and remember it as active path.
- Updated saver to prefer `activeDataFilePath` when writing updates.

### 3) Why this should fix the observed behavior

The previous single-path strategy could miss the real startup location depending on HTA host/path format. Candidate probing + remembered active path makes load/save converge on the same `launcher_entries.txt` location more consistently across reopen cycles.

### 4) Validation performed

- Re-checked script syntax by extracting the embedded JavaScript and parsing with Node.
- Ran `git diff --check` to ensure patch quality.
- Confirmed expected files changed (`originplanet.hta`, `REPO_WORKLOG.md`).

## 2026-02-17 — Visual polish pass ("make it really pretty")

### 1) Request interpreted

User requested a strong visual polish of the HTA app while keeping existing launcher functionality.

### 2) Styling overhaul applied

Performed a full UI refresh focused on a modern soft-card look:

- Reworked page shell:
  - gradient app background
  - larger title typography and descriptive subtitle
- Updated panel surface:
  - rounded corners
  - softer border color
  - deeper shadow and light glass-like appearance
- Modernized button system:
  - shared rounded shape, gradient fill, hover shadow, pressed state
  - semantic button variants:
    - `.primary`
    - `.ghost`
    - `.danger`
- Improved launcher entry visuals:
  - each entry row rendered as a subtle card row
  - launcher buttons styled to look like tappable tiles
  - delete buttons styled with danger treatment while preserving delete-mode behavior
- Improved form UX styling:
  - uppercase labels with stronger hierarchy
  - rounded, cleaner inputs
  - refined create dialog panel look
- Refined feedback badges/text:
  - `#msg` now rendered as a pill-style success indicator
  - launcher status text color/spacing adjusted

### 3) Markup/class updates (non-functional)

- Updated heading text to `OriginPlanet Launcher` and added subtitle.
- Added button utility classes in markup for visual consistency.
- Replaced plain launcher section label with `.panel-title`.

### 4) Functional safety

- JavaScript launcher behavior intentionally kept intact (create, delete mode, home navigation, persistence logic).
- Styling changes were scoped to CSS + class attributes to avoid behavior regressions.

### 5) Validation performed

- Parsed embedded JavaScript with Node to ensure no syntax regressions.
- Ran `git diff --check` for patch formatting.
- Attempted screenshot capture through browser tool (environment still blocks local file path access).
