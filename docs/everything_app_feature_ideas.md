# OriginPlanet — Feature Ideas and Implementation Roadmap

This document converts the rough notes in `plans.txt` into a practical, staged plan.

## 1. Cross-platform C Performance Hub

### Objective
Build a small, portable C core that exposes a stable API for local compute tasks and can be called from host applications (HTA, Python, or other runtimes).

### Principles
- Use standard C (C11/C17-level compatibility) with minimal platform-specific code.
- Keep ABI stable and documented.
- Prioritize deterministic behavior and easy embedding.

### Suggested first API surface
- `op_eval_expression(const char* expression, char* out, size_t out_size)`
  - Example input: `"2+3"`
  - Example output: `"5"`
- `op_get_version()`
- `op_last_error()`

### Integration targets
- Windows HTA app via helper executable (initial phase).
- Python wrapper using `ctypes`/`cffi` (secondary phase).

---

## 2. Windows TXT-driven UI Configuration

### Objective
Allow users to configure startup UI parameters through a plain-text config file.

### Candidate config keys
- `window.width`
- `window.height`
- `window.left`
- `window.top`
- `window.caption` (`yes` / `no`)
- `window.border` (`thin` / `thick` / `none`)
- `window.state` (`normal` / `maximized` / `minimized`)

### Behavior requirements
- On startup, parse config and apply supported values.
- Validate values and fall back to defaults on invalid input.
- Show a non-blocking status message when config contains errors.

---

## 3. Demo Action: `2+3` Compute Button

### Objective
Add a simple UI control that calls the C compute hub and displays the result beside the button.

### Minimum acceptance criteria
- Button label clearly indicates compute action (e.g., `Run 2+3 via Hub`).
- Call route succeeds without blocking the UI.
- Result renders in nearby status text.
- Errors render in nearby status text and are logged.

### Implementation phases
1. Temporary local fallback (JScript-side arithmetic) for UI wiring.
2. Replace fallback with C hub process invocation.
3. Replace process invocation with direct bridge only if needed.

---

## 4. Delivery Sequence (recommended)

1. Define C hub project structure + API contract doc.
2. Implement expression prototype (`2+3`).
3. Add config parsing and window setup in HTA startup flow.
4. Add compute demo button in UI.
5. Add export/import updates if any new persisted keys are introduced.

---

## 5. Open questions

- Should config file be global (`%APPDATA%`) or local (next to `.hta`)?
- Should C hub run in-process, out-of-process, or both?
- What is the long-term expression grammar scope (basic arithmetic vs richer parser)?
- How should failures be surfaced to non-technical users?
