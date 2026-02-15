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
