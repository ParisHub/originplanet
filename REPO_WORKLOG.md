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

## 2026-02-17 — Optimization pass + everything-app feature backlog

### 1) Request interpreted

User requested two outcomes:

1. Produce a list of plausible "everything app" productivity features.
2. Optimize `originplanet.hta` implementation.

Also honored user preference to document changes clearly for future maintenance.

### 2) Feature ideation output

Created a dedicated planning document:

- `docs/everything_app_feature_ideas.md`

What it contains:

- 10 feature domains (capture, planning, tasks, focus, launcher expansion, reference, personal ops, automation, review, UX foundations).
- Practical module ideas designed for HTA/JScript constraints.
- Suggested implementation order to maximize early usefulness.

### 3) HTA optimization changes

File updated:

- `originplanet.hta`

Optimization themes implemented:

- **DOM access cleanup**
  - Added helper `el(id)` to remove repetitive `document.getElementById(...)` calls.
  - Added `setVisible(id, isVisible)` helper to centralize visibility toggling.
- **Render efficiency**
  - `renderLauncherEntries()` now batches row insertion with `DocumentFragment` before appending.
- **Path resolution reuse**
  - Added `pathCandidatesCache` so repeated candidate path generation avoids redundant rebuild work.
- **Launch robustness**
  - `launchPath(...)` now checks path existence (`FolderExists`/`FileExists`) before `explorer` run.
  - Provides status feedback when path is missing.
- **Keyboard UX speed-up**
  - Added Enter-key submit behavior for `appName` and `folderPath` inputs to create entries faster.

### 4) Verification actions

Validation performed locally:

- `git diff --check` for patch cleanliness.
- Reviewed final file diff for behavior consistency and non-regression of existing launcher create/delete/persist flows.

### 5) Notes for future self

If future optimization is needed, likely highest ROI next steps are:

1. Add explicit path-candidate cache invalidation if runtime location can change dynamically.
2. Introduce a small in-memory index for launcher entries if list size becomes large.
3. Move inline JS into a separate `.js` file if HTA packaging constraints allow (improves maintainability/testing).

## 2026-02-18 — Launcher header spacing + button auto-width polish

### 1) Request interpreted

User asked for two UI adjustments in the launcher area shown in screenshot feedback:

1. Move the header action buttons (`Create`, `Delete`, `Home`) a bit to the right so the title/buttons don't look squeezed.
2. Ensure button widths adapt to each button label text instead of looking overly fixed/squeezed.

### 2) Changes made in `originplanet.hta`

#### A) Global button sizing behavior

Updated the shared `button` style to be explicitly content-sized:

- `width: auto;`
- `min-width: 0;`
- `white-space: nowrap;`

Why:

- Keeps all button widths tied to text + padding.
- Prevents inherited/fallback sizing behavior from forcing awkward widths.
- Avoids multiline label wrapping that can make buttons look compressed.

#### B) Launcher list item button sizing

Updated `.launcher-item` (the dynamic app-entry launch buttons) from fixed-ish sizing to text-adaptive sizing:

- Removed `min-width: 220px`
- Added `width: auto`

Why:

- Lets each generated launcher button size naturally by label length.
- Aligns with request that “other buttons” adapt to button text.

#### C) Header button alignment/spacing

Added a dedicated wrapper for launcher header actions:

- New CSS class: `.launcher-header-actions`
  - `display: inline-flex`
  - `align-items: center`
  - `gap: 8px`
  - `margin-left: 12px`

Updated launcher header markup so `Create/Delete/Home` buttons live in this wrapper, placed after the `App Launcher` title.

Why:

- Introduces clear horizontal offset from the title.
- Makes top row read less cramped while preserving current structure and behavior.

### 3) Validation notes

- Performed source inspection after patch to confirm:
  - new wrapper class exists and is used in launcher header markup,
  - button sizing rules are present,
  - `.launcher-item` fixed min-width has been removed.
- This repository has no automated UI test harness for HTA rendering; visual validation should be done in HTA runtime.

## 2026-02-18 — Obfuscated persistence + Clipboard Snippets app

### 1) Request interpreted

Follow-up request had two concrete implementation goals:

1. Replace plain-text entry storage with a less directly readable data format.
2. Add a second in-window app (parallel to App Launcher) for named text snippets where clicking a button copies its content to clipboard, with Create/Delete/Home controls similar to launcher flow.

### 2) Persistence redesign (single obfuscated data file)

#### A) File strategy

- Replaced cleartext `launcher_entries.txt` style persistence with a single application data file:
  - `originplanet_data.opdb`
- Both app launch entries and clipboard snippet entries are saved in this file.

#### B) Data model serialization

- Introduced unified serialization format in-memory before writing:
  - launcher rows serialized as: `L|escapedName|escapedPath`
  - snippet rows serialized as: `S|escapedName|escapedContent`
- Existing escaping rules are reused for separators/newlines/backslashes.

#### C) Obfuscation layer

- Added `obfuscateData(...)` and `deobfuscateData(...)`:
  - payload prefixed with `OPDB1:`
  - body stored as XOR-mixed hex stream using a local key + position-based variation
- Intent:
  - produce a file that is not human-readable at a glance in a text editor,
  - maintain deterministic decode behavior without external dependencies.

#### D) Compatibility behavior

- Decoder falls back gracefully if prefix is missing (treats input as plain text), so older plain payloads don't instantly crash load path.

### 3) New feature: Clipboard Snippets app

#### A) Navigation/UI structure

- Added a second launch button on home panel:
  - `Open Clipboard Snippets`
- Added new panel `snippetPanel` with title, header actions, and list area:
  - `Create`
  - `Delete`/`Done` toggle
  - `Home`

#### B) Create dialog and fields

- Added `snippetCreateDialog` with:
  - `snippetName` (input)
  - `snippetContent` (textarea)
  - `Confirm` / `Cancel`
- Validation requires both name and content.

#### C) Runtime behavior

- Snippet buttons are generated dynamically like launcher rows.
- Clicking a snippet button copies its associated text to clipboard.
- Copy implementation:
  - primary path: `window.clipboardData.setData("Text", content)` (HTA/IE-host friendly)
  - fallback path: hidden textarea + `document.execCommand("copy")`
- Deletion flow mirrors launcher delete mode with confirmation dialogs.

### 4) Shared logic refactor notes

- Replaced launcher-only save/load with shared functions:
  - `saveAllEntries()`
  - `loadAllEntries()`
  - `serializeAllEntries()` / `deserializeAllEntries()`
- Added separate state for launcher and snippet modules:
  - entries arrays
  - next-id counters
  - delete-mode flags
  - status outputs

### 5) Validation notes

- Source-level validation:
  - checked that both panels render and use independent controls/status lines,
  - verified save/load now routes through unified obfuscated persistence path,
  - verified new clipboard-copy flow wiring.
- Further runtime validation recommended in HTA host on Windows to verify clipboard behavior in target environment.

## 2026-02-18 — Data ownership note + TXT import/export module

### 1) Request interpreted

Follow-up requirements were:

1. Add an explicit note that `.opdb` is user-specific and should not be treated as a shared hand-edited file.
2. Keep existing `.opdb` handling behavior unchanged (so app updates remain distributable while each colleague keeps their local `.opdb`).
3. Add another module to export/import between `.opdb` and a human-readable `.txt` format.

### 2) Scope and non-change guarantee

I intentionally **did not alter** the underlying `.opdb` path/discovery/write mechanics (`getDataFilePathCandidates`, `getDataFilePath`, `saveAllEntries`, `loadAllEntries`).

Result:

- each user's `.opdb` still lives next to their app copy,
- app updates can be distributed independently,
- existing local data compatibility behavior remains intact.

### 3) New module: Data Import / Export

#### A) Navigation and panel

- Added a home button: `Open Data Import / Export`.
- Added new panel `dataToolsPanel` containing:
  - a maintenance note about `.opdb` ownership/use,
  - one path input for readable text file target/source,
  - `Export to TXT` and `Import from TXT` actions,
  - status line (`dataToolsStatus`).

#### B) Export behavior

- New function: `exportDataToTxt()`.
- Output includes comment header lines plus typed records:
  - `L|escapedName|escapedPath`
  - `S|escapedName|escapedContent`
- Export file is intentionally readable and editable.

#### C) Import behavior

- New function: `importDataFromTxt()`.
- Reads selected `.txt`, ignores blank/comment lines (`#...`), parses typed record lines, then:
  - rehydrates launcher/snippet in-memory state,
  - re-renders both modules,
  - persists imported state back into `.opdb` via existing save path.

#### D) Default path helper

- New helper: `getDefaultTxtPath()`:
  - derives a nearby `.txt` path from active `.opdb` path where possible,
  - falls back to `originplanet_export.txt`.

### 4) Explicit user-specific note placement

Added on-screen note in Data Import / Export panel:

- `.opdb` is user-specific, should stay beside each user's app,
- avoid sharing/manual editing of `.opdb`,
- use export/import `.txt` for readable transfer.

### 5) Validation notes

- Verified new panel wiring and function references through source inspection.
- Confirmed `.opdb` core file handling functions were left intact.
- Recommended runtime HTA validation on Windows for final operational confirmation in target host.

## 2026-02-18 — Optimization / cleanup pass before closing task

### 1) Request interpreted

Final request was to do a broad optimization/general-improvement sweep before closing the task.

### 2) Optimization focus areas (without changing product behavior)

I targeted low-risk maintainability and robustness improvements while preserving established UX and `.opdb` behavior.

#### A) Panel navigation de-duplication

- Added `showOnlyPanel(panelId)` with centralized `panelIds` list.
- Replaced repeated multi-line `setVisible(...)` sequences in:
  - `openLauncher()`
  - `openSnippetPanel()`
  - `openDataToolsPanel()`
  - `goHome()`

Impact:

- less duplicated UI-state code,
- reduced chance of future panel-state drift bugs.

#### B) Shared utility helpers for repeated logic

- Added `findEntryIndexById(entries, entryId)` and reused it in both delete handlers.
- Added `bindEnterToAction(inputId, action)` to unify Enter-key wiring in `window.onload`.
- Added `renderAllEntryLists()` for two-panel re-render operations.
- Added `setAllStatuses(message)` for shared persistence error messaging.

Impact:

- shorter, easier-to-audit functions,
- fewer repeated loops/boilerplate blocks.

#### C) Import/export robustness improvements

- `importDataFromTxt()` now rejects imports with zero parsed records instead of silently overwriting with empty state.
- Export/import status messages now include record counts for clearer operator feedback.

Impact:

- safer data operations,
- clearer maintenance diagnostics.

### 3) Behavioral compatibility note

- No changes were made to `.opdb` path discovery or persistence architecture:
  - `getDataFilePathCandidates`
  - `getDataFilePath`
  - `saveAllEntries`
  - `loadAllEntries`

So per-user local `.opdb` behavior remains as designed.

### 4) Validation notes

- Ran patch sanity and source checks after refactor.
- Captured updated UI screenshot for the Data Import / Export module to confirm navigational wiring still works.

## 2026-02-18 — Trace cleanup pass for removed/legacy references

### 1) Request interpreted

User asked for a repository cleanup pass to remove traces of old components that are no longer active, with explicit documentation of actions for future maintenance.

### 2) Audit performed

I ran a targeted text-reference search against current project files to identify lingering stale references to removed files/tools and older names.

Scope searched:

- `README.md`
- `REPO_WORKLOG.md`
- `docs/`
- `originplanet.hta`

Reference patterns checked included:

- removed typing utility names
- old HTA filename
- previously deleted binary/html artifacts
- moved legacy source filenames

### 3) Cleanup decision

Historical references in `REPO_WORKLOG.md` were intentionally retained because they are part of the chronological audit trail.

Action taken focused on user-facing repository overview text in `README.md`, removing "status notes" phrasing that centered deleted components, and replacing it with an explicit **current layout** section that reflects only the active/relevant structure.

### 4) File edits

- `README.md`
  - Replaced old cleanup-status bullets with a stable "Current repository layout" section.
  - The new section points maintainers directly to active app path (`originplanet.hta`), docs/data, archived experiments, and worklog.

- `REPO_WORKLOG.md`
  - Added this entry to document request interpretation, audit method, rationale, and exact scope of cleanup.

### 5) Validation notes

- Verified expected modifications via line-numbered file inspection and `git diff`.
- Confirmed no unintended file changes outside documentation cleanup scope.

## 2026-02-18 — Terminology pivot from apps/modules to extensions

### 1) Request interpreted

Applied a product-language decision to stop referring to the launcher/snippet features as apps/modules in user-facing text and instead use **extensions** terminology.

User-provided target examples:
- `path opener extension` (for previous `App Launcher` concept)
- `pasting extension` (for previous clipboard snippets concept)

### 2) Implementation changes made

Updated user-facing labels in `originplanet.hta`:
- Home actions renamed to:
  - `Open Path Opener Extension`
  - `Open Pasting Extension`
- Launcher panel title renamed from `App Launcher` -> `Path Opener Extension`
- Launcher creation fields renamed:
  - `App Name` -> `Path Name`
  - `Folder Path` -> `Path Target`
- Snippet panel title renamed from `Clipboard Snippets` -> `Pasting Extension`
- Snippet creation fields renamed:
  - `Snippet Name` -> `Pasting Extension Name`
  - `Snippet Content` -> `Pasting Content`
- Snippet/pasting status and helper copy updated to extension language (error, empty state, tooltip, success/failure copy messages).

Updated docs to match terminology:
- `README.md`
  - `Quick launcher dashboard` -> `Path opener extension`
  - `Personal clipboard snippets tool` -> `Pasting extension`
- `docs/everything_app_feature_ideas.md`
  - `module extension` phrasing -> `extension enhancement`
  - `Global search across modules` -> `...across extensions`
  - `Module toggles` -> `Extension toggles`

### 3) Notes for future edits

- Internal variable and function names in script (`openLauncher`, `snippetEntries`, etc.) were intentionally not renamed in this pass to keep behavior risk low.
- If a future cleanup wants full conceptual consistency, do a separate refactor pass for internal identifiers and persistence record prefixes.
- This pass focuses strictly on outward terminology (UI + docs), not data schema changes.

## 2026-02-18 — README full rework as product-style app introduction

### 1) Request interpreted

User requested a complete README redesign so the repository presents itself as a focused OriginPlanet Windows app (instead of a mixed/legacy project narrative), with a polished introduction style.

### 2) Rewrite strategy used

I replaced the previous README wholesale with a product-first structure that:

- starts with a concise value proposition,
- highlights the three current in-app capabilities,
- adds an at-a-glance user flow,
- keeps Windows run instructions easy to find,
- lists only app-relevant project files,
- and closes with a short product philosophy section.

This keeps onboarding fast for new users while still being useful for future maintenance.

### 3) Content decisions

- Removed historical/cleanup framing and “mini app plan” scaffolding from the front page.
- Removed emphasis on archived/non-app parts of repo from primary presentation.
- Aligned terminology with current naming decision (`Path Opener Extension`, `Pasting Extension`).
- Kept technical details intentionally lightweight and practical (HTA stack + single-file distribution note).

### 4) Files changed

- `README.md`
  - Fully rewritten for a clean, product-oriented introduction and usage guide.

- `REPO_WORKLOG.md`
  - Added this entry to record rationale and exact scope of the README rework.

### 5) Validation notes

- Reviewed the rewritten README in plain text to confirm section order and readability.
- Confirmed naming consistency with the current extension terminology.
- Confirmed no code-path/runtime behavior changes were introduced in this pass.

## 2026-02-18 — Dynamic HTA window resizing support

### 1) Request interpreted

Implemented dynamic window resizing behavior so OriginPlanet is no longer fixed to a dialog-style frame and can adjust to UI state changes.

### 2) What changed in `originplanet.hta`

- Enabled user-resizable HTA frame:
  - `BORDER="dialog"` -> `BORDER="thick"`
  - Added `RESIZE="yes"`
- Added a new helper: `syncWindowToContent()`
  - Computes target dimensions from current document body content (`scrollWidth` / `scrollHeight`).
  - Adds small frame paddings for non-client area.
  - Clamps to practical min/max bounds:
    - min: `700 x 480`
    - max: screen available size fallback (`1600 x 1200`)
  - Calls `window.resizeTo(...)` when available.
- Hooked dynamic resize helper to UI transitions:
  - After panel changes in `showOnlyPanel(...)`
  - After create-dialog open/close in launcher panel
  - After create-dialog open/close in pasting panel
  - On app load (`window.onload`) after initial data hydration

### 3) Why this approach

- HTA-level resizing (`RESIZE="yes"`) allows manual drag resizing by the user.
- Content-sync resize avoids clipped UI when switching between compact/expanded views.
- Min/max constraints prevent tiny unusable windows or oversized growth.
- Kept implementation additive (small helper + call sites) to minimize regression risk.

### 4) Validation done

- Ran a focused source check for resize-related edits and call sites.
- Ran `git diff --check` to confirm patch hygiene.
- Captured a browser-rendered screenshot artifact of the updated UI for visual verification.

### 5) Maintenance notes for future me

- If users report the window "fighting" their manual size, consider making `syncWindowToContent()` opt-in only for panel transitions and not dialog toggles.
- If additional panels are added, they will automatically trigger resize when shown via `showOnlyPanel(...)`.
- If minimum size needs to be configurable, lift constants into top-level vars near other app state config.

## 2026-02-18 — Resizing flicker follow-up + scrollable extension button lists

### 1) User feedback addressed

Follow-up issues reported after the first dynamic resize pass:

1. Vertical-only manual resizing showed flicker.
2. Extension button lists were cut off when window height became small.

### 2) Implementation adjustments

#### A) Reduced resize contention during vertical manual resizing

- Kept the HTA window user-resizable (`BORDER="thick"` + `RESIZE="yes"` unchanged).
- Updated `syncWindowToContent()` so it no longer force-recomputes height from content on each call.
  - Width still adapts to content (`body.scrollWidth + padding`).
  - Height now respects current window height (`window.outerHeight`) with min/max clamping.
- Removed `syncWindowToContent()` calls from dialog show/hide handlers to avoid unnecessary resize nudges during rapid UI interactions.

Why this helps:
- The prior behavior was more likely to fight user-driven vertical adjustments by recomputing height from content snapshots.
- Respecting current height avoids that tug-of-war while preserving dynamic width behavior and initial layout sizing.

#### B) Made extension button lists scrollable

- Updated list container CSS for both:
  - `#launcherButtons`
  - `#snippetButtons`
- Added:
  - `overflow-y: auto;`
  - `overflow-x: hidden;`
  - `padding-right: 4px;`
- Added `updateScrollableListHeights()` helper to compute a practical `maxHeight` based on viewport height with a floor value.
- Invoked `updateScrollableListHeights()`:
  - from `syncWindowToContent()`
  - on native `window.onresize`

Why this helps:
- When window height is reduced, the button areas now get their own vertical scroll instead of clipping content.
- The layout remains usable even in constrained window sizes.

### 3) Validation performed

- Ran source inspection focused on resize logic and scroll container behavior.
- Ran `git diff --check` for patch hygiene.
- Attempted screenshot capture via browser tool; current container/browser path to the local app remains unavailable in this environment.

### 4) Maintenance notes for future me

- If product intent later requires auto-height growth again, reintroduce it behind a feature flag and disable it while user is actively resizing.
- If panel header/content structure changes significantly, revisit the `availableHeight - 260` offset in `updateScrollableListHeights()`.
- If UI must support very tiny windows, lower the list `minimumHeight` from `140` after usability test.
