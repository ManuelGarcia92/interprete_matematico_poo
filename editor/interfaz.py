from prompt_toolkit.application import get_app

class Interfaz:
    def __init__(self, logica):
        self.logica = logica
        self.scroll_y = 0
        self.scroll_x = 0

    @staticmethod
    def obtener_texto_superior(mensaje_superior):
        app_actual = get_app()
        _, ancho_terminal = app_actual.output.get_size()
        return f"{mensaje_superior}\n{"_" * ancho_terminal}"

    @staticmethod
    def obtener_texto_inferior(mensaje_inferior):
        app_actual = get_app()
        _, ancho_terminal = app_actual.output.get_size()
        return f"{"_" * ancho_terminal}\n {mensaje_inferior}"
    
    def obtener_texto_medio(self):
        lineas = self.logica.matriz
        ancho_numero = len(str(len(lineas)))

        app = get_app()
        alto_terminal, ancho_terminal = app.output.get_size()

        ancho_texto = ancho_terminal - ancho_numero - 5
        lineas_visibles = max(1, alto_terminal - 5)

        self._ajustar_largo(lineas_visibles)
        self._ajustar_ancho(ancho_texto)
        return self._generar_interfaz_editor(lineas_visibles, ancho_texto, ancho_numero)
    
    def _generar_interfaz_editor(self, lineas_visibles, ancho_texto, ancho_numero):
        resultado = []
        for fila in range(lineas_visibles):
            i = self.scroll_y + fila
            if i >= len(self.logica.matriz):
                break
            texto = "".join(self.logica.matriz[i])
            if i == self.logica.cursor_y:
                texto = texto[:self.logica.cursor_x] + "<" + texto[self.logica.cursor_x:]
            texto_visible = texto[self.scroll_x : self.scroll_x + ancho_texto]
            numero_str = str(i+ 1).rjust(ancho_numero)
            resultado.append(('', f"{numero_str} | {texto_visible}\n"))
        return resultado
    
    def _ajustar_largo(self, lineas_visibles):
        if self.logica.cursor_y < self.scroll_y:
            self.scroll_y = self.logica.cursor_y
        elif self.logica.cursor_y >= self.scroll_y + lineas_visibles:
            self.scroll_y = self.logica.cursor_y - lineas_visibles + 1

    def _ajustar_ancho(self, ancho_texto):
        if self.logica.cursor_x < self.scroll_x:
            self.scroll_x = self.logica.cursor_x
        elif self.logica.cursor_x >= self.scroll_x + ancho_texto:
            self.scroll_x = self.logica.cursor_x - ancho_texto + 1