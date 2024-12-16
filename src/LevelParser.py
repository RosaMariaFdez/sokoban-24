import hashlib

'''*********************************************************************
* Class name: LevelParser
* Description: clase para parsear el nivel
* Methods: parse_level, encode_id, validate_level, walls_closed
* Attributes: level_str, rows, num_rows, num_cols, walls, targets, player, boxes, invalid
*********************************************************************'''

class LevelParser:
    def __init__(self, level_str):
        self.level_str = level_str
        self.rows = str(level_str).split('\\n')
        self.num_rows = len(self.rows)
        self.num_cols = max(len(row) for row in self.rows)
        self.walls = []     #lista para coords de paredes
        self.targets = []    #lista para coords de objetivos
        self.player = (0,0)
        self.boxes = []      #lista para coords de cajas
        self.invalid = []   #lista para coords invalidos
        self.parse_level()
        self.id = self.encode_id()

    '''*********************************************************************
    * Method name: set_player
    * Description: actualiza el jugador en nueva posición y actualiza el id
    * Calling arguments: player
    * Return value: None
    *********************************************************************'''
    def set_player(self, player):
        self.player = player
        self.id = self.encode_id()
    
    '''*********************************************************************
    * Method name: set_boxes
    * Description: actualiza las cajas en nueva posición y actualiza el id
    * Calling arguments: boxes
    * Return value: None
    *********************************************************************'''
    def set_boxes(self, boxes):
        self.boxes = boxes
        self.id = self.encode_id()

    '''*********************************************************************
    * Method name: parse_level
    * Description: parsea el string del nivel, identifica los caracteres 
    * y agrupa las coordenadas de las paredes, objetivos y cajas en listas
    * Calling arguments: argumentos de la clase
    * Return value: modifica los argumentos de la clase
    * Required Files: 
    *********************************************************************'''
    def parse_level(self):
        for i, row in enumerate(self.rows):
            for j, cell in enumerate(row):
                if cell == '#':
                    self.walls.append((i, j))
                elif cell == '.':
                    self.targets.append((i, j))
                elif cell == '@':
                    self.player = (i, j)
                elif cell == '$':
                    self.boxes.append((i, j))
                elif cell == '+':
                    self.player = (i, j)
                    self.targets.append((i, j))
                elif cell == '*':
                    self.boxes.append((i, j))
                    self.targets.append((i, j))
                else:
                    if cell != ' ':
                        self.invalid.append((i, j))

    '''*********************************************************************
    * Method name: encode_id
    * Description: codifica el id del nivel
    * Calling arguments: argumentos de la clase
    * Return value: id del nivel
    * Required Files: librería hashlib (importada)
    *********************************************************************'''
    def encode_id(self):
        str_boxes = str(self.boxes).replace(" ", "")
        str_player = str(self.player).replace(" ", "")
        return hashlib.md5((str_player + str_boxes).encode()).hexdigest().upper()

    '''*********************************************************************
    * Method name: encode_id2
    * Description: codifica el id del nivel (pasando los datos como argumentos)
    * Calling arguments: player, boxes
    * Return value: id del nivel
    * Required Files: librería hashlib (importada)
    *********************************************************************'''
    def encode_id2(self, player, boxes):
        str_boxes = str(boxes).replace(" ", "")
        str_player = str(player).replace(" ", "")
        return hashlib.md5((str_player + str_boxes).encode()).hexdigest().upper()

    '''*********************************************************************
    * Method name: validate_level
    * Description: valida el nivel - no se usa al final en los test
    * Calling arguments: argumentos de la clase
    * Return value: booleano, mensaje de error
    *********************************************************************'''
    def validate_level(self):
        if len(self.invalid) != 0:
            return False, "Error: Caracteres invalidos en "+ str(self.invalid)
        if len(self.boxes) != len(self.targets):
            return False, "Error: El número de cajas y el de objetivos es diferente"
        if len(self.player) != 2:
            return False, "Error: Hay más de un jugador"
        return True, None


