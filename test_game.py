import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from vim_masterpiece.core.engine import GameEngine
from vim_masterpiece.data.procgen import DungeonGenerator
from vim_masterpiece.data.models import LevelConfig, GameMode, Point, Entity, EntityType


def test_engine():
    print("Testing Procedural Generation...")
    generator = DungeonGenerator(width=15, height=10)
    map_template = generator.generate(difficulty=15)

    assert len(map_template) == 10
    assert len(map_template[0]) == 15
    print("ProcGen passed.")

    print("Testing Engine Initialization...")
    engine = GameEngine()
    config = LevelConfig(
        num=15,
        name="Sector 15",
        instructions="Test",
        map_template=map_template
    )
    engine.load_level(config)
    print("Level load passed.")

    print("Testing Move and Undo...")
    start_pos = Point(engine.player.position.x, engine.player.position.y)
    engine.save_state()
    engine.move_player(1, 0, 1)
    assert engine.player.position.x != start_pos.x or engine.map_data[start_pos.y][start_pos.x + 1] != "."

    engine.undo()
    assert engine.player.position.x == start_pos.x
    assert engine.player.position.y == start_pos.y
    print("Undo passed.")

    print("Testing Visual Mode Deletion...")
    engine.enemies.clear()

    enemy = Entity("TestEnemy", "G", Point(start_pos.x + 1, start_pos.y), 5, 5, EntityType.ENEMY)
    engine.enemies.append(enemy)

    engine.mode = GameMode.VISUAL
    engine.set_visual_anchor()
    engine.player.position = Point(start_pos.x + 1, start_pos.y)
    engine.handle_delete()

    assert len(engine.enemies) == 0
    assert engine.mode == GameMode.NORMAL
    print("Visual Mode Deletion passed.")

    print("ALL TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_engine()
