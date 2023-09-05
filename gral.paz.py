import random 
from typing import Optional
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
width, height = 1000, 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Avenida General Paz")

# Colores
white = (255, 255, 255)
gray = (200, 200, 200)
green = (0, 150, 0)
black = (0, 0, 0)

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar la carretera y los agentes en cada iteración
    road.update_road()

    # Dibujar el pasto verde arriba de la carretera
    pygame.draw.rect(screen, green, (0, 0, width, height // 3))

    # Carretera gris
    pygame.draw.rect(screen, gray, (0, height // 3, width, height // 3))

    # Dibujar el pasto verde abajo de la carretera
    pygame.draw.rect(screen, green, (0, 2 * height // 3, width, height // 3))

    # Líneas blancas en el medio de la carretera
    line_width = 10
    line_height = 5
    num_lines = 30
    gap = width // (num_lines + 1)
    for i in range(num_lines):
        x = (i + 1) * gap - line_width // 2
        pygame.draw.rect(screen, white, (x, height // 2 - line_height // 2, line_width, line_height))

    # Dibujar los agentes en la carretera
    for agent in road.agents:
        pygame.draw.rect(screen, black, (agent.get_position(), height // 3 - 10, agent.length, 20))

    pygame.display.flip()

# Salir del juego
pygame.quit()
sys.exit()
