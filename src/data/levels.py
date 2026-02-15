from src.data.models import LevelConfig
from typing import List

def gen_curriculum() -> List[LevelConfig]:
    lvls = []
    
    # Milestone I: Foundation (1-5)
    lvls.append(LevelConfig(1, "The Cursor", "VimRunner, move to the portal [>] using h,j,k,l.", ["#@.......>#"], {"h","j","k","l"}, 7))
    lvls.append(LevelConfig(2, "The Word", "Word jumps [w/b] are faster. Leap across.", ["#@...w...w..>#"], {"w","b"}, 3))
    lvls.append(LevelConfig(3, "The Edge", "0 and $ jump to boundaries. Use them.", ["#@.........>#"], {"0","$"}, 2))
    lvls.append(LevelConfig(4, "Efficiency", "Combine counts [3j]. Speed is armor.", ["#@..........","#..........","#..........>#"], {"count"}, 3))
    lvls.append(LevelConfig(5, "ZigZag", "Navigate the stack. No wasted moves.", ["#@...#","#...#","#..>#"], {"h","j","k","l"}, 10))

    # Milestone II: Registers & Discovery (6-10)
    lvls.append(LevelConfig(6, "The Key", "Yank the Key [a] using \"ay. Use it on Lock [A].", ["#@..a..A..>#"], {"y","p"}, 6))
    lvls.append(LevelConfig(7, "The Vault", "Multiple registers. \"ay the a-key. \"by the b-key.", ["#@..a..b..A..B..>#"], {"y","p"}, 10))
    lvls.append(LevelConfig(8, "The Sniper", "Jump to character [f] followed by target.", ["#@...X.......>#"], {"f","t"}, 3))
    lvls.append(LevelConfig(9, "The Corridor", "Corrupted data ahead. Re-read the manual.", ["#@.........>#"], {"all"}, 2))
    lvls.append(LevelConfig(10, "BOSS: CORRUPTED DATA", "TYPE [:] then [s/CORRUPT/DATA/g] to purge the Boss [B].", ["#@...B.....>#"], {"command"}, 5))

    # Milestones 11-30 generated
    for i in range(11, 31):
        lvls.append(LevelConfig(i, f"Sector {i}", f"Continue training, Runner. Difficulty level {i}.", ["#@....G....>#"], {"all"}, i))
    
    return lvls

LEVELS = gen_curriculum()
