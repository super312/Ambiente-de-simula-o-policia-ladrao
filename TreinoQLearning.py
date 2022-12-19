# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 08:41:00 2022

@author: super
"""

import pickle
import numpy as np
import time
from TCC_POO_Bruno import Game
from TCC_POO_Bruno import Player

class Treino(Game):
    
    def __init__(self,SIZE):
        
        p1 = Player(0,0)
        p2 = Player(0,0)
        super().__init__(SIZE, p1, p2)
        
        self.q_values = np.zeros((self.p1_gas_maximum+1,self.SIZE,self.SIZE,self.SIZE,self.SIZE,self.SIZE,self.SIZE,4))
        self.rewards = np.full((self.p1_gas_maximum+1,self.SIZE,self.SIZE,self.SIZE,self.SIZE,self.SIZE,self.SIZE),-1)
        self.set_rewards()
        
        pass
    
    def set_rewards(self):
        
        self.gas_reward = 25
        for gn in range(self.p1_gas_maximum+1):
            for gasx in range(self.SIZE):
                for gasy in range(self.SIZE):
                    for tr in range(self.SIZE):
                        for tc in range(self.SIZE):
                            for ir in range(self.SIZE):
                                for ic in range(self.SIZE):
                                    
                                    if gn == 0:
                                        self.rewards[gn,gasx,gasy,tr,tc,ir,ic] = -50
                                    elif tr == ir and tc == ic and not self.arena.is_wall(tr,tc):
                                        self.rewards[gn,gasx,gasy,tr,tc,ir,ic] = 50
                                    elif gasx == ir and gasy == ic and not self.arena.is_wall(tr,tc):
                                        self.rewards[gn,gasx,gasy,tr,tc,ir,ic] = self.gas_reward
                                    
                                    
        #print(self.rewards)
    
    
    def terminal_state(self,gas,gasx,gasy,enemy_x,enemy_y): #OK
        
        if gas == 0:
            return True
        
        if self.rewards[gas,gasx,gasy,enemy_x,enemy_y,self.p1.x,self.p1.y] == -1 or self.rewards[gas,gasx,gasy,enemy_x,enemy_y,self.p1.x,self.p1.y] == self.gas_reward:
            return False
        else:
            return True
        pass
    
    def starting_location(self,gas,gasx,gasy,enemy_x,enemy_y): #OK
        
        self.p1.y = np.random.randint(self.SIZE)
        self.p1.x = np.random.randint(self.SIZE)
        
        while self.terminal_state(gas,gasx,gasy,enemy_x,enemy_y) or self.arena.is_wall(self.p1.x,self.p1.y):
            self.p1.y = np.random.randint(self.SIZE)
            self.p1.x = np.random.randint(self.SIZE)

        
        pass
    
    def next_action(self,gas,gasx,gasy,enemy_x,enemy_y,epsilon): #OK
        
        if np.random.random() < epsilon:
            
            a0 = self.q_values[gas,gasx,gasy,enemy_x,enemy_y,self.p1.x, self.p1.y,0]
            a1 = self.q_values[gas,gasx,gasy,enemy_x,enemy_y,self.p1.x, self.p1.y,1]
            a2 = self.q_values[gas,gasx,gasy,enemy_x,enemy_y,self.p1.x, self.p1.y,2]
            a3 = self.q_values[gas,gasx,gasy,enemy_x,enemy_y,self.p1.x, self.p1.y,3]
            
            if a0 == 0 and a1 == 0 and a2 == 0 and a3 == 0:
                return np.random.randint(4)
            
            return np.argmax(self.q_values[gas,gasx,gasy,enemy_x,enemy_y,self.p1.x, self.p1.y])
        else:
            return np.random.randint(4)
        pass
    
    def treino(self,eps,generations,timelimit): #OK
        epsilon = eps
        epsilon_inicial = eps
        epsilon_final = 0.9
        
        discount_factor = 0.75 #lambda
        learning_rate = 0.9 #alpha
        
        start_time = time.time()
        
        total_steps = 0
        for gens in range(generations):
            
            p = gens / generations
            
            epsilon = epsilon_inicial + p * (epsilon_final - epsilon_inicial)
            
            enemy_x = np.random.randint(self.SIZE)
            enemy_y = np.random.randint(self.SIZE)
            
            while self.arena.is_wall(enemy_x, enemy_y):
                enemy_y = np.random.randint(self.SIZE)
                enemy_x = np.random.randint(self.SIZE)
            
            self.p2.x = enemy_x
            self.p2.y = enemy_y
            
            self.p1_current_gas = np.random.randint(self.p1_gas_maximum) + 1
            #self.p1_current_gas = self.p1_gas_maximum
            
            self.gas_x = np.random.randint(self.SIZE)
            self.gas_y = np.random.randint(self.SIZE)
            
            while self.arena.is_wall(self.gas_x,self.gas_y):
                self.gas_y = np.random.randint(self.SIZE)
                self.gas_x = np.random.randint(self.SIZE)
            
            
            gasx = self.gas_x
            gasy = self.gas_y
            
            
            self.starting_location(self.p1_current_gas,gasx,gasy,self.p2.x,self.p2.y)
            
            #if gens % 10000 == 0:
            #    print("gens=%d, ex=%d, ey=%d, px=%d, py=%d, gx=%d, gy=%d, gas=%d" %(gens,enemy_x,enemy_y,self.p1.x,self.p1.y,gasx,gasy,self.p1_current_gas))
            
            step_count = 0
            while(not self.terminal_state(self.p1_current_gas,gasx,gasy,self.p2.x,self.p2.y)):
                
                action = self.next_action(self.p1_current_gas,gasx,gasy,self.p2.x,self.p2.y,epsilon)
                
                old_y,old_x,old_gas,old_gasx,old_gasy,old_ey,old_ex = self.p1.y,self.p1.x,self.p1_current_gas,gasx,gasy,self.p2.y,self.p2.x
                self.p1.move(self.arena, action)
                
                #self.p2.move(self.arena, np.random.randint(4))
                
                step_count += 1
                
                self.update_gas_location()
                gasx = self.gas_x
                gasy = self.gas_y
                
                reward = self.rewards[self.p1_current_gas,gasx,gasy,self.p2.x,self.p2.y,self.p1.x,self.p1.y]
                old_q_value = self.q_values[old_gas,old_gasx,old_gasy,old_ex,old_ey,old_x,old_y,action]
                temporal_diference = reward + (discount_factor * np.max(self.q_values[self.p1_current_gas,gasx,gasy,self.p2.x,self.p2.y,self.p1.x,self.p1.y])) - old_q_value
                
                new_q_value = old_q_value + (learning_rate * temporal_diference)
                self.q_values[old_gas,old_gasx,old_gasy,old_ex,old_ey,old_x,old_y,action] = new_q_value
                
                totaltime = (time.time() - start_time)
                if totaltime > timelimit:
                    break
            
            total_steps += step_count
            if totaltime > timelimit:
                break
        
            
        
        
        totaltime = (time.time() - start_time)
        
        txtname = "size_" + str(self.SIZE) + "_epsilon_" + str(epsilon_inicial) + "_geracoes_" + str(generations) + "_qvalues.csv"
        
        pickle.dump(self.q_values, open(txtname,"wb"))
        #print("Treino completo salvo em " + txtname)
        return (totaltime,total_steps/generations)
        pass
    
    
    
    pass

#treino = Treino(6)
#print(treino.treino(0.3,1000000))



