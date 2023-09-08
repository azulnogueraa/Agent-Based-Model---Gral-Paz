
import random 
from typing import Optional
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

import pygame
import sys

class Agent(pygame.sprite.Sprite):

    def __init__(self):
        self.position = 0                                             #posición inicial, todos los autos entran al inicio de la autopista
        self.max_velocity = 80/3.6                                    #velocidad maxima, todos los autos tienen la misma velocidad maxima (sabemos que en la Gral. Paz es de 80 km/h)  
        self.length = 5                                               #longitud del vehiculo, todos los autos tienen la misma longitud 
        self.front_agent = None                                       #agente de adelante
        self.back_agent = None                                        #agente de atras
        self.collision = False                                        #variable que indica si hubo un choque
        
        '''
        velocidad de agente es generada a partir de la distribución triangular con los siguientes parametros:
        - 30,000 m/s: velocidad minima
        - 100,000 m/s: velocidad maxima
        - 70,000 m/s: moda
        '''
        self.velocity = random.triangular(30/3.6, 100/3.6, 70/3.6)
        self.time = 0
        self.arrival_time = 0
    
        self.reaction_time = random.normalvariate(0.17, 0.005) #EXPLICAR PORQUE ES 0.15 (HAY UN PAPER)
    
    def __str__(self):
        front_agent_info = (
            f"(t={self.front_agent.time}, x={self.front_agent.position}, "
            f"v={self.front_agent.velocity})"
            if self.front_agent is not None else "None"
        )
        
        back_agent_info = (
            f"(t={self.back_agent.time}, x={self.back_agent.position}, "
            f"v={self.back_agent.velocity})"
            if self.back_agent is not None else "None"
        )
        
        return (
            f"Agent(t={self.time}, at={self.arrival_time}, x={self.position}, "
            f"v={self.velocity}, rt={self.reaction_time}, "
            f"fa={front_agent_info}, ba={back_agent_info})"
        )

    def dist_to_front_agent(self):
        if self.front_agent == None:
            return None

        else: #hay otro agente adelante
            return abs(self.position - self.front_agent.position - self.length)


    def dist_to_back_agent(self):
        if self.back_agent == None:
            return None

        else: #hay otro agent atras
            return abs(self.back_agent.position - self.position - self.back_agent.length)

    def speed_variation(self):
        if self.dist_to_front_agent() == None or self.dist_to_front_agent() >= 20:
            self.velocity = random.normalvariate(self.velocity, 5/3.6)
            if self.velocity < 0:
                self.velocity = 0

            # entran todos con media 17 y desvio 1, buscan llegar a la velocidad deseada dada por la triangular 
            '''
            la distribución de variacion de velocidad viene dada por una normal con media 
            la diferencia entre la velocidad deseada y la actual multiplicado por 1/3 ponele para que sea realista
            y desvio (gio dijo 1 ) hay que ver que onda

            '''

    def reduce_speed(self):
        # si se encuentra "cerca" del agente de adelante, reducirá su velocidad mediante una distribución exponencial con media 1.
        if self.dist_to_front_agent() is not None and self.dist_to_front_agent() / (self.velocity - self.front_agent.velocity) < 1:   

            reduction = (self.front_agent.velocity - self.velocity) /(1 - stats.expon.rvs(scale=self.reaction_time))

            # verificamos que sea una reducción posible para un agente humano. 
            if reduction < -4:
                #Imposible que frene un humano
                self.collision = True
    
            else:
                self.velocity += reduction

            #CHEQUEAR SI PUEDE PASAR ESTO...
            if self.velocity < 0:
                self.velocity = 0  
        

        # si se encuentra "lejos" del agente de adelante, reducirá su velocidad mediante una distribución exponencial con media 3.
        elif self.dist_to_front_agent() is not None and self.dist_to_front_agent() / (self.velocity - self.front_agent.velocity) < 2 and self.dist_to_front_agent() / (self.velocity - self.front_agent.velocity) >= 1:
            
            reduction = (self.front_agent.velocity - self.velocity) /(2 - stats.expon.rvs(scale=self.reaction_time))

            # verificamos que sea una reducción posible para un agente humano. 
            if reduction < -4:
                #Imposible que frene un humano
                self.collision = True
                
            else:
                self.velocity += reduction

            #CHEQUEAR SI PUEDE PASAR ESTO...
            if self.velocity < 0:
                self.velocity = 0
    

    def move(self):
        self.position = self.position + self.velocity * 1 
    
    def get_position(self):
        return self.position

    def update(self):
        self.move()
        self.reduce_speed()
        self.speed_variation()

        self.time += 1

class Road:
    
    def __init__(self, m:int, c:bool):
        self.km = m
        self.agents = []
        self.time = 0
        self.total_time = 100
        self.congestion = c
    
    def add_agent(self, rate):
        # Si no hay agentes en la Gral.Paz, agregamos el primer agente
        if not self.agents:
            print("Agregando primer agente...")
            self.agents.append(Agent())
            print("Primer agente agregado: " + str(self.agents[0]))
            
            self.time_to_next_arrival = stats.expon.rvs(scale=1/rate)

        else:
            # Verificamos el tiempo desde el último agente
            if self.time - self.agents[-1].arrival_time > self.time_to_next_arrival:
                print("Agregando agente nro. ", len(self.agents))
                # Agregamos un nuevo agente a la lista
                new_agent = Agent()
                self.agents.append(new_agent)
                
                new_agent.arrival_time = self.time
                self.time_to_next_arrival = stats.expon.rvs(scale=1/rate)
                
                if len(self.agents) == 2:
                    position_new_agent = self.agents.index(new_agent)
                    new_agent.front_agent = self.agents[position_new_agent - 1]
                    self.agents[position_new_agent - 1].back_agent = new_agent

                # Configuramos el front y back car para el nuevo agente
                elif len(self.agents) >= 2:
                    position_new_agent = self.agents.index(new_agent)
                    new_agent.front_agent = self.agents[position_new_agent - 1]
                    self.agents[position_new_agent - 1].back_agent = new_agent

        self.update_road()

    def time_lapse(self):
        while self.time < self.total_time:
            if self.congestion == True:
                # Agrega autos con distribución exponencial negativa con media = 15
                self.add_agent(15)
            else:
                # Agrega autos con distribución exponencial negativa con media = 45
                self.add_agent(45)
        
    
    def update_road(self):
        self.time += 1

        removed = set()
        for agent in self.agents:
            agent.update()
            print("Estado agente nro:", self.agents.index(agent), "->", agent)
            # print("Posición del agente:", self.agents.index(agent), "->", agent.get_position())
            
            #Si el agente llega al final de la carretera lo eliminamos
            if agent.get_position() > self.km:
                removed.add(agent)

            #Reasignamos el front y back car de los agentes extremos de la lista
            if len(self.agents) > 0:
                self.agents[0].front_agent = None

            if agent.collision == True:
                removed.add(agent)
                removed.add(agent.front_agent)

        # reasingo la posiciones de la lista
        for agent in removed:
            # Si hay choque lo eliminamos y reasignamos los front y back car
            self.agents.remove(agent)
        
        for agent in self.agents:
            if self.agents.index(agent) != 0:
                        agent.front_agent = self.agents[self.agents.index(agent) - 1]
            else:
                agent.front_agent = None
                
            if self.agents.index(agent) != (len(self.agents) - 1):
                agent.back_agent = self.agents[self.agents.index(agent) + 1]
            else:
                agent.back_agent = None

        self.time_lapse()


def animate_simulation():
    # Crear una figura de Matplotlib para la animación
    fig, ax = plt.subplots()
    
    # Configurar los ejes de la gráfica
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    
    # Función de inicialización de la animación
    def init():
        return []
    
    # Función de actualización de la animación
    def update(frame):
        ax.clear()

        # Dibujar el pasto verde arriba de la carretera
        ax.fill_between([0, width], 0, height // 3, color=green)

        # Carretera gris
        ax.fill_between([0, width], height // 3, 2 * height // 3, color=gray)

        # Dibujar el pasto verde abajo de la carretera
        ax.fill_between([0, width], 2 * height // 3, height, color=green)

        # Líneas blancas en el medio de la carretera
        for i in range(num_lines):
            x = (i + 1) * gap - line_width // 2
            ax.fill_between([x, x + line_width], height // 2 - line_height // 2, height // 2 + line_height // 2, color=white)

        # Dibujar los agentes en la carretera
        for agent in general_paz.agents:
            ax.fill_between([agent.get_position(), agent.get_position() + agent.length], height // 3 - 10, height // 3 + 10, color=black)

        return []
    
    # Crear la animación
    ani = animation.FuncAnimation(fig, update, frames=range(100), init_func=init, blit=True)
    
    # Mostrar la animación en una ventana de Matplotlib
    plt.show()

# ...

# Salir del juego
pygame.quit()
sys.exit()
