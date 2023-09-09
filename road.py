class Road:
    
    def __init__(self, m:int, c:bool):
        self.km = m
        self.agents = []
        self.time = 0
        self.total_time = 500
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