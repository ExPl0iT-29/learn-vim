from typing import List
from src.data.procgen import DungeonGenerator

def gen_curriculum() -> List[LevelConfig]:
    """Generates the game curriculum consisting of 30 levels."""
    levels = []
    
    # Milestone I: Foundation (1-5)
    levels.append(LevelConfig(1, "The Cursor", "VimRunner, move to the portal [>] using h,j,k,l.", ["#@.......>#"], {"h","j","k","l"}, 7, hint="Use [bold]h,j,k,l[/] to move. Navigate to the [bold]>[/] symbol."))
    levels.append(LevelConfig(2, "The Word", "Word jumps [w/b] are faster. Leap across.", ["#@...w...w..>#"], {"w","b"}, 3, hint="Use [bold]w[/] to jump to the next word."))
    levels.append(LevelConfig(3, "The Edge", "0 and $ jump to boundaries. Use them.", ["#@.........>#"], {"0","$"}, 2, hint="Use [bold]0[/] for start, [bold]$[/] for end of line."))
    levels.append(LevelConfig(4, "Efficiency", "Combine counts [3j]. Speed is armor.", ["#@..........","#..........","#..........>#"], {"count"}, 3, hint="Type a [bold]number[/] before a motion (e.g., [bold]3j[/])."))
    levels.append(LevelConfig(5, "ZigZag", "Navigate the stack. No wasted moves.", ["#@...#","#...#","#..>#"], {"h","j","k","l"}, 10, hint="Find the most efficient path using all learned motions."))

    # Milestone II: Registers & Discovery (6-10)
    levels.append(LevelConfig(6, "The Key", "Yank the Key [a] using \"ay. Use it on Lock [A].", ["#@..a..A..>#"], {"y","p"}, 6, 
        hint="Stand near [bold]a[/], type [bold]\"ay[/]. Then near [bold]A[/], type [bold]\"ap[/].",
        detailed_help="[bold #bb9af7]REGISTERS 101[/]\n\n" +
                      "Registers are like clipboards. You have multiple!\n" +
                      "1. Stand next to Key [bold #e0af68]a[/].\n" +
                      "2. Type [bold #7aa2f7]\"ay[/] to Yank the key into register 'a'.\n" +
                      "3. Stand next to Lock [bold #bb9af7]A[/].\n" +
                      "4. Type [bold #7aa2f7]\"ap[/] to Put (paste) the key into the lock.\n\n" +
                      "The register name ([bold]a[/]) must match the key symbol."))
    
    levels.append(LevelConfig(7, "The Vault", "Multiple registers. \"ay the a-key. \"by the b-key.", ["#@..a..b..A..B..>#"], {"y","p"}, 10,
        hint="Yank 'a' into [bold]\"a[/] and 'b' into [bold]\"b[/]. Unlock in order.",
        detailed_help="[bold #bb9af7]MULTI-REGISTER MASTERY[/]\n\n" +
                      "You can store different keys in different registers simultaneously.\n" +
                      "1. Yank 'a' into '\"a' ([bold]\"ay[/]).\n" +
                      "2. Yank 'b' into '\"b' ([bold]\"by[/]).\n" +
                      "3. Use [bold]\"ap[/] near Lock A and [bold]\"bp[/] near Lock B."))

    levels.append(LevelConfig(8, "The Sniper", "Jump to character [f] followed by target.", ["#@...X.......>#"], {"f","t"}, 3, hint="Type [bold]f[/] then [bold]X[/] to jump directly to X."))
    levels.append(LevelConfig(9, "The Corridor", "Corrupted data ahead. Resolve the integrity breach.", ["#@.........>#"], {"all"}, 2, hint="Prepare for combat. Use all learned techniques."))
    levels.append(LevelConfig(10, "BOSS: CORRUPTED DATA", "TYPE [:] then [s/CORRUPT/DATA/g] to purge the Boss [B].", ["#@...B.....>#"], {"command"}, 5,
        hint="Type [bold]:[/], then [bold]s/CORRUPT/DATA/g[/], then [bold]Enter[/].",
        detailed_help="[bold #f7768e]REGEX COMBAT[/]\n\n" +
                      "To damage a BOSS [bold #f7768e]B[/], you must use a Search & Replace command.\n" +
                      "1. Type [bold]:[/] to enter Command Mode.\n" +
                      "2. Type [bold]s/TARGET/REPLACEMENT/g[/].\n" +
                      "3. Press [bold]Enter[/].\n\n" +
                      "Example: To purge CORRUPT data, use [bold]:s/CORRUPT/DATA/g[/]."))

    # Milestones 11-30 are procedurally generated
    generator = DungeonGenerator(width=25, height=12)
    for level_number in range(11, 31):
        # Generate the map dynamically
        map_template = generator.generate(difficulty=level_number)
        
        hint = "Procedural Sector. Use everything you've learned."
        if level_number % 5 == 0:
            hint = "WARNING: Boss detected. Prepare your regex."
        elif level_number % 3 == 0:
            hint = "PUZZLE CACHE: Locate the key and yank it to open the lock."
            
        levels.append(LevelConfig(
            num=level_number, 
            name=f"Sector {level_number}", 
            instructions=f"Proceed to the next portal. Threat Level {level_number}.", 
            map_template=map_template, 
            unlocked_commands={"all"}, 
            par_keystrokes=level_number * 2 + 10,
            hint=hint
        ))
    
    return levels

LEVELS = gen_curriculum()
