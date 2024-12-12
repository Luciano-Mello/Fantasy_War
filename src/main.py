import pygame
import sys
import random

from src.game.game import attack, heal
from src.ui.grid import Grid
from src.game.characters import Archer, Knight, Mage, Tank, Healer
from src.game.game import handle_click, draw_highlighted_area, move_character, get_cell_at_mouse, is_cell_occupied, \
    get_character_at_cell

# Configurações da Grade
GRID_ROWS = 15
GRID_COLS = 12
CELL_SIZE = 40


# Função que define o time que começa
def jogada_inicial():
    """Roda um random de 50% para qual jogador começa a partida"""
    numero_primeira_jogada = random.randint(1, 2)
    if numero_primeira_jogada == 1:
        return "Team 1"
    else:
        return "Team 2"


# Define o time que começa
primeira_jogada = jogada_inicial()

# Verifica o turno de cada jogador
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
font = pygame.font.Font(None, 22)

# Variável para guardar o personagem selecionado
selected_character = None


def draw_character_on_grid(character):
    """Desenha o personagem na posição especificada no grid"""
    x = character.position[0] * CELL_SIZE
    y = character.position[1] * CELL_SIZE

    # Definir a cor do personagem (usando uma cor baseada no time ou tipo)
    if character in team_1:
        color = (255, 140, 0)  # Cor verde para o time 1 (pode mudar conforme necessário)
    else:
        color = (110, 15, 115)  # Cor vermelha para o time 2 (pode mudar conforme necessário)

    # Desenha um quadrado representando o personagem
    pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

    # Opcional: desenhar o nome do personagem dentro do quadrado
    font = pygame.font.Font(None, 18)
    text = font.render(character.name, True, (255, 255, 255))  # Texto branco
    screen.blit(text, (x + 5, y + 7))  # Desenha o nome no quadrado


def draw_characters():
    """Desenha todos os personagens no mapa, apenas aqueles que estão vivos"""
    for character in team_1 + team_2:
        if character.health > 0:  # Só desenha personagens vivos
            draw_character_on_grid(character)


def main():
    global selected_character, primeira_jogada
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Obtém a célula que foi clicada
                cell = get_cell_at_mouse(pygame.mouse.get_pos(), CELL_SIZE)

                if selected_character:
                    # Verifica se o personagem selecionado é do turno atual
                    if selected_character.team != primeira_jogada:
                        selected_character = None  # Deseleciona o personagem
                        continue

                    # Se o personagem está selecionado, tenta realizar a ação
                    target = get_character_at_cell(cell, team_1 + team_2)

                    if target and target.team != selected_character.team:
                        # Se o alvo for um inimigo, realiza o ataque ou cura
                        if isinstance(selected_character, Healer) and selected_character.range > 0:
                            heal(selected_character, target)  # Cura se for Healer
                        else:
                            attack(selected_character, target, team_1, team_2)  # Ataque normal
                        selected_character = None  # Deselect após ação
                        primeira_jogada = "Team 1" if primeira_jogada == "Team 2" else "Team 2"  # Alterna o turno
                    elif not is_cell_occupied(cell, team_1, team_2):
                        # Se a célula não estiver ocupada e dentro do alcance, move o personagem
                        if move_character(selected_character, cell, team_1, team_2):
                            selected_character = None  # Deselect após mover
                            primeira_jogada = "Team 1" if primeira_jogada == "Team 2" else "Team 2"  # Alterna o turno
                    else:
                        selected_character = None  # Deseleciona o personagem se a ação falhar
                else:
                    # Se não há personagem selecionado, tenta selecionar um novo personagem
                    clicked_character = handle_click(pygame.mouse.get_pos(), team_1 + team_2)
                    if clicked_character and clicked_character.team == primeira_jogada:
                        selected_character = clicked_character  # Seleciona apenas personagens do turno atual

        # Limpa a tela e desenha os componentes
        screen.fill((50, 5, 20))
        grid.draw(screen)

        if selected_character:
            draw_highlighted_area(screen, selected_character, CELL_SIZE, GRID_ROWS, GRID_COLS)

        draw_characters()

        # Mostra de quem é o turno atual
        turn_text = font.render(f"Turno: {primeira_jogada}", True, (0, 255, 0))
        screen.blit(turn_text, (10, 10))

        pygame.display.flip()  # Atualiza a tela
        clock.tick(60)  # Limita a taxa de quadros

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
