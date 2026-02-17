# originplanet

the first of its kind

## Typing Speed Increaser

A terminal program to practice typing speed with adaptive difficulty and feedback.

- **Mode 1 (word trainer):** adaptive word rounds with accuracy + WPM feedback.
- **Mode 2 (single-key reaction):** one key at a time (example: `t`, then `r`, etc.) with persistent per-key timing stats.
- Timing begins on your first typed character (not before).
- Windows and POSIX terminals are both supported.

### Run

```bash
python3 typing_speed_increaser.py
```

When started without `--mode`, the program asks you to choose mode 1 or 2.

Optional flags:

- `--mode 1` or `--mode 2`
- `--rounds 8` number of rounds for mode 1
- `--words 18` words per round for mode 1
- `--mode2-drills 40` number of key drills for mode 2
- `--mode2-stats-file my_key_timings.csv` persistent mode 2 timing profile
- `--seed 42` deterministic prompt/key selection


## Windows mini app plan (documented)

1. Build a tiny Windows-native style script app using built-in Windows tooling (HTA + VBScript).
2. Keep UI minimal: one button and a text area next to it.
3. On button press, display "Hello" next to the button.
4. Document implementation and run instructions directly in this repository.

## Windows mini app implementation log

Implemented `windows_hello.hta`:

- Uses the built-in `mshta.exe` host available on standard Windows installs.
- Defines a compact window with simple default Windows-like controls and Segoe UI font.
- Adds a **Press me** button and a neighboring output label.
- Wires the button to a VBScript handler (`SayHello`) that sets the label text to `Hello`.

### How to run (Windows)

1. Copy `windows_hello.hta` to a Windows 10 machine.
2. Double-click the file, or run from cmd:

```bat
mshta.exe windows_hello.hta
```

This opens a small window; pressing the button shows **Hello** next to it.
