# -*- coding: utf-8 -*-

import numpy as np
import random
class MAXSATGEN():
  def __init__(self):
    m = random.randint(0,10) + 50
    n = random.randint(0,10) + 100
    self.Matriz = [[0 for x in range(n)] for r in range(m)]
    cota = 0
    for e in self.Matriz:
      auxaux = random.sample(range(0,n-1),5)
      dado1 = (random.randint(0,1) == 0)
      dado2 = (random.randint(0,1) == 0)
      dado3 = (random.randint(0,1) == 0)
      if(dado1):
        e[auxaux[0]] = 1
      else:
        e[auxaux[0]] = -1
      if(dado2):
        e[auxaux[1]] = 1
      else:
        e[auxaux[1]] = -1
      if(dado3):
        e[auxaux[2]] = 1
      else:
        e[auxaux[2]] = -1
      if(random.randint(0,1)==0):
        dado4 = (random.randint(0,1) == 0)
        if(dado4):
          e[auxaux[3]] = 1
        else:
          e[auxaux[3]] = -1
      if(random.randint(0,1)==0):
        dado5 = (random.randint(0,1) == 0)
        if(dado5):
          e[auxaux[4]] = 1
        else:
          e[auxaux[4]] = -1
    numPob = 100
    self.Poblacion = list()
    self.PoblacionAleatoria(numPob,n)
    self.FunFitness = list(map(self.fitness, self.Poblacion))
    SumFitness = sum(self.FunFitness)
    self.ProbRoulette = list(map(lambda a : a / SumFitness, self.FunFitness))
  
  def PoblacionAleatoria(self,numPob,n):
    for i in range(0,numPob):
      aux = list()
      for j in range(0,n):    
        aux.append(random.randint(0,1))
      self.Poblacion.append(aux)
  
  def RecalcularFitness(self):
    self.FunFitness = list(map(self.fitness, self.Poblacion))
    SumFitness = sum(self.FunFitness)
    self.ProbRoulette = list(map(lambda a : a / SumFitness, self.FunFitness))

  def SeleccionRuleta(self):
    aux = list(range(len(self.ProbRoulette)))
    auxpadre1 = np.random.choice(aux,1,p=self.ProbRoulette)[0]
    auxpadre2 = np.random.choice(aux,1,p=self.ProbRoulette)[0]
    return self.Poblacion[auxpadre1],self.Poblacion[auxpadre2]

  def fitness(self,individuo):
    fit = 0
    for e in self.Matriz:
      for i in range(0,len(e)):
        if(e[i] == 1):
          if(individuo[i] == 1):
            fit = fit + 1
            break
          else:
            continue
        if(e[i] == -1):
          if(individuo[i] == 0):
              fit = fit + 1
              break
          else:
            continue
    return fit

  def Mutacion(self,moneda,mutante,especimen):
    if(moneda):
      if(mutante):
        #Displacement mutation
        puntos = random.sample(range(0,len(especimen)-1),2)
        aux = especimen[puntos[0]:puntos[1]]
        mutado = list()
        mutado = (especimen[0:puntos[0]] + aux + especimen[puntos[1]:len(especimen)])
        return mutado
      else:
        return especimen
    else:
      if(mutante):
        #Exchange Mutation
        puntos = random.sample(range(0,len(especimen)-1),2)
        aux = especimen[puntos[0]]
        aux1 = especimen[puntos[1]]
        especimen[puntos[1]] = aux
        especimen[puntos[0]] = aux1
        return especimen
      else:
        return especimen

  def Recombinacion(self,moneda,p1,p2):
    if(moneda):
      #Ordered Crossover
      puntos = random.sample(range(0,len(p1)-1),2)
      mediop1 = p1[puntos[0]:puntos[1]]
      mediop2 =  p2[puntos[0]:puntos[1]]
      hijo1 = p1[0:puntos[0]] + mediop2 + p1[puntos[1]:len(p1)]
      hijo2 = p2[0:puntos[0]] + mediop1 + p2[puntos[1]:len(p1)]
      return hijo1,hijo2
    else:
      #PartiallyMappedCrossover
      puntos = random.sample(range(0,len(p1)-1),2)
      mediop1 = p1[puntos[0]:puntos[1]]
      chromosoma1_1 = p1[0:puntos[0]]
      chromosoma1_2 = p1[puntos[1]:len(p1)]
      mediop2 =  p2[puntos[0]:puntos[1]]
      chromosoma2_1 = p2[0:puntos[0]]
      chromosoma2_2 = p2[puntos[1]:len(p2)]
      hijo1 = chromosoma1_2[::-1] + mediop2 + chromosoma1_1[::-1]
      hijo2 = chromosoma2_2[::-1] + mediop1 + chromosoma2_1[::-1]
      return hijo1,hijo2

  def MejorIndividuo(self):
    mejor = 0
    aux = self.FunFitness[0]
    for i in range(0,len(self.FunFitness)):
      if(self.FunFitness[i] > aux):
        aux = self.FunFitness[i]
        mejor = i
    return mejor

  def AlgoritmoGenetico(self):
    print(Ejemplar.toString())
    i = 0
    while i < 20:
      NuevaPoblacion = list()
      MejorInd = self.MejorIndividuo()
      if(self.FunFitness[MejorInd] == len(self.Matriz)):
        break
      NuevaPoblacion.append(self.Poblacion[MejorInd])
      while(len(NuevaPoblacion) < 25):
        padres = self.SeleccionRuleta()
        hijos = self.Recombinacion(random.randint(0,2)==0,padres[0],padres[1]) 
        hijo1 = hijos[0]
        hijo2 = hijos[1]
        hijo1 = self.Mutacion(random.randint(0,2)==0,random.random() <= 0.2,hijo1)
        hijo2 = self.Mutacion(random.randint(0,2)==0,random.random() <= 0.2,hijo2)
        NuevaPoblacion.append(hijo1)
        NuevaPoblacion.append(hijo2)
      print("generacion " + str(i) + "de 20")
      print("Con mejor individuo satisfaciendo " + str(self.FunFitness[MejorInd]))
      self.Poblacion = NuevaPoblacion
      self.RecalcularFitness()
      self.PoblacionAleatoria(75,len(self.Poblacion[0]))
      i += 1
    print("Mejor individuo despues de ejecutar el algoritmo es : \n" + self.toStringSolucion(self.Poblacion[MejorInd]))
    print("Con " + str(self.FunFitness[MejorInd]) + " clausulas satisfechas de " + str(len(self.Matriz)))

  def toStringSolucion(self,solucion):
    cadena = ""
    for i in range(0,len(solucion)):
      cadena += "x" + str(i) + " = " + str(solucion[i]) + ","
    return cadena

  def toString(self):
    cadena = "Las clausulas son: { "
    primero = False
    primeroAux = False
    for e in self.Matriz:
      if (primero):
        cadena = cadena + " ^ ( "
      else:
        cadena = cadena + " ( "
      for i in range(0,len(e)):
        if(e[i] == 0):
          continue
        else:
          if(e[i] == 1):
            if(primeroAux):
              cadena = cadena + " v x" + str(i)
            else:
              cadena = cadena + " x" + str(i)
              primeroAux = True
          if(e[i] == -1):
            if(primeroAux):
              cadena = cadena + " v ¬x" + str(i)
            else:
              cadena = cadena + " ¬x" + str(i)
              primeroAux = True
      primeroAux = False
      primero = True
      cadena = cadena + " ) "
    return cadena + " }"

Ejemplar = MAXSATGEN()
Ejemplar.AlgoritmoGenetico()
