import Nodo
import heapq
'''*********************************************************************
* Class name: Frontera
* Description: clase para manejar frontera
* Methods: add, pop, is_empty, length
* Attributes: frontera
*********************************************************************'''
class Frontera:
    def __init__(self):
        self.frontera = []
        heapq.heapify(self.frontera)

    '''*********************************************************************
    * Method name: add
    * Description: añade un nodo a la frontera
    * Calling arguments: nodo
    * Using libraries: heapq
    *********************************************************************'''
    def add(self, nodo : Nodo)-> None:
        heapq.heappush(self.frontera, (nodo.valor, nodo.id, nodo))
    
    '''*********************************************************************
    * Method name: pop
    * Description: saca un nodo de la frontera
    * Calling arguments: None
    * Using libraries: heapq
    * Return value: nodo
    *********************************************************************'''
    def pop(self) -> Nodo:
        _, _, nodo = heapq.heappop(self.frontera)
        return nodo
    
    def is_empty(self) -> bool:
        return len(self.frontera) == 0
    
    def length(self) -> int:
        return len(self.frontera)
    
    
