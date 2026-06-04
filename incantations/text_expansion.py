import keyboard

def register_expansions():
    """Maps custom shorthand runes to comprehensive formatting patterns."""
    print("✍️ Loading text expansion spell matrices...")
    
    # Type ;shrug and hit Space/Enter to expand
    keyboard.add_abbreviation(";shrug", "¯\\_(ツ)_/¯")
    
    # Standard code structure layout boilerplate expansion
    code_block_template = "```text\n\n```"
    keyboard.add_abbreviation(";code", code_block_template)
    
    # Keeps expansion hooks listening actively
    keyboard.wait()
