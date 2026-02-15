from .engine import LevelConfig

LEVELS = [
    LevelConfig(
        1, "The Basics",
        "Welcome! Move to the exit [>] using [h, j, k, l].\nh: Left, j: Down, k: Up, l: Right",
        [
            "####################",
            "#@.................#",
            "#..................#",
            "#..................#",
            "#..................#",
            "#.................>#",
            "####################",
        ],
        ["h", "j", "k", "l"]
    ),
    LevelConfig(
        2, "Word Power",
        "Use [w] to jump forward 3 tiles and [b] to jump back.\nReach the exit!",
        [
            "####################",
            "#@..w..w..w..w..w..#",
            "#..................#",
            "#..................#",
            "#>.................#",
            "####################",
        ],
        ["w", "b"]
    ),
    LevelConfig(
        3, "Line Navigation",
        "Use [0] to jump to the start of the line\nand [$] to jump to the end.\nNavigate the long bridge!",
        [
            "########################################",
            "#@....................................>#",
            "########################################",
        ],
        ["0", "$"]
    ),
    LevelConfig(
        4, "Multiplication",
        "Type a number before a command (e.g., 5j) to repeat it.\nCross the gap quickly!",
        [
            "#########",
            "#@......#",
            "#.......#",
            "#.......#",
            "#.......#",
            "#.......#",
            "#......>#",
            "#########",
        ],
        ["count"]
    ),
    LevelConfig(
        5, "The Destroyer",
        "Use [x] to delete Rubble [R] in your way.\nClear the path to the exit.",
        [
            "##########",
            "#@.......#",
            "####R#####",
            "#........#",
            "#R########",
            "#.......>#",
            "##########",
        ],
        ["x"]
    ),
    LevelConfig(
        6, "The Warrior",
        "Use [dd] or [dw] to defeat Goblins [G].\nYou must fight to survive!",
        [
            "##########",
            "#@..G....#",
            "##########",
            "#G.......#",
            "##########",
            "#....G..>#",
            "##########",
        ],
        ["dw", "dd"]
    ),
    LevelConfig(
        7, "Zig Zag",
        "Combine counts and movement to navigate the maze.",
        [
            "##########",
            "#@.......#",
            "########.#",
            "#........#",
            "#.########",
            "#........#",
            "########>#",
        ],
        ["all"]
    ),
    LevelConfig(
        8, "The Gauntlet",
        "Multiple enemies and rubble blocks stand in your way.",
        [
            "####################",
            "#@..R..G..R..G..R..#",
            "##################.#",
            "#..................#",
            "#.##################",
            "#.................>#",
            "####################",
        ],
        ["all"]
    ),
    LevelConfig(
        9, "Speed Run",
        "Reach the exit in the least steps possible using all your skills.",
        [
            "####################",
            "#@.................#",
            "#.......R..........#",
            "#.......G..........#",
            "#.......R..........#",
            "#>.................#",
            "####################",
        ],
        ["all"]
    ),
    LevelConfig(
        10, "Master of Vim",
        "Final Test: Reach the exit. Congratulations on your journey!",
        [
            "####################",
            "#@.......G.........#",
            "#........G.........#",
            "#..G..G..G..G..G...#",
            "#........G.........#",
            "#........G........>#",
            "####################",
        ],
        ["all"]
    )
]
