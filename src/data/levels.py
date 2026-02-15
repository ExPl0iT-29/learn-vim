from src.data.models import LevelConfig
from typing import List

def gen_curriculum() -> List[LevelConfig]:
    """Generates the game curriculum consisting of 30 levels."""
    levels = []
    
    # Milestone I: Foundation (1-5)
    levels.append(LevelConfig(1, "The Cursor", "VimRunner, move to the portal [>] using h,j,k,l.", ["#@.......>#"], {"h","j","k","l"}, 7))
    levels.append(LevelConfig(2, "The Word", "Word jumps [w/b] are faster. Leap across.", ["#@...w...w..>#"], {"w","b"}, 3))
    levels.append(LevelConfig(3, "The Edge", "0 and $ jump to boundaries. Use them.", ["#@.........>#"], {"0","$"}, 2))
    levels.append(LevelConfig(4, "Efficiency", "Combine counts [3j]. Speed is armor.", ["#@..........","#..........","#..........>#"], {"count"}, 3))
    levels.append(LevelConfig(5, "ZigZag", "Navigate the stack. No wasted moves.", ["#@...#","#...#","#..>#"], {"h","j","k","l"}, 10))

    # Milestone II: Registers & Discovery (6-10)
    levels.append(LevelConfig(6, "The Key", "Yank the Key [a] using \"ay. Use it on Lock [A].", ["#@..a..A..>#"], {"y","p"}, 6))
    levels.append(LevelConfig(7, "The Vault", "Multiple registers. \"ay the a-key. \"by the b-key.", ["#@..a..b..A..B..>#"], {"y","p"}, 10))
    levels.append(LevelConfig(8, "The Sniper", "Jump to character [f] followed by target.", ["#@...X.......>#"], {"f","t"}, 3))
    levels.append(LevelConfig(9, "The Corridor", "Corrupted data ahead. Resolve the integrity breach.", ["#@.........>#"], {"all"}, 2))
    levels.append(LevelConfig(10, "BOSS: CORRUPTED DATA", "TYPE [:] then [s/CORRUPT/DATA/g] to purge the Boss [B].", ["#@...B.....>#"], {"command"}, 5))

    # Milestones 11-30 generated
    for level_number in range(11, 31):
        levels.append(LevelConfig(level_number, f"Sector {level_number}", f"Continue training, Runner. Difficulty level {level_number}.", ["#@....G....>#"], {"all"}, level_number))
    
    return levels

LEVELS = gen_curriculum()
