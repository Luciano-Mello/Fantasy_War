import pygame
#import sys
import random

from src.game.game import attack, heal
from src.ui.grid import Grid
from src.game.characters import Archer, Knight, Mage, Tank, Healer
from src.game.game import handle_click, draw_highlighted_area, move_character, get_cell_at_mouse, is_cell_occupied, get_character_at_cell

# Configurações da Grade
GRID_ROWS = 15
GRID_COLS = 12
CELL_SIZE = 40

#Função que define o time que começa
def jogada_inicial():
    """Roda um random de 50% para qual dorado começa a partida"""
    numero_primeira_jogada = random.randint(1,2)
    if numero_primeira_jogada == 1:
        a = "time_1"
        return a
    else:
        b = "time_2"
        return b

primeira_jogada = jogada_inicial() # Define o time que começa

#Verifica o turno de cada jogador
grid = Grid(GRID_ROWS, GRID_COLS, CELL_SIZE)

# Time 1 (branco)
team_1 = [
    Archer("Robin", 'Team 1'),
    Knight("Arthur", 'Team 1'),
    Mage("Merlin", 'Team 1'),
    Tank("Goliath", 'Team 1'),
    Healer("Luna", 'Team 1'),
]

# Time 2 (vermelho)
team_2 = [
    Archer("Vlad", 'Team 2'),
    Knight("Edgar", 'Team 2'),
    Mage("Zara", 'Team 2'),
    Tank("Hector", 'Team 2'),
    Healer("Clara", 'Team 2'),
]

# Configurar posições iniciais para o Time 1
team_1[0].position = (1, 1)  # Robin
team_1[1].position = (2, 2)  # Arthur
team_1[2].position = (3, 3)  # Merlin
team_1[3].position = (4, 4)  # Goliath
team_1[4].position = (5, 5)  # Luna

# Configurar posições iniciais para o Time 2
team_2[0].position = (GRID_COLS - 2, 1)  # Vlad
team_2[1].position = (GRID_COLS - 3, 2)  # Edgar
team_2[2].position = (GRID_COLS - 4, 3)  # Zara
team_2[3].position = (GRID_COLS - 5, 4)  # Hector
team_2[4].position = (GRID_COLS - 6, 5)  # Clara



# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_COLS * CELL_SIZE, GRID_ROWS * CELL_SIZE))
pygame.display.set_caption("Tactics Game")
clock = pygame.time.Clock()

# Fonte para os nomes
font = pygame.font.Font(None, 24)

# Variável para guardar o personagem selecionado
selected_character = None

def draw_character_on_grid(character):
    """Desenha o personagem na posição especificada no grid"""
    # Tamanho do quadrado (tamanho de cada célula no grid)
    cell_size = 40

    # Posições x, y baseadas na posição do personagem no grid
    x = character.position[0] * cell_size
    y = character.position[1] * cell_size

    # Definir a cor do personagem (usando uma cor baseada no time ou tipo)
    if character in team_1:
        color = (0, 255, 0)  # Cor verde para o time 1 (pode mudar conforme necessário)
    else:
        color = (255, 0, 0)  # Cor vermelha para o time 2 (pode mudar conforme necessário)

    # Desenha um quadrado representando o personagem
    pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))

    # Opcional: desenhar o nome do personagem dentro do quadrado
    font = pygame.font.Font(None, 20)
    text = font.render(character.name, True, (255, 255, 255))  # Texto branco
    screen.blit(text, (x + 5, y + 5))  # Desenha o nome no quadrado


def draw_characters():
    """Desenha todos os personagens no mapa, apenas aqueles que estão vivos"""
    for character in team_1 + team_2:
        if character.health > 0:  # Só desenha personagens vivos
            draw_character_on_grid(character)

def contador_de_turnos(selected_character, primeira_jogada):
    """Verifica se o personagem pertence ao time correto para o turno atual."""
    if selected_character.team == primeira_jogada:
        return True
    else:
        print(f"Não é o turno do {selected_character.team}! É o turno do {primeira_jogada}.")
        return False



def main():
    running = True
    global selected_character, primeira_jogada
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Obtém a célula clicada
                cell = get_cell_at_mouse(pygame.mouse.get_pos(), CELL_SIZE)

                if selected_character:
                    # *** NOVO: Verifica se o turno é válido antes de realizar a ação ***
                    if not contador_de_turnos(selected_character, primeira_jogada):
                        selected_character = None
                        continue

                    target = get_character_at_cell(cell, team_1 + team_2)  # Obtém o alvo (se houver)

                    if target and target.team != selected_character.team:
                        # Realiza ataque ou cura
                        if isinstance(selected_character, Healer) and selected_character.range > 0:
                            heal(selected_character, target)
                        else:
                            attack(selected_character, target, team_1, team_2)

                        # *** NOVO: Troca o turno após o ataque ou cura ***
                        if primeira_jogada == "team_1":
                            primeira_jogada = "team_2"
                        else:
                            "team_1"
                        selected_character = None  # Deseleciona o personagem após a jogada
                    elif not is_cell_occupied(cell, team_1, team_2):
                        # Move o personagem se a célula estiver livre e no alcance
                        if move_character(selected_character, cell, team_1, team_2):
                            # *** NOVO: Troca o turno após o movimento ***
                            if primeira_jogada == "team_1":
                                primeira_jogada = "team_2"
                            else:
                                "team_1"
                            selected_character = None  # Deseleciona o personagem após a jogada
                    else:
                        # Permite selecionar outro personagem se a célula não for válida
                        selected_character = handle_click(pygame.mouse.get_pos(), team_1 + team_2)
                else:
                    # Seleciona um personagem se nenhum estiver selecionado
                    selected_character = handle_click(pygame.mouse.get_pos(), team_1 + team_2)

        # Atualiza a tela
        screen.fill((50, 50, 50))
        grid.draw(screen)
        if selected_character:
            draw_highlighted_area(screen, selected_character, CELL_SIZE, GRID_ROWS, GRID_COLS)
        draw_characters()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
