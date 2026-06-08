# vim-masterpiece

A terminal game for learning Vim. 30 levels, each teaching one or more motions through a small puzzle map. Built with [Textual](https://textual.textualize.io/) and Python.

Runs on Windows, macOS, and Linux.

---

## Why

I kept forgetting Vim motions because I only used them when editing. This forces repetition in a context where getting it wrong has a visible cost — you move the wrong way, you take longer, you see your stroke count climb. The game loop is minimal: reach the exit in as few keystrokes as possible.

---

## Install

```bash
pipx install vim-masterpiece
vim-masterpiece
```

Or with uv:

```bash
uv tool install vim-masterpiece
```

Requires Python 3.10+.

**Dev install:**

```bash
git clone https://github.com/ExPl0iT-29/learn-vim.git
cd learn-vim
pip install -e .
vim-masterpiece
```

---

## How it works

Levels 1–10 are hand-written maps that introduce one concept each. Levels 11–30 are procedurally generated with increasing density of enemies, locks, and puzzle elements.

Each level has a par keystroke count. Your best scores are stored in your OS data directory (`~/.local/share/vim-masterpiece` on Linux, `%LOCALAPPDATA%\vim-masterpiece` on Windows).

The Vim parser is a small state machine that handles counts (`3j`), operators (`d`), registers (`"ay`), and mode switching. It does not use any Vim library — the motions that matter for the game are implemented directly.

---

## Levels

| Levels | Focus |
| :--- | :--- |
| 1–5 | `hjkl`, word jumps (`w`/`b`), line boundaries (`0`/`$`) |
| 6–10 | Registers (`"ay`/`"ap`), `f`/`t` jumps, regex boss combat |
| 11–30 | Procedurally generated maps, escalating density |

---

## Controls

| Key | Action |
|-----|--------|
| `h j k l` | Move |
| `w` / `b` | Jump by word distance |
| `3j`, `5l` | Count prefix |
| `"ay` | Yank nearby key into register `a` |
| `"ap` | Put register `a` into nearby lock |
| `v` | Visual mode |
| `d` (in Visual) | Delete selection |
| `u` | Undo |
| `:s/x/y/g` + Enter | Attack regex boss |
| `T` | Cycle theme (Tokyonight / Dracula / Gruvbox) |
| `?` | Level hint |
| `Escape` | Normal mode |

---

## Scoring

Each level has a par. Your rating:

| Rating | Strokes |
|--------|---------|
| S | ≤ par |
| A | ≤ par × 1.5 |
| B | ≤ par × 2.5 |
| C | anything else |

---

## Technical notes

- Audio uses `playsound3` in a Textual worker thread. If no audio backend is available the game runs silently.
- Textual 7+ sends `event.key = "colon"` for `:` and `"question_mark"` for `?`. The key handler normalises via `event.character` before dispatching.
- Scores and config are stored via `platformdirs` so they persist regardless of working directory.

---

## Limitations

- The Vim parser only covers the motions used in the game. It is not a general Vim emulator.
- Audio files (`clack.mp3`, `tick.mp3`) are not included in the repo. The game works without them.
- No multiplayer, no online scores, no Neovim-specific features.

---

## License

MIT — Tushar Satpute
