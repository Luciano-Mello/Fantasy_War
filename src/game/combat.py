
def check_combat(character_1, character_2):
    """Verifica se dois personagens estão próximos o suficiente para lutar."""
    x1, y1 = character_1.position
    x2, y2 = character_2.position

    # Verifica se os personagens estão dentro do alcance de ataque
    if abs(x1 - x2) <= character_1.range and abs(y1 - y2) <= character_1.range:
        # Ataque!
        character_2.health -= character_1.attack
        if character_2.health < 0:
            character_2.health = 0
        return True
    return False