# -*- coding: utf-8 -*-
import itertools

from simpleai.search import (CspProblem, backtrack, min_conflicts,
                             MOST_CONSTRAINED_VARIABLE, 
                             LEAST_CONSTRAINING_VALUE, 
                             HIGHEST_DEGREE_VARIABLE)

armaduras = ['Verde','Blanca','Amarilla','Roja','Azul']
vikingos = ['Agnar', 'Bjarni', 'Cnut', 'Diarf', 'Egil']
escudos = ['Cruz','Pajaros','Dragon','Arboles','Trebol']
armas = ['Martillo','Hacha','Lanza','Espada','Garrote']
amuletos = ['Anillo','Cinturon','Pulsera','Moneda','Pendiente']              

variables = armaduras + vikingos + escudos + armas + amuletos
dominios = {variable: list(range(1,6)) for variable in variables}

dominios['Agnar'] = [1,]

dominios['Escudo'] = [3,]

def izquierda_derecha(variables, values):
	return values[0] + 1 == values[1]
	
def al_lado(variables, values):
	return abs(values[0]-values[1]) == 1

def misma_posicion(variables,values):
	return values[0] == values[1]
	
def diferentes(variables, values):
	return values[0] != values[1]
	
restricciones = []
restricciones.append((('Roja','Bjarni'),misma_posicion))
restricciones.append((('Pendiente','Egil'),misma_posicion))
restricciones.append((('Trebol','Diarf'),misma_posicion))
restricciones.append((('Garrote','Cnut'),misma_posicion))
restricciones.append((('Verde','Cruz'),misma_posicion))
restricciones.append((('Verde','Blanca'),izquierda_derecha))
restricciones.append((('Martillo','Anillo'),misma_posicion))
restricciones.append((('Amarilla','Hacha'),misma_posicion))
restricciones.append((('Cinturon','Hacha'),al_lado))
restricciones.append((('Lanza','Pulsera'),al_lado))
restricciones.append((('Espada','Escudo'),misma_posicion))
restricciones.append((('Lanza','Arboles'),al_lado))
restricciones.append((('Agnar','Azul'),al_lado))

for i,j in itertools.combinations(armas, 2):
    restricciones.append(((i, j), diferentes))
for i,j in itertools.combinations(armaduras, 2):
    restricciones.append(((i, j), diferentes))
for i,j in itertools.combinations(vikingos, 2):
    restricciones.append(((i, j), diferentes))
for i,j in itertools.combinations(escudos, 2):
    restricciones.append(((i, j), diferentes))
for i,j in itertools.combinations(amuletos, 2):
    restricciones.append(((i, j), diferentes))

def resolver(metodo_busqueda, iteraciones):
        #problema = CspProblem(variables, dominios, restricciones)
        if metodo_busqueda == 'backtrack':
                return backtrack(CspProblem(variables, dominios, restricciones))
        if metodo_busqueda == 'min_conflicts':
                return min_conflicts(CspProblem(variables, dominios, restricciones), iterations_limit = iteraciones)
        

if __name__ == '__main__':
        problema = CspProblem(variables, dominios, restricciones)

        resultado = backtrack(problema)
        print(resultado)
        print('backtrack:')
        for i in range(1,6):
                print('Posicion:', i)
                for j in resultado:
                        if i == resultado[j]:
                                print(j)
				
        resultado = min_conflicts(problema, iterations_limit=500)
        print(resultado)
        print
        print('min conflicts:')
        for i in range(1,6):
                print('Posicion:', i)
                for j in resultado:
                        if i == resultado[j]:
                                print(j)
