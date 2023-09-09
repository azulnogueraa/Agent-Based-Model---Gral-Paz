class Agent(pygame.sprite.Sprite):

    def __init__(self):
        self.position = 0                                             
        self.max_velocity = 80/3.6                                    
        self.length = 5                                               
        self.front_agent = None                                      
        self.back_agent = None                                       
        self.collision = False                                        
        self.desired_velocity = random.triangular(30/3.6, 100/3.6, 70/3.6)
        self.velocity = random.normalvariate(17, 1)
        self.time = 0
        self.arrival_time = 0
        self.reaction_time = random.normalvariate(0.25, 0.005) 
    
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
        if self.dist_to_front_agent() is not None and self.dist_to_front_agent() / (self.velocity - self.front_agent.velocity) >= 3:
            # si se encuentra "lejos" del agente de adelante, buscará acercarse a la velocidad deseada.
            self.velocity += random.normalvariate((self.desired_velocity - self.velocity) * 1/3, 1)

        elif self.dist_to_front_agent() is not None and self.dist_to_front_agent() / (self.velocity - self.front_agent.velocity) < 3 and self.dist_to_front_agent() / (self.velocity - self.front_agent.velocity) >= 2:
            #Si se encuentra a distancia media del agente de adelante, solo puede acercarse a la velocidad deseada si es menor a la actual.
            if self.velocity > self.desired_velocity:
                self.velocity += random.normalvariate((self.front_agent.velocity - self.velocity) * 1/3, 1)



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