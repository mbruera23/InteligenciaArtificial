from simpleai.search import breadth_first, SearchProblem, astar, greedy, depth_first
from simpleai.search.viewers import BaseViewer

n = 3
salida = (n,n)
class Problem(SearchProblem):
    def cost(self, state1, action, state2):
        return 1
    
    def is_goal(self, state):
        #Si alguno esta fuera de la salida devuelvo falso
        for ap in state[1:]:
            if (ap[0],ap[1]) != salida:
                return False
            if ap[2] > 500:
                return False
        #Devuelvo verdadero si ninguna de las anteriores se cumple
        return True
    
    def actions(self, state):
        acciones = []
        destruido = False
        for ap in state[1:]:
            if ap[2] > 500:
                destruido = True
        if not destruido:
            #rx y ry son las coordenadas del robot
            rx, ry = state[0][0], state[0][1]
            #acciones de mover solamente al robot
            if rx != 0:
                acciones.append(('robot', (rx - 1, ry)))
            if rx != n:
                acciones.append(('robot', (rx + 1, ry)))
            if ry != 0:
                acciones.append(('robot', (rx, ry - 1)))
            if ry != n:
                acciones.append(('robot', (rx, ry + 1)))  
            i = 1
            while i < len(state):
                #si el aparato esta en la misma posicion que el robot y no estan en la salida
                if (rx,ry) == (state[i][0],state[i][1]) and (rx,ry) != salida:
                    #enfrio el aparato y queda en su lugar
                    acciones.append(('extintor', (rx, ry, 175)))
                    #acciones de mover el aparato
                    if rx != 0:
                        acciones.append((i, (rx - 1, ry, state[i][2])))
                    if rx != n:
                        acciones.append((i, (rx + 1, ry, state[i][2])))
                    if ry != 0:
                        acciones.append((i, (rx, ry - 1, state[i][2])))
                    if ry != n:
                        acciones.append((i, (rx, ry + 1, state[i][2])))
                i += 1
        return acciones
                                               
    def result(self, state, action):
        state = list(state)
        identif = action[0]
        
        #si algun aparato se mueve junto con el robot
        if (identif != 'robot') and (identif != 'extintor'):
            state[identif] = action[1]
        #si usa el extintor
        elif identif == 'extintor':
            i=1
            while i < len(state):
                #si la ubicacion del aparato y la del robot es la misma lo enfria
                if (state[i][0],state[i][1]) == (state[0][0],state[0][1]):
                    state[i] = (action[1][0], action[1][1], state[i][2] - action[1][2])
                i+=1

        #muevo el robot (sea cual sea la accion a ejecutar,
        #la posicion del robot va a ser siempre action[1][0] y action[1][1])
        state[0] = (action[1][0], action[1][1])
        
        #caliento todos los aparatos que no esten en la salida
        i = 1
        while i < len(state):
            if (state[i][0], state[i][1]) != salida:
                state[i] = (state[i][0], state[i][1], state[i][2] + 25)
            i += 1
        return tuple(state)

    def heuristic(self, state):
        #calculo la suma de la distancia mas corta de cada aparato con la salida
        distancia = 0
        for ap in state[1:]: 
            distancia += n*2 - ap[0] - ap[1]
        return distancia

def resolver(metodo_busqueda, posiciones_aparatos):
	Inicial = [(3,3)]
	for ap in posiciones_aparatos:
		Inicial.append((ap[0], ap[1], 300))
	if metodo_busqueda == "breadth_first":
		return breadth_first(Problem(tuple(Inicial)), graph_search=True)
	if metodo_busqueda == "astar":
		return astar(Problem(tuple(Inicial)), graph_search=True)
	if metodo_busqueda == "greedy":
		return greedy(Problem(tuple(Inicial)), graph_search=True)
	if metodo_busqueda == "depth_first":
		return depth_first(Problem(tuple(Inicial)), graph_search=True)
        
if __name__ == '__main__':
	Inicial = ((3,3),(1,2,300),(2,0,300),(3,0,300))
	print ('Prueba breadth_first')	
	visor = BaseViewer()
	resultado = breadth_first(Problem(Inicial), graph_search = True, viewer = visor)
	print (resultado.path())
	print (resultado.state)
	print (resultado.cost)
	print (visor.stats)
