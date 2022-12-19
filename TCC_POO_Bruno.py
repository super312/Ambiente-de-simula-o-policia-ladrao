# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 11:37:15 2022

@author: super
"""

import numpy as np
import time
import pickle

class Arena:
    
    def __init__(self,SIZE):
        
        self.SIZE = SIZE
        self.walls = np.zeros((self.SIZE,self.SIZE))
        self.set_walls()
        
        pass
    
    
    def set_walls(self): #OK
        
        #Cria paredes na arena
        if self.SIZE > 7:
            
            #Obstacles number.
            on = int(self.SIZE / 4) #Quantidade de blocos 2x2 que cabem na arena.
            
            if on > 2: #Se houver mais de 2 coloca varios blocos.
                
                posx = 1
                posy = 1
                
                for i in range(on):
                    for j in range(on):
                        
                        if posx < self.SIZE-1 and posy < self.SIZE-1:
                            self.walls[posx,posy] = 1
                            self.walls[posx,posy+1] = 1
                            self.walls[posx+1,posy] = 1
                            self.walls[posx+1,posy+1] = 1
                        
                        posx += 4
                        pass
                    posx = 1
                    posy += 4
                    pass
                
                
                pass
            else: #Padrão de posicionamento
                
                #Primeiro bloco
                
                self.walls[1,1] = 1
                self.walls[1,2] = 1
                self.walls[2,1] = 1
                self.walls[2,2] = 1
                
                #Segundo bloco
                
                self.walls[self.SIZE - 3,1] = 1
                self.walls[self.SIZE - 2,1] = 1
                self.walls[self.SIZE - 3,2] = 1
                self.walls[self.SIZE - 2,2] = 1
                
                #Terceiro bloco
                
                self.walls[1,self.SIZE - 3] = 1
                self.walls[1,self.SIZE - 2] = 1
                self.walls[2,self.SIZE - 3] = 1
                self.walls[2,self.SIZE - 2] = 1
                
                #Quarto bloco
                
                self.walls[self.SIZE - 3,self.SIZE - 3] = 1
                self.walls[self.SIZE - 3,self.SIZE - 2] = 1
                self.walls[self.SIZE - 2,self.SIZE - 3] = 1
                self.walls[self.SIZE - 2,self.SIZE - 2] = 1
                
                pass
            #print(self.walls)
            pass
        elif self.SIZE > 3: 
            
            self.walls[1,1] = 1
            self.walls[self.SIZE-2,1] = 1
            self.walls[1,self.SIZE-2] = 1
            self.walls[self.SIZE-2,self.SIZE-2] = 1
            
            pass
        
        
        pass
    
    def is_wall(self,x,y): #OK
        
        if x < 0 or y < 0 or x >= self.SIZE or y >= self.SIZE:
            return True
    
        if self.walls[x,y] != 0:
            return True
        else:
            return False
        
    def get_size(self):
        return self.SIZE
        pass
    

class Player:
    
    def __init__(self,x,y): #OK
        
        self.actions = ["up","right","down","left"]
        self.x = x
        self.y = y
        
        pass
    
    def move(self,arena,action): #OK
        
        if self.actions[action] == "up" and self.y > 0:
            if arena.is_wall(self.x, self.y-1) == 0:
                self.y -= 1
        elif self.actions[action] == "right" and self.x < arena.get_size() - 1:
            if arena.is_wall(self.x+1, self.y) == 0:
                self.x += 1
        elif self.actions[action] == "down" and self.y < arena.get_size() - 1:
            if arena.is_wall(self.x, self.y+1) == 0:
                self.y += 1
        elif self.actions[action] == "left" and self.x > 0:
            if arena.is_wall(self.x-1, self.y) == 0:
                self.x -= 1
    
    def get_position(self): #OK
        return (self.x,self.y)
    
    def next_action(self,gas,gas_x,gas_y,enemy_x,enemy_y,arena): #OK
        #TODO
        pass
    
    pass

class IAQlearning(Player): #Ia feita em Qlearning.
    
    def __init__(self,SIZE,epsilon,generations,x,y): #OK
        
        super().__init__(x, y)
        
        try:
            txtname = "size_" + str(SIZE) + "_epsilon_" + str(epsilon) + "_geracoes_" + str(generations) + "_qvalues.csv"
            
            self.q_values = pickle.load(open(txtname,"rb"))
        except:
            print("Treino não encontrado")
            
            pass
        
    
    def next_action(self,gas,gasx,gasy,enemy_x,enemy_y,arena): #OK
        
        a0 = self.q_values[gas,gasx,gasy,enemy_x,enemy_y,self.x, self.y,0]
        a1 = self.q_values[gas,gasx,gasy,enemy_x,enemy_y,self.x, self.y,1]
        a2 = self.q_values[gas,gasx,gasy,enemy_x,enemy_y,self.x, self.y,2]
        a3 = self.q_values[gas,gasx,gasy,enemy_x,enemy_y,self.x, self.y,3]
        
        if a0 == 0 and a1 == 0 and a2 == 0 and a3 == 0:
            return np.random.randint(4)
        
        return np.argmax(self.q_values[gas,gasx,gasy,enemy_x,enemy_y,self.x, self.y])
    
        
    pass

class LadraoAleatorio(Player):
    
    def next_action(self,gas,gas_x,gas_y,enemy_x,enemy_y,arena): #OK
        
        return np.random.randint(4)
    
    pass

class Game:
    
    def __init__(self,SIZE,p1,p2): #OK
        
        self.winner = " "
        
        self.arena = Arena(SIZE)
        self.SIZE = SIZE
        
        self.p1 = p1
        self.p2 = p2
        
        self.gas_x = np.random.randint(self.SIZE)
        self.gas_y = np.random.randint(self.SIZE)
        
        while self.arena.is_wall(self.gas_x, self.gas_y):
            self.gas_x = np.random.randint(self.SIZE)
            self.gas_y = np.random.randint(self.SIZE)
        
        self.p1.x = np.random.randint(self.SIZE)
        self.p1.y = np.random.randint(self.SIZE)
        
        while self.arena.is_wall(self.p1.x, self.p1.y):
            self.p1.x = np.random.randint(self.SIZE)
            self.p1.y = np.random.randint(self.SIZE)
            
        self.p2.x = np.random.randint(self.SIZE)
        self.p2.y = np.random.randint(self.SIZE)
        
        while self.arena.is_wall(self.p2.x, self.p2.y):
            self.p2.x = np.random.randint(self.SIZE)
            self.p2.y = np.random.randint(self.SIZE)
            
        
        self.p1_gas_maximum = int(SIZE * 2 + SIZE/2)
        self.p1_current_gas = self.p1_gas_maximum
        
        pass
    
    def play(self, slowdown = True): #OK
        self.history = []
        self.history.append(self.print_state(True))
        
        it = 1
        while not self.end_of_game():
            
            oldl_x,oldl_y = self.p2.x,self.p2.y
            action2 = self.p2.next_action(self.p1_current_gas,self.gas_x, self.gas_y, self.p1.x, self.p1.y,self.arena)
            if it % 4 != 0:
                self.p2.move(self.arena, action2)
            else:
                action2 = -1
            
            if self.end_of_game():
                self.history.append(self.print_state(True,(action2,-1)))
                break
            
            action1 = self.p1.next_action(self.p1_current_gas,self.gas_x, self.gas_y, oldl_x, oldl_y,self.arena)
            self.p1.move(self.arena, action1)
            
            self.update_gas_location()
            
            
            if slowdown:
                for i in range(80): print()
                self.print_state()
                time.sleep(0.5)
                
            self.history.append(self.print_state(True,(action2,action1)))
            it += 1
            
        if slowdown:
            print("Fim de jogo o vencendor é: " + self.winner)
        return self.winner
        pass
    
    def print_state(self,store = False,a = (-1,-1)): #OK?
        
        board = np.full((self.SIZE,self.SIZE),".")
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.arena.is_wall(i, j):
                    board[i,j] = "|"
        board[self.gas_x,self.gas_y] = "G"
        board[self.p2.x,self.p2.y] = "L"
        board[self.p1.x,self.p1.y] = "P"
        
        mapa = "gas = " + str(self.p1_current_gas) + " " + str(a) + "\n"
        for i in range(self.SIZE):
            linha = ""
            for j in range(self.SIZE):
                linha += board[j][i] + " "
            mapa += linha + "\n"
        
        if not store:
            print(mapa)
        else: 
            return mapa
        
        
    def update_gas_location(self): #OK
        
        if (self.gas_x,self.gas_y) == self.p1.get_position():
            self.p1_current_gas = self.p1_gas_maximum
        elif (self.gas_x,self.gas_y) == self.p2.get_position():
            pass
        else:
            self.p1_current_gas -= 1
            return
        
        
        new_gas_x = np.random.randint(self.arena.get_size())
        new_gas_y = np.random.randint(self.arena.get_size())
        
        while self.arena.is_wall(new_gas_x, new_gas_y):
            
            new_gas_x = np.random.randint(self.arena.get_size())
            new_gas_y = np.random.randint(self.arena.get_size())
            
        self.gas_x = new_gas_x
        self.gas_y = new_gas_y
        
        pass
    
    def end_of_game(self): #OK
        
        if self.p1_current_gas <= 0:
            self.winner = "Ladrão"
            return True
        elif self.p1.get_position() == self.p2.get_position():
            self.winner = "Policia"
            return True
        else:
            False
        

class LadraoInteligente(Player):
    
    def next_action(self,gas,gas_x,gas_y,enemy_x,enemy_y,arena):
        
        distancia = [0,0,0,0]
        
        #Testando para cima
        if not arena.is_wall(self.x,self.y-1):
            distancia[0] = abs(self.x-enemy_x) + abs(self.y-1 - enemy_y)
        if not arena.is_wall(self.x+1,self.y):
            distancia[1] = abs(self.x+1 - enemy_x) + abs(self.y - enemy_y)
        if not arena.is_wall(self.x,self.y+1):
            distancia[2] = abs(self.x-enemy_x) + abs(self.y+1 - enemy_y)
        if not arena.is_wall(self.x-1,self.y):
            distancia[3] = abs(self.x-1 - enemy_x) + abs(self.y - enemy_y)
        
        return np.argmax(distancia)
        
        pass
    
    pass










