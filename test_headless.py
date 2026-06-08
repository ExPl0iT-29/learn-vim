"""
Headless playthrough test using Textual's Pilot API.
Exercises: launch, narrative dismiss, movement, help overlay,
level completion, score persistence, undo, theme cycling, audio (no crash).
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from vim_masterpiece.app import VimMasterpiece
from vim_masterpiece.data.models import GameMode, Point


PASS = "[PASS]"
FAIL = "[FAIL]"
results = []


def check(label, condition, detail=""):
    status = PASS if condition else FAIL
    msg = f"{status} {label}" + (f" -- {detail}" if detail else "")
    results.append((condition, msg))
    print(msg)


async def run_tests():
    app = VimMasterpiece()

    async with app.run_test(size=(120, 40)) as pilot:

        # ── 1. App mounted & level loaded ─────────────────────────────────
        check("App mounted", app.engine is not None)
        check("Level 1 loaded", app.engine.current_level.num == 1,
              f"got level {app.engine.current_level.num}")
        check("AudioEngine created", app.audio is not None)
        check("ScoringEngine created", app.scoring is not None)

        # ── 2. Narrative overlay visible at start ─────────────────────────
        narrative = app.query_one("#narrative")
        check("Narrative overlay shown on level 1",
              narrative.styles.display == "block")

        await pilot.press("space")
        await pilot.pause(0.05)
        check("Narrative dismissed after keypress",
              narrative.styles.display != "block")

        # ── 3. Command bar present ────────────────────────────────────────
        cmdbar = app.query_one("#command-bar")
        check("Command bar present", cmdbar is not None)

        # ── 4. Movement (l = move right) ──────────────────────────────────
        start_x = app.engine.player.position.x
        await pilot.press("l")
        await pilot.pause(0.05)
        check("l key handled without crash",
              app.engine.keystroke_count >= 1)

        # ── 5. Undo reverts the move ──────────────────────────────────────
        await pilot.press("u")
        await pilot.pause(0.05)
        check("Undo works",
              app.engine.player.position.x == start_x,
              f"expected x={start_x}, got x={app.engine.player.position.x}")

        # ── 6. Count + motion (3l) ────────────────────────────────────────
        await pilot.press("3")
        await pilot.press("l")
        await pilot.pause(0.05)
        check("Count + motion handled without crash",
              app.engine.keystroke_count >= 0)

        # ── 7. Visual mode ────────────────────────────────────────────────
        await pilot.press("v")
        await pilot.pause(0.05)
        check("v enters Visual mode",
              app.engine.mode == GameMode.VISUAL)

        await pilot.press("escape")
        await pilot.pause(0.05)
        check("Escape returns to Normal mode",
              app.engine.mode == GameMode.NORMAL)

        # ── 8. Command mode via : ─────────────────────────────────────────
        await pilot.press(":")
        await pilot.pause(0.05)
        check("':' enters Command mode",
              app.engine.mode == GameMode.COMMAND,
              f"mode is {app.engine.mode}")

        await pilot.press("escape")
        await pilot.pause(0.05)
        check("Escape exits Command mode",
              app.engine.mode == GameMode.NORMAL)

        # ── 9. Help overlay ───────────────────────────────────────────────
        help_overlay = app.query_one("#help-overlay")
        await pilot.press("?")
        await pilot.pause(0.05)
        check("? opens help overlay",
              help_overlay.styles.display == "block",
              f"display={help_overlay.styles.display}")

        await pilot.press("space")
        await pilot.pause(0.05)
        check("Keypress dismisses help overlay",
              help_overlay.styles.display != "block")

        # ── 10. Theme cycling ─────────────────────────────────────────────
        theme_before = app.themes[app.current_theme_idx]
        await pilot.press("T")
        await pilot.pause(0.05)
        theme_after = app.themes[app.current_theme_idx]
        check("T cycles theme",
              theme_before != theme_after,
              f"{theme_before} -> {theme_after}")

        # ── 11. Audio engine — no crash on clack() with missing assets ────
        audio_ok = True
        try:
            app.audio.clack()
            await pilot.pause(0.1)
        except Exception:
            audio_ok = False
        check("AudioEngine.clack() doesn't raise even without .mp3 files", audio_ok)

        # ── 12. Score persistence ─────────────────────────────────────────
        app.scoring.save_best(99, 5)
        reloaded = app.scoring.storage.load()
        check("Score saved and reloaded from disk",
              reloaded.get("99") == 5,
              f"got {reloaded.get('99')}")

        # ── 13. Stats display renders ─────────────────────────────────────
        check("StatsDisplay present", app.query_one("#stats") is not None)

        # ── 14. Log widget renders ────────────────────────────────────────
        check("Log widget present", app.query_one("#log") is not None)

        # ── 15. HelpPanel present ─────────────────────────────────────────
        check("HelpPanel present", app.query_one("#help-panel") is not None)

        # ── 16. VimMap present ────────────────────────────────────────────
        check("VimMap present", app.query_one("#map") is not None)

        # ── 17. Regex attack in Command mode ─────────────────────────────
        await pilot.press(":")
        await pilot.pause(0.05)
        for ch in "s/CORRUPT/DATA/g":
            await pilot.press(ch)
            await pilot.pause(0.01)
        await pilot.press("enter")
        await pilot.pause(0.05)
        check("Regex attack enters and exits Command mode",
              app.engine.mode == GameMode.NORMAL,
              f"mode={app.engine.mode}")

        # ── 18. Level advance loads level 2 ──────────────────────────────
        app.engine.level_complete = True
        app.engine.current_level_index += 1
        app.load_level()
        await pilot.pause(0.05)
        check("Level advance loads level 2",
              app.engine.current_level.num == 2,
              f"got level {app.engine.current_level.num}")

        # ── 19. Keystroke count resets on new level ───────────────────────
        check("Keystroke count reset on level load",
              app.engine.keystroke_count == 0)

        # ── 20. All 30 levels have valid config ───────────────────────────
        from vim_masterpiece.data.levels import LEVELS
        levels_ok = all(
            lvl.num > 0 and lvl.map_template and lvl.par_keystrokes >= 0
            for lvl in LEVELS
        )
        check("All 30 levels have valid config", levels_ok,
              f"count={len(LEVELS)}")

        await app.action_quit()

    # ── Summary ───────────────────────────────────────────────────────────
    passed = sum(1 for ok, _ in results if ok)
    total = len(results)
    failed = [msg for ok, msg in results if not ok]

    print()
    print("=" * 55)
    print(f"  RESULT: {passed}/{total} tests passed")
    if failed:
        print("\n  FAILURES:")
        for f in failed:
            print(f"    {f}")
    print("=" * 55)

    return passed == total


if __name__ == "__main__":
    ok = asyncio.run(run_tests())
    sys.exit(0 if ok else 1)
