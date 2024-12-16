from Frontera import Frontera
from Nodo import Nodo

import sokoban
'''*********************************************************************
* Method name: algoritmo_busqueda
* Description: algoritmo de búsqueda para resolver el problema
* Calling arguments: nodoInicial, estrategia, max_prof
* Return value: camino de nodo inicial a solucion
*********************************************************************'''
def algoritmo_busqueda(nodoInicial, estrategia, max_prof):
    
    estrategia = estrategia.upper()
    id_nodo = 0

    if estrategia == 'DFS':
        nodoInicial.valor = 1.0

    frontera = Frontera()
    
    visitados = set()
    solucion = False
    
    frontera.add(nodoInicial)

    while not frontera.is_empty() and not solucion:
        nodo = frontera.pop()

        if sokoban.is_objetive(nodo.estado):
            solucion = True
        
        elif nodo.estado.id not in visitados and nodo.profundidad < int(max_prof):
            visitados.add(nodo.estado.id)
            
            for sucesor in nodo.generar_sucesores():
                id_nodo += 1
                                    #nodo id, padre, estado, profundidad, costo, heuristica, accion
                nodo_sucesor = Nodo(id_nodo, nodo, sucesor.estado, nodo.profundidad + 1, nodo.costo + 1, 0, sucesor.accion)
                
                if estrategia == 'A*' or estrategia == 'GREEDY': #solo t4
                    nodo_sucesor.heuristica = nodo_sucesor.calcular_heuristica()
                
                nodo_sucesor.valor = valor_estrategia(nodo_sucesor, estrategia)
                
                frontera.add(nodo_sucesor) 
    
    camino = []
    if solucion:
        camino = nodo.funcion_camino()
    
    return camino #camino vacío no hay solución

'''*********************************************************************
* Method name: valor_estrategia
* Description: calcula el valor según la estrategia
* Calling arguments: nodo, estrategia
* Return value: valor
*********************************************************************'''
def valor_estrategia(nodo, estrategia):
    valor = 0.0
    if estrategia == 'A*':
        valor = nodo.costo + nodo.heuristica
    elif estrategia == 'GREEDY':
        valor = nodo.heuristica
    elif estrategia == 'BFS':
        valor = nodo.profundidad
    elif estrategia == 'DFS':
        valor = 1/(1 + nodo.profundidad)
    elif estrategia == 'UC':
        valor = nodo.costo
    
    return valor

