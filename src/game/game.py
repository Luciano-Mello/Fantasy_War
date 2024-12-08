import pygame

def handle_click(pos, characters):
    """Lida com cliques do mouse para selecionar personagens."""
    x, y = pos
    cell = x // 40, y // 40
    for character in characters:
        if character.position == cell:
            return character
    return None

def draw_highlighted_area(screen, character, cell_size, grid_rows, grid_cols):
    """Desenha áreas de movimento e ataque ao redor do personagem."""
    if character:
        x, y = character.position
        # Área de movimento
        for dx in range(-character.movement, character.movement + 1):
            for dy in range(-character.movement, character.movement + 1):
                if abs(dx) + abs(dy) <= character.movement:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < grid_cols and 0 <= ny < grid_rows:
                        rect = pygame.Rect(nx * cell_size, ny * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, (0, 0, 255), rect, 2)  # Azul

        # Área de ataque
        for dx in range(-character.range, character.range + 1):
            for dy in range(-character.range, character.range + 1):
                if abs(dx) + abs(dy) <= character.range:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < grid_cols and 0 <= ny < grid_rows:
                        rect = pygame.Rect(nx * cell_size, ny * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, (255, 0, 0), rect, 2)  # Vermelho

def is_cell_occupied(position, team_1, team_2):
    """Verifica se a célula está ocupada por algum personagem"""
    for character in team_1 + team_2:
        if character.position == position:
            return True
    return False

def move_character(character, target_position, team_1, team_2):
    """Move o personagem se a célula não estiver ocupada"""
    # Verificar se o alvo está dentro do alcance de movimento
    x, y = target_position
    x_curr, y_curr = character.position
    if abs(x_curr - x) <= character.movement and abs(y_curr - y) <= character.movement:
        # Verificar se a célula está ocupada
        if not is_cell_occupied(target_position, team_1, team_2):
            character.position = target_position
            print(f"{character.name} se moveu para {target_position}")
        else:
            print(f"A célula {target_position} está ocupada.")
    else:
        print(f"{character.name} não pode se mover para {target_position}. Fora do alcance de movimento.")


def get_cell_at_mouse(pos, cell_size):
    """Obtém a célula da grade com base na posição do mouse."""
    x, y = pos
    return x // cell_size, y // cell_size

def attack(attacker, defender):
    """Função que simula o ataque de um personagem a outro"""
    if defender.health > 0:
        defender.health -= attacker.attack
        if defender.health < 0:
            defender.health = 0  # Não permite vida negativa
        print(f"{attacker.name} atacou {defender.name}. {defender.name} agora tem {defender.health} de vida.")
    else:
        print(f"{defender.name} já está derrotado!")

def heal(healer, ally):
    """Função para curar um aliado"""
    if ally.health > 0:
        heal_amount = 20  # Valor de cura
        ally.health += heal_amount
        if ally.health > 100:  # A vida não pode ultrapassar 100
            ally.health = 100
        print(f"{healer.name} curou {ally.name}. {ally.name} agora tem {ally.health} de vida.")
    else:
        print(f"{ally.name} não pode ser curado porque já está derrotado!")

def get_character_at_cell(cell, all_characters):
    """Retorna o personagem que está na célula especificada (se houver)"""
    for character in all_characters:
        if character.position == cell:
            return character
    return None

# Definindo a função de ataque
def attack(attacker, defender, team_1, team_2):
    """Função que simula o ataque de um personagem a outro"""
    if defender.health > 0:
        defender.health -= attacker.attack
        if defender.health < 0:
            defender.health = 0  # Não permite vida negativa
        print(f"{attacker.name} atacou {defender.name}. {defender.name} agora tem {defender.health} de vida.")

        # Remover o personagem derrotado
        if defender.health == 0:
            if defender in team_1:
                team_1.remove(defender)
                print(f"{defender.name} foi derrotado e removido do time 1.")
            elif defender in team_2:
                team_2.remove(defender)
                print(f"{defender.name} foi derrotado e removido do time 2.")
    else:
        print(f"{defender.name} já está derrotado!")


# Definindo a função de cura
def heal(healer, ally):
    """Função para curar um aliado"""
    if ally.health > 0:
        heal_amount = 20  # Valor de cura
        ally.health += heal_amount
        if ally.health > 100:  # A vida não pode ultrapassar 100
            ally.health = 100
        print(f"{healer.name} curou {ally.name}. {ally.name} agora tem {ally.health} de vida.")
    else:
        print(f"{ally.name} não pode ser curado porque já está derrotado!")
