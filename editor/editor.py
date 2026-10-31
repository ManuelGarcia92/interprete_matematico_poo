from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import Layout, Window
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.layout.controls import FormattedTextControl

from .interfaz import Interfaz
from .logica import Logica

class Editor:
    def __init__(self):
        self.logica = Logica()
        self.interfaz = Interfaz(self.logica)
        self.kb = KeyBindings()
        self.procesar = False
        self._configurar_teclas()

    def _configurar_teclas(self):
        kb = self.kb

        @kb.add('up')
        def _(event):
            self.logica.arriba()

        @kb.add('down')
        def _(event):
            self.logica.abajo()
        
        @kb.add('left')
        def _(event):
            self.logica.izquierda()

        @kb.add('right')
        def _(event):
            self.logica.derecha()

        @kb.add('home')
        def _(event):
            self.logica.principio_linea()

        @kb.add('end')
        def _(event):
            self.logica.fin_linea()

        @kb.add('pageup')
        def _(event):
            self.logica.primera_linea()

        @kb.add('pagedown')
        def _(event):
            self.logica.ultima_linea()

        @kb.add('enter')
        def _(event):
            self.logica.añadir_linea()

        @kb.add('backspace')
        def _(event):
            self.logica.eliminar_caracter()

        @kb.add('tab')
        def _(event):
            self.logica.tabulacion()

        @kb.add('s-tab')
        def _(event):
            self.logica.tabulacion_inversa()

        @kb.add('escape', eager=True)
        def _(event):
            self.procesar = False
            event.app.exit()

        @kb.add('c-r')
        def _(event):
            self.procesar = True
            event.app.exit()
        
        @kb.add(Keys.Any)
        def _(event):
            if event.data:
                self.logica.añadir_caracter(event.data)

    def salida(self,
                mensaje_superior="[Presione [Escape] para salir]\n[Presione [Control+R] para procesar]",
                mensaje_inferior=""):
        
        self.procesar = False

        control_superior = FormattedTextControl(text=lambda:self.interfaz.obtener_texto_superior(mensaje_superior))
        control_medio = FormattedTextControl(text=self.interfaz.obtener_texto_medio)
        control_inferior = FormattedTextControl(text=lambda:self.interfaz.obtener_texto_inferior(mensaje_inferior))

        root_container = HSplit([
            Window(content=control_superior, height=3, always_hide_cursor=True),
            Window(content=control_medio, always_hide_cursor=True),
            Window(content=control_inferior, height=2, always_hide_cursor=True),
        ])

        layout = Layout(root_container)

        app = Application(
            layout=layout,
            key_bindings=self.kb,
            full_screen=True,
            mouse_support=True,
            cursor=None
        )

        app.run()
        return self.logica.matriz
    
    @staticmethod
    def comprobar_matriz_vacia(matriz):
        if not matriz:
            return True
        return all(str(celda).strip() == "" for fila in matriz for celda in fila)

    def formatear_matriz(self, matriz):
        matriz_formateada = ""
        if self.comprobar_matriz_vacia(matriz):
            return matriz_formateada
        for linea in matriz:
            matriz_formateada += "".join(linea)
            matriz_formateada += "|"
        return matriz_formateada[:-1]
    

    
    



