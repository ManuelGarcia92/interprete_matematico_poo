class Logica:
    def __init__(self):
        self.cursor_y = 0
        self.cursor_x = 0
        self.cursor_x_deseado = 0
        self.ancho_max = 99
        self.matriz = [[]]

    def _actualizar_x_deseado(self):
        self.cursor_x_deseado = self.cursor_x

    def arriba(self):
        if self.cursor_y > 0:
            self.cursor_y -= 1
            self.cursor_x = min(self.cursor_x_deseado, len(self.matriz[self.cursor_y]))

    def abajo(self):
        if self.cursor_y < len(self.matriz) - 1:
            self.cursor_y += 1
            self.cursor_x = min(self.cursor_x_deseado, len(self.matriz[self.cursor_y]))
        
    def izquierda(self):
        if self.cursor_x > 0:
            self.cursor_x -= 1
        elif self.cursor_x == 0 and self.cursor_y > 0:
            self.cursor_y -= 1
            self.cursor_x = len(self.matriz[self.cursor_y])
        self._actualizar_x_deseado()
                    
    def derecha(self):
        if self.cursor_x < len(self.matriz[self.cursor_y]):
            self.cursor_x += 1
        elif self.cursor_x == len(self.matriz[self.cursor_y]) and self.cursor_y < len(self.matriz) - 1:
            self.cursor_y += 1
            self.cursor_x = 0
        self._actualizar_x_deseado()
            
    def principio_linea(self):
        self.cursor_x = 0
        self._actualizar_x_deseado()

    def fin_linea(self):
        self.cursor_x = len(self.matriz[self.cursor_y])
        self._actualizar_x_deseado()

    def primera_linea(self):
        self.cursor_y = 0
        self.cursor_x = min(self.cursor_x_deseado, len(self.matriz[self.cursor_y]))

    def ultima_linea(self):
        self.cursor_y = len(self.matriz) - 1
        self.cursor_x = min(self.cursor_x_deseado, len(self.matriz[self.cursor_y]))

    def añadir_linea(self):
        linea_actual = self.matriz[self.cursor_y]
        resto = linea_actual[self.cursor_x:]
        del linea_actual[self.cursor_x:]
        self.matriz.insert(self.cursor_y + 1, resto)
        self.cursor_y += 1
        self.cursor_x = 0
        self.cursor_x_deseado = 0
                                                
    def tabulacion(self):
        linea = self.matriz[self.cursor_y]
        n = 4 - (self.cursor_x % 4)
        libre = self.ancho_max - len(linea)
        if libre > 0:
            self.añadir_caracter([' '] * min(n, libre))
        else:
            self.cursor_x = min(self.cursor_x + n, len(linea))
            self._actualizar_x_deseado()
            
    def tabulacion_inversa(self):
        if self.cursor_x == 0:
            return
        n = self.cursor_x % 4 or 4
        for _ in range(n):
            if self.matriz[self.cursor_y] and self.matriz[self.cursor_y][0] == " ":
                self.matriz[self.cursor_y].pop(0)
                self.cursor_x -= 1
        self._actualizar_x_deseado()

    def añadir_caracter(self, entrada):
        linea = self.matriz[self.cursor_y]
        if len(linea) + len(entrada) > self.ancho_max:
            return
        self.matriz[self.cursor_y][self.cursor_x:self.cursor_x] = list(entrada)
        self.cursor_x += len(entrada)
        self._actualizar_x_deseado()

    def eliminar_caracter(self): 
        if self.cursor_x > 0:
            self.matriz[self.cursor_y].pop(self.cursor_x - 1)
            self.cursor_x -= 1
        elif self.cursor_x == 0 and self.cursor_y > 0:
            if len(self.matriz[self.cursor_y - 1]) == 0 or len(self.matriz[self.cursor_y]) == 0:
               indice_a_borrar = self.cursor_y - 1 if len(self.matriz[self.cursor_y - 1]) == 0 else self.cursor_y
               self.matriz.pop(indice_a_borrar)
               self.cursor_y -= 1
               self.cursor_x = len(self.matriz[self.cursor_y])
        self._actualizar_x_deseado()
            
   
