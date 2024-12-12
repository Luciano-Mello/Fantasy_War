import pygame

class Character:
    def __init__(self, name, team, color):
        self.name = name
        self.health = 100
        self.attack = 10
        self.movement = 3
        self.range = 1
        self.team = team  # 'Team 1' ou 'Team 2'
        self.color = color  # Cor do personagem
        self.position = (0, 0)  # Posição inicial

    def draw(self, screen, cell_size):
        """Desenha o personagem na tela"""
        x, y = self.position
        pygame.draw.circle(screen, self.color,
                           (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), cell_size // 3)
        font = pygame.font.Font(None, 24)
        name_surface = font.render(self.name, True, (0, 0, 0))
        screen.blit(name_surface, (x * cell_size + 5, y * cell_size - 10))

# Definindo subclasses de cada tipo de personagem (Arqueiro, Cavaleiro, etc.)

class Archer(Character):
    def __init__(self, name, team):
        super().__init__(name, team, (255, 255, 255) if team == 'Team 1' else (255, 0, 0))
        self.attack = 20
        self.movement = 3
        self.range = 1

class Knight(Character):
    def __init__(self, name, team):
        super().__init__(name, team, (255, 255, 255) if team == 'Team 1' else (255, 0, 0))
        self.health = 150
        self.attack = 25
        self.movement = 2
        self.range = 1

class Mage(Character):
    def __init__(self, name, team):
        super().__init__(name, team, (255, 255, 255) if team == 'Team 1' else (255, 0, 0))
        self.health = 80
        self.attack = 30
        self.movement = 3
        self.range = 2

class Tank(Character):
    def __init__(self, name, team):
        super().__init__(name, team, (255, 255, 255) if team == 'Team 1' else (255, 0, 0))
        self.health = 200
        self.attack = 15
        self.movement = 1
        self.range = 1

class Healer(Character):
    def __init__(self, name, team):
        super().__init__(name, team, (255, 255, 255) if team == 'Team 1' else (255, 0, 0))
        self.health = 90
        self.attack = 0
        self.movement = 4
        self.range = 4
