import math
import copy

'''*********************************************************************
* Class name: Nodo
* Description: clase para manejar nodos con métodos para generar sucesores, 
* calcular heurística, valor y camino
* Methods: generar_sucesores, calcular_heuristica, funcion_camino
* Attributes: id, parent, estado, profundidad, costo, heuristica, accion, valor
*********************************************************************'''
class Nodo:
    def __init__(self, id: int, parent: 'Nodo | None', estado: 'Estado', profundidad: int, 
                 costo: float, heuristica: float = 0.0, accion: 'str' = 'NOTHING'):
        self.id = id
        self.parent = parent
        self.estado = estado
        self.profundidad = profundidad
        self.costo = costo
        self.heuristica = heuristica
        self.accion = accion
        self.valor = 0.0 #se calcula en algoritmo_busqueda
    
    '''*********************************************************************
    * Method name: __lt__
    * Description: compara dos nodos de igual valor
    * Calling arguments: self, other
    * Return value: booleano
    *********************************************************************'''
    def __lt__(self,other):
        if self.valor == other.valor:
            return self.id < other.id

    '''*********************************************************************
    * Method name: redondear_tercer_decimal
    * Description: redondea el tercer decimal
    * Calling arguments: valor
    * Return value: valor redondeado
    *********************************************************************'''
    def redondear_tercer_decimal(self, valor):
        aux_value = valor * 1000
        tercer_decimal = int(aux_value) % 10
        if tercer_decimal >= 5:
            return math.ceil(valor * 100) / 100
        else:
            return math.floor(valor * 100) / 100


    '''*********************************************************************
    * Method name: __str__
    * Description: convierte el nodo al formato requerido de salida, 
    *               REDONDEO A 2 decimales
    * Calling arguments: self
    * Return value: string
    *********************************************************************'''    
    def __str__(self) -> str:
        costo_redondeado = round(self.costo, 2)
        heuristica_redondeada = round(self.heuristica, 2)
        valor_redondeado = round(self.valor, 2)

        #<Node ID>, <State ID>, <Parent ID>, <Accion>, <Profundidad>, <Costo>, <Heuristica>, <Valor>
        return (f"{self.id}, {self.estado.id}, {self.parent.id if self.parent else 'None'}, {self.accion}, "
                f"{self.profundidad}, {costo_redondeado:.2f}, {heuristica_redondeada:.2f}, {self.redondear_tercer_decimal(self.valor):.2f}")


    '''*********************************************************************
    * Method name: generar_sucesores
    * Description: genera los sucesores del nodo
    * Calling arguments: argumentos de la clase y del estado del nodo (levelParser)
    * Return value: lista de nodos
    *********************************************************************'''
    def generar_sucesores(self):
        acciones = ['u', 'r', 'd', 'l'] #arriba, derecha, abajo, izquierda
        sucesores = [] 
        
        #diccionario de movimientos (coords)
        movimientos = {
            'u': (-1, 0), 'r': (0, 1),   
            'd': (1, 0), 'l': (0, -1)   
        }
        
        for accion in acciones:
            dr, dc = movimientos[accion]    #desplazamiento row, desplazamiento column
            jugador_nuevo = (self.estado.player[0] + dr, self.estado.player[1] + dc)
            nuevo_estado = copy.deepcopy(self.estado) #copia del estado actual, no referencia

            # Intentar mover el jugador
            if jugador_nuevo not in self.estado.walls:
                # Si la casilla está vacía, solo se mueve el jugador
                if jugador_nuevo not in self.estado.boxes:
                    nuevo_estado.set_player(jugador_nuevo) #actualizar jugador
                    nodo_sucesor = Nodo(self.id, self, nuevo_estado, self.profundidad + 1, self.costo + 1, 0, accion)
                    sucesores.append(nodo_sucesor)

                # Si hay una caja intentamos moverla
                else:
                    caja_nueva = (jugador_nuevo[0] + dr, jugador_nuevo[1] + dc)
                    # Verificar que la casilla siguiente a la caja esté libre
                    if caja_nueva not in self.estado.walls and caja_nueva not in self.estado.boxes:

                        #actualizar cajas
                        nuevas_cajas = self.estado.boxes.copy()
                        nuevas_cajas.remove(jugador_nuevo)
                        nuevas_cajas.append(caja_nueva)          
                        nuevas_cajas.sort() #ordenar cajas por si se mueven de fila

                        nuevo_estado.set_player(jugador_nuevo) #actualizar jugador
                        nuevo_estado.set_boxes(nuevas_cajas) #actualizar cajas

                        nodo_sucesor = Nodo(self.id, self, nuevo_estado, self.profundidad + 1, self.costo + 1, 0, accion.upper())
                        sucesores.append(nodo_sucesor)

        return sucesores

    '''*********************************************************************
    * Method name: funcion_camino
    * Description: genera el camino del nodo
    * Calling arguments: argumentos de la clase
    * Return value: lista de nodos
    *********************************************************************'''
    def funcion_camino(self) -> list['Nodo']:
        camino = [self]
        if self.parent is not None:
            camino += self.parent.funcion_camino()
        return camino

    '''*********************************************************************
    * Method name: calcular_heuristica
    * Description: calcula la heurística del nodo
    * Calling arguments: argumentos de la clase
    * Return value: heurística
    *********************************************************************'''
    def calcular_heuristica(self):
        heuristica = 0.0
        for box in self.estado.boxes:
        # distancia mínima de esta caja a objetivo
            heuristica += min(
                abs(box[0] - target[0]) + abs(box[1] - target[1])
                for target in self.estado.targets
        )
        return heuristica


    '''
    #TRUNCANDO A 2
    def truncate(number, decimals=2):
        factor = 10 ** decimals
        return math.trunc(number * factor) / factor

    def __str__(self) -> str:
        return f"{self.id}, {self.estado.id}, {self.parent.id if self.parent else 'None'}, {self.accion}, {self.profundidad}, {truncate(self.costo, 2)}, {truncate(self.heuristica, 2)}, {truncate(self.valor, 2)}"
    '''