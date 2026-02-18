# OriginPlanet for Windows

> A compact, native-feeling Windows utility built with HTA (`mshta.exe`) for fast everyday actions.

OriginPlanet is a single-file desktop helper focused on practical workflows:

- open frequently used paths quickly,
- copy reusable text in one click,
- and move data in and out through a readable transfer format.

---

## ✨ What OriginPlanet includes

### 1) Path Opener Extension
Create named buttons that open folders/locations directly from one panel.

**Good for:** workspaces, project folders, docs hubs, shared drives.

### 2) Pasting Extension
Save reusable text and copy it to clipboard instantly from named entries.

**Good for:** message templates, email snippets, signatures, status updates.

### 3) Data Import / Export
Export your entries into a human-readable `.txt` format and import them back later.

**Good for:** backup, migration, and manual inspection without editing internal storage directly.

---

## 🧭 User flow at a glance

1. Launch `originplanet.hta`.
2. From Home, open either extension panel.
3. Add entries with **Create**.
4. Click an entry to run/copy.
5. Use **Delete** mode for cleanup.
6. Use **Data Import / Export** to back up or restore.

---

## 🚀 Run on Windows

OriginPlanet uses built-in Windows HTA hosting. No additional runtime is required.

### Option A: double click
- Double-click `originplanet.hta` in File Explorer.

### Option B: command line
```bat
mshta.exe originplanet.hta
```

---

## 🗂️ Main project files

- `originplanet.hta` — complete app UI + behavior.
- `README.md` — product introduction and run guide.
- `REPO_WORKLOG.md` — chronological implementation notes for future maintenance.
- `docs/everything_app_feature_ideas.md` — future roadmap ideas for OriginPlanet.

---

## 🛠️ Technical notes

- Stack: **HTA + HTML/CSS + JScript + ActiveX integrations**.
- Distribution: **single-file app** (`originplanet.hta`) suitable for lightweight personal/internal tooling.
- Persistence: entries are stored locally for reuse between launches.

---

## 📌 Philosophy

OriginPlanet is intentionally small and direct:

- low ceremony,
- fast interaction,
- practical day-to-day value.

If a workflow needs to happen repeatedly, it should be one click away.
