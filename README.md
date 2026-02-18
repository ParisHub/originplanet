# originplanet

the first of its kind

## Current repository layout

- `originplanet.hta` — primary HTA application entry point.
- `docs/` — reference notes and source data files (`.md`, `.txt`, `.csv`).
- `bad programs/` — archived experimental code kept out of the main app path.
- `REPO_WORKLOG.md` — chronological implementation and maintenance log.

## Windows mini app plan (documented)

1. Build a tiny Windows-native style script app using built-in Windows tooling (HTA + VBScript).
2. Keep UI minimal: one button and a text area next to it.
3. On button press, display "Hello" next to the button.
4. Document implementation and run instructions directly in this repository.

## Windows mini app implementation log

Implemented `originplanet.hta`:

- Uses the built-in `mshta.exe` host available on standard Windows installs.
- Defines a compact window with simple default Windows-like controls and Segoe UI font.
- Adds a **Press me** button and a neighboring output label.
- Wires the button to a script handler that sets the label text to `Hello`.

### How to run (Windows)

1. Copy `originplanet.hta` to a Windows 10 machine.
2. Double-click the file, or run from cmd:

```bat
mshta.exe originplanet.hta
```

This opens a small window; pressing the button shows **Hello** next to it.


## Follow-up plan (documented)

1. Capture practical ideas the HTA mini app can grow into.
2. Keep ideas realistic for built-in Windows scripting (HTA + VBScript/JScript).
3. Document implementation options so the app can evolve without extra frameworks.

## Cool things you can realize with this HTA app

Starting from this tiny button app, you can build surprisingly useful Windows tools:

1. **Quick launcher dashboard**
   - Add buttons to open favorite apps, folders, and websites.
   - Example: open Notepad, Downloads folder, and a work URL from one window.

2. **Personal clipboard snippets tool**
   - Keep reusable text snippets (email replies, signatures, templates).
   - Click a button to copy a snippet into the clipboard.

3. **Mini task tracker (local file based)**
   - Add task input + list and save to a local `.txt` or `.csv` file.
   - Load tasks automatically when app starts.

4. **System helper panel**
   - Show quick system info (username, computer name, date/time, network status).
   - Add one-click actions like clearing temp folders or opening Device Manager.

5. **Study helper / flashcard app**
   - Read questions from a text file and reveal answers on button press.
   - Great for language learning or interview prep.

6. **Simple timer + Pomodoro window**
   - Start/stop timer with visual countdown.
   - Add desktop popup reminders using built-in script commands.

7. **File organizer assistant**
   - Buttons to move files by extension (e.g., downloads to Images/PDFs/Docs).
   - Useful for routine cleanup tasks.

8. **Local notes panel**
   - Small always-on-top note window for quick thoughts.
   - Save and reload notes between sessions.

9. **Data-entry form for CSV**
   - Create fields (name, date, note) and append entries to CSV.
   - Later open CSV in Excel for analysis.

10. **Command palette for your own workflows**
    - One input box where typing short commands triggers scripted actions.
    - Example: `backup`, `open mail`, `today report`.

### Why this is powerful

- HTA runs with built-in Windows components (`mshta.exe`)—no external runtime needed.
- You can combine HTML UI + VBScript/JScript + Windows shell commands.
- Perfect for lightweight internal tools and personal automation.
