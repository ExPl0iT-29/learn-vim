# Contributing

## Setup

```bash
git clone https://github.com/ExPl0iT-29/vim-masterpiece
cd vim-masterpiece
pip install -e ".[dev]"
```

Requires Python 3.10+. The dev extras pull in `textual-dev` for the Textual devtools and `pytest` for tests.

## Running tests

```bash
pytest test_headless.py -v
```

27 headless tests using Textual's Pilot API. They cover level loading, command parsing, scoring, and screen transitions. No display required.

## What to work on

Check the issue tracker. Good first areas:

- **New levels** — add entries to `src/vim_masterpiece/data/levels.py`. Each level needs a `target_text`, `start_text`, a list of `commands`, and a `par` keystroke count.
- **Audio** — the audio engine is in `src/vim_masterpiece/audio.py`. Currently plays two sounds (`clack.mp3`, `tick.mp3`). Additions go there.
- **Vim command coverage** — the parser is in `src/vim_masterpiece/mechanics/parser.py`. If a real Vim command isn't handled, that's a bug.

## Before opening a PR

- Run `pytest` — all 27 tests should pass
- Run the game manually: `vim-masterpiece` (or `python -m vim_masterpiece`)
- If you added a level, play through it to confirm the par count is achievable

## Adding levels

The level format is defined in `src/vim_masterpiece/data/levels.py`. Copy an existing level as a template. The `par` value should be the minimum number of keystrokes a reasonably experienced Vim user would need, not the theoretical minimum.

## Bugs

File an issue with:
- What you typed
- What the game did
- What you expected

For command parsing bugs, include the exact key sequence.
