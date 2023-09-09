import sys
import pygame
import random



from agent import Agent
from road import Road

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
width, height = 1000, 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulación de la Ruta General Paz")

# Colores
white = (255, 255, 255)
gray = (200, 200, 200)
green = (0, 150, 0)
black = (0, 0, 0)


def draw_road(screen):
    # Dibuja la carretera (rectángulo gris)
    pygame.draw.rect(screen, gray, (0, 0, width, height))

    # Dibuja líneas blancas en la carretera
    line_width = 10
    line_height = 5
    num_lines = 20
    line_gap = width // num_lines

    for i in range(num_lines):
        line_x = i * line_gap
        pygame.draw.rect(screen, white, (line_x, height // 2 - line_height // 2, line_width, line_height))

    # Dibuja los autos
    for agent in general_paz.agents:
        pygame.draw.rect(screen, black, (agent.get_position(), height // 2 - agent.length // 2, agent.length, 10))


general_paz = Road(1000, congestion=True)  # Puedes ajustar la longitud de la carretera aquí


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(green)  # Establece el fondo como verde para simular pasto
    draw_road(screen)  # Dibuja la carretera y los autos

    pygame.display.flip()
    clock.tick(60)  # Controla la velocidad de fotogramas

    general_paz.update_road()  # Actualiza la simulación de la carretera y los autos
