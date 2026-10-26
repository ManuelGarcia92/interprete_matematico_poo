from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app
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
            self.logica.primera_linea()

        @kb.add('end')
        def _(event):
            self.logica.fin_linea()

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

        @kb.add('escape')
        def _(event):
            event.app.exit()

        @kb.add(Keys.Any)
        def _(event):
            if event.data:
                self.logica.añadir_caracter(event.data)

    def salida(self, mensaje_superior, mensaje_inferior):
        def obtener_texto_sup():
            app_actual = get_app()
            _, ancho_term = app_actual.output.get_size()
            return f"{mensaje_superior}\n{"_" * ancho_term}"

        def obtner_texto_inf():
            app_actual = get_app()
            _, ancho_term = app_actual.output.get_size()
            return f"{"_" * ancho_term}\n {mensaje_inferior}"

        control_superior = FormattedTextControl(text=obtener_texto_sup)
        control_editor = FormattedTextControl(text=self.interfaz.interfaz_editor)
        control_inferior = FormattedTextControl(text=obtner_texto_inf)

        root_container = HSplit([
            Window(content=control_superior, height=2, always_hide_cursor=True),
            Window(content=control_editor, always_hide_cursor=True),
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
    def formatear_matriz(matriz):
        matriz_formateada = ""
        for linea in matriz:
            matriz_formateada += "".join(linea)
            matriz_formateada += "|"
        return matriz_formateada[:-1]


