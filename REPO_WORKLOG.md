# Repository Worklog

This file is a chronological maintenance log intended for future contributors (or future me).

## 2026-02-18 — Baseline documentation pass

### Goal
Establish missing project documentation that was already referenced by `README.md`, so the repository better explains ongoing work and next implementation steps.

### What was changed
1. Added this `REPO_WORKLOG.md` file to track sessions and decisions.
2. Added `docs/everything_app_feature_ideas.md` as a structured roadmap extracted from `plans.txt` and expanded into implementation-oriented notes.
3. Updated `README.md` to include a dedicated "Maintainer workflow" section describing how to use planning artifacts (`plans.txt`, roadmap doc, and worklog) during development.

### Why this matters
- The README previously referenced docs that did not exist.
- Future iteration is easier when plans are split into:
  - raw scratch notes (`plans.txt`),
  - organized roadmap (`docs/everything_app_feature_ideas.md`),
  - chronological session history (`REPO_WORKLOG.md`).

### Follow-up suggestions
- Implement the first roadmap milestone: TXT-driven window configuration.
- Define a minimal C API contract for external compute calls (starting with arithmetic sample endpoint).
- Add import/export format examples to docs once finalized.


## 2026-02-18 — C hub + HTA integration pass

### Goal
Implement the requested concrete functionality:
- startup TXT config for window behavior,
- a real C helper program,
- and a UI button that runs `2+3` through the C helper and displays the result.

### What was changed
1. Added `c_hub/originplanet_c_hub.c`:
   - CLI contract: `--eval <expression>`.
   - First milestone parser supports strict `integer+integer` and returns the sum to stdout.
2. Added `c_hub/README.md`:
   - build commands for GCC, MinGW, and MSVC,
   - expected runtime behavior.
3. Added `originplanet_config.txt`:
   - startup options for width/height/left/top/caption/border/state.
4. Updated `originplanet.hta`:
   - parses startup config file,
   - applies window size/position from config,
   - surfaces config warnings in dashboard,
   - adds dashboard button `Run 2+3 via C Hub`,
   - executes local helper executable and prints returned result next to button.
5. Updated `README.md`:
   - documents the new integration flow and build placement requirement.

### Constraints and notes
- HTA `CAPTION`/`BORDER` values are primarily application-host settings; runtime override is limited. The app reads these config keys and reports notes when override cannot be fully honored.
- Current C parser scope is intentionally small for the first integration milestone.

### Suggested next iteration
- Add richer expression parsing (`-`, `*`, `/`, parentheses) with explicit error codes.
- Add non-blocking process polling for the C helper call.
- Add a tiny Windows build script that copies the compiled `.exe` beside `originplanet.hta`.
