from .despacho import OPERACIONES
from evaluacion import evaluar_instrucciones

class NodoNumero:
    def __init__(self, valor):
        self.valor = valor

    def evaluar(self, memoria):
        if "." in self.valor:
            valor = float(self.valor)
        else:
            valor = int(self.valor)
        return valor

class NodoUnario:
    def __init__(self, signo : str, valor):
        self.signo = signo
        self.valor = valor

    def evaluar(self, memoria):
        resultado = self.valor.evaluar(memoria)
        if self.signo == "-":
            return -resultado
        else:
            return resultado
        
class NodoBinario:
    def __init__(self, operador : str, nodo_izquierdo, nodo_derecho):
        self.operador = operador
        self.nodo_izquierdo = nodo_izquierdo
        self.nodo_derecho = nodo_derecho
    
    def evaluar(self, memoria):
        valor_izquierda = self.nodo_izquierdo.evaluar(memoria)
        valor_derecha = self.nodo_derecho.evaluar(memoria)
        return OPERACIONES[self.operador](valor_izquierda, valor_derecha)

class NodoDeclaracionVariable:
    def __init__(self, nombre : str, valor):
        self.nombre = nombre
        self.valor = valor

    def evaluar(self, memoria):
        return memoria.declarar_variable(self.nombre, self.valor.evaluar(memoria))

class NodoDeclaracionFuncion:
    def __init__(self, nombre : str, argumentos : list, cuerpo : list):
        self.nombre = nombre
        self.argumentos = argumentos
        self.cuerpo = cuerpo

    def evaluar(self, memoria):
        memoria.declarar_funcion(self.nombre, self.argumentos, self.cuerpo, entorno=memoria)

class NodoLlamadaVariable:
    def __init__(self, nombre : str):
        self.nombre = nombre

    def evaluar(self, memoria):
        return memoria.obtener_simbolo(self.nombre)
    
class NodoLlamadaFuncion:
    def __init__(self, nombre : str, argumentos_llamada : list):
        self.nombre = nombre
        self.argumentos_llamada = argumentos_llamada

    def evaluar(self, memoria):
        funcion = memoria.obtener_simbolo(self.nombre)
        argumentos_funcion = funcion["argumentos"]
        cuerpo_codigo = funcion["cuerpo"]
        entorno_definicion = funcion["entorno"]

        if len(argumentos_funcion) != len(self.argumentos_llamada):  
            raise Exception(f"La función {self.nombre} espera {len(argumentos_funcion)} argumentos y recibio {len(self.argumentos_llamada)}")
        
        valores = [argumento.evaluar(memoria) for argumento in self.argumentos_llamada]
        entorno_local = entorno_definicion.crear_entorno_local()

        for parametro, valor in zip(argumentos_funcion, valores):
            entorno_local.declarar_variable(parametro.nombre, valor)

        resultado = evaluar_instrucciones(cuerpo_codigo, entorno_local)
        return resultado           