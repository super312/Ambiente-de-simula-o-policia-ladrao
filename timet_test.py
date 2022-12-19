# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 11:19:56 2022

@author: super
"""

from TreinoQLearning import Treino
from TCC_POO_Bruno import Game
from TCC_POO_Bruno import IAQlearning
from TCC_POO_Bruno import LadraoAleatorio
from TCC_POO_Bruno import LadraoInteligente
import time
import pickle

gens = [10000,100000,1000000,10000000,100000000]

size = [4,6,8,10]

timelimit = 10800

eps = 0
results = []

p2 = LadraoInteligente(0,0)

for g in gens:
    for s in size:
        
        add = [s,g]
        
        treino = Treino(s)
        #totaltime = treino.treino(eps,g,timelimit)
        
        count = 0
        
        for j in range(100):
            p1 = IAQlearning(s,eps,g, 0, 0)
            gm = Game(s,p1,p2)
            if "Policia" == gm.play(False):
                count += 1
            #else:
                #print("-----------------------------")
                #for h in gm.history:
                    #print(h)
           
        
        add.append(count)
        
        #add.append(totaltime)
        
        results.append(add)
        print(add)
    
    

print("Resumo dos resultados finais: ")
for i in range(len(results)):
    print(results[i])


