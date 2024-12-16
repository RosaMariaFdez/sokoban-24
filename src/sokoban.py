
import sys
from LevelParser import LevelParser
from Nodo import Nodo
import algoritmo_busqueda


'''*********************************************************************
* Method name: detect_param
* Description: detecta los argumentos de entrada para las tareas

* Calling arguments: argumentos de entrada por consola
* Return value: nivel (caso -l / --level), -s y -d para la tarea 3
* Required Files: librería sys (importada)
*********************************************************************'''
def detect_param(sys_argv):
    level = ""  #string para guardar el nivel
    
    if sys.argv[1] != "T1" and sys.argv[1] != "T2S" and sys.argv[1] != "T2T" and sys.argv[1] != "T3":
        print("Error, no existe esa acción")
        sys.exit(1)

    else:
        level = sys.argv[3]

    return level

'''*********************************************************************
* Method name: print_level_info
* Description: imprime la información que define el nivel (tarea 1) 
* Calling arguments: parser del nivel
* Return value: None
*********************************************************************'''
def print_level_info(level_parser):
    str_walls = str(level_parser.walls).replace(" ", "")
    str_targets = str(level_parser.targets).replace(" ", "")
    str_player = str(level_parser.player).replace(" ", "")
    str_boxes = str(level_parser.boxes).replace(" ", "")

    print("ID:", level_parser.encode_id())
    print("Rows:", level_parser.num_rows)
    print("Columns:", level_parser.num_cols)
    print("Walls:", str_walls)
    print("Targets:", str_targets)
    print("Player:", str_player)
    print("Boxes:", str_boxes)


'''*********************************************************************
* Method name: fsucesor --------------- DEPRECATED, SOLO ESTÁ PARA LA TAREA 2
* Description: genera los sucesores del nivel   
* Calling arguments: level_parser
* Return value: lista de sucesores
*********************************************************************'''
def fsucesor(level_parser):
    acciones = ['u', 'r', 'd', 'l']
    sucesores = []
    
    movimientos = {
        'u': (-1, 0), 'r': (0, 1),   
        'd': (1, 0), 'l': (0, -1)   
    }
    
    for accion in acciones:
        dr, dc = movimientos[accion]
        jugador_nuevo = (level_parser.player[0] + dr, level_parser.player[1] + dc)
        nuevo_estado = level_parser

        # Intentar mover el jugador
        if jugador_nuevo not in level_parser.walls:
            # Si la casilla está vacía, solo se mueve el jugador
            if jugador_nuevo not in level_parser.boxes:
                sucesores.append((accion, nuevo_estado.encode_id2(jugador_nuevo, nuevo_estado.boxes), 1))

            # Si hay una caja intentamos moverla
            else:
                caja_nueva = (jugador_nuevo[0] + dr, jugador_nuevo[1] + dc)
                # Verificar que la casilla siguiente a la caja esté libre
                if caja_nueva not in level_parser.walls and caja_nueva not in level_parser.boxes:

                    nuevas_cajas = level_parser.boxes.copy()
                    nuevas_cajas.remove(jugador_nuevo)
                    nuevas_cajas.append(caja_nueva)
                    nuevas_cajas.sort() #ordenar cajas por si se mueven de fila

                    sucesores.append((accion.upper(), nuevo_estado.encode_id2(jugador_nuevo, nuevas_cajas), 1))

    return sucesores

'''*********************************************************************
* Method name: is_objetive
* Description: comprueba si el nivel es objetivo
* Calling arguments: LevelParser
* Return value: booleano
*********************************************************************'''
def is_objetive(level_parser):
    for box in level_parser.boxes:
        if box not in level_parser.targets:
            return False
    return True

def main():
    # coger el nivel y hacer un level parser (objeto nivel)
    level_str = detect_param(sys.argv)
    level_parser = LevelParser(level_str)

    #Tarea 1
    if sys.argv[1] == "T1":
        print_level_info(level_parser)
    
    #Tarea 2
    elif sys.argv[1] == "T2T":
        goal = is_objetive(level_parser)
        print(str(goal).upper())

    elif sys.argv[1] == "T2S":
        # Imprimir ID del nivel
        print("ID:", level_parser.encode_id())
        # Lista de sucesores
        sucesores_list = fsucesor(level_parser)
        for sucesor in sucesores_list:
            print(f"\t[{sucesor[0]},{sucesor[1]},{sucesor[2]}]")

    #Tarea 3 y 4
    elif sys.argv[1] == "T3":
        estrategia = sys.argv[5]
        max_prof = int(sys.argv[7])

        #nodo inicial
        nodoInicial = Nodo(0, None, level_parser, 0, 0, 0, 'NOTHING')
        if estrategia == 'A*' or estrategia == 'GREEDY':
            nodoInicial.heuristica = nodoInicial.calcular_heuristica()
        nodoInicial.valor = algoritmo_busqueda.valor_estrategia(nodoInicial, estrategia)

        #algoritmo de busqueda
        camino = algoritmo_busqueda.algoritmo_busqueda(nodoInicial, estrategia, max_prof)
        camino.reverse()
        
        print(level_parser.level_str)
        for nodo in camino:
            print(nodo.__str__())
         

if __name__ == "__main__":
    main()
