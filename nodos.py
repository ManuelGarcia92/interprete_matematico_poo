import math

class NodoBinario:
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha
    
class NodoSuma(NodoBinario):
    def evaluar(self, memoria):
        return self.izquierda.evaluar(memoria) + self.derecha.evaluar(memoria)

class NodoResta(NodoBinario):
    def evaluar(self, memoria):
        return self.izquierda.evaluar(memoria) - self.derecha.evaluar(memoria)
    
class NodoMulti(NodoBinario):
    def evaluar(self, memoria):
        return self.izquierda.evaluar(memoria) * self.derecha.evaluar(memoria)
    
class NodoDiv(NodoBinario):
    def evaluar(self, memoria):
        if self.derecha.evaluar(memoria) == 0:
            raise Exception("Error matemático: No se puede dividir por 0")
        return self.izquierda.evaluar(memoria) / self.derecha.evaluar(memoria)
    
class NodoDivEntera(NodoBinario):
    def evaluar(self, memoria):
        if self.derecha.evaluar(memoria) == 0:
            raise Exception("Error matemático: No se puede dividir por 0")
        return self.izquierda.evaluar(memoria) // self.derecha.evaluar(memoria)
    
class NodoModulo(NodoBinario):
    def evaluar(self, memoria):
        if self.derecha.evaluar(memoria) == 0:
            raise Exception("Error matemático: Módulo no se puede dividir por 0")
        return self.izquierda.evaluar(memoria) % self.derecha.evaluar(memoria)
    
class NodoPotencia(NodoBinario):
    def evaluar(self, memoria):
        return self.izquierda.evaluar(memoria) ** self.derecha.evaluar(memoria)
    
class NodoRaizEnesima(NodoBinario):
    def evaluar(self, memoria):
        if self.izquierda.evaluar(memoria) < 0 and self.derecha.evaluar(memoria) % 2 != 0:
            return -(-self.izquierda.evaluar(memoria)) ** (1 / self.derecha.evaluar(memoria))
        return self.izquierda.evaluar(memoria) ** (1 / self.derecha.evaluar(memoria))
    
class NodoNumero:
    def __init__(self, valor):
        self.valor = valor

    def evaluar(self, memoria):
        return self.valor

class NodoPositivo(NodoNumero):
    def evaluar(self, memoria):
        return self.valor.evaluar(memoria)
    
class NodoNegativo(NodoNumero):
    def evaluar(self, memoria):
        return -self.valor.evaluar(memoria)
    
class NodoAbs(NodoNumero):
    def evaluar(self, memoria):
        valor = self.valor.evaluar(memoria)
        return valor if valor >= 0 else -valor    
       
class NodoSin(NodoNumero):
    def evaluar(self, memoria):
        return math.sin(self.valor.evaluar(memoria))

class NodoAsin(NodoNumero):
    def evaluar(self, memoria):
        valor = self.valor.evaluar(memoria)
        if not(-1 <= valor <= 1):
            raise Exception("Error matemático: el argumento de asin debe estar entre -1 y 1")
        return math.asin(valor)
    
class NodoCos(NodoNumero):
    def evaluar(self, memoria):
        return math.cos(self.valor.evaluar(memoria))

class NodoAcos(NodoNumero):
    def evaluar(self, memoria):
        valor = self.valor.evaluar(memoria)
        if not(-1 <= valor <= 1):
            raise Exception("Error matemático: el argumento de acos debe estar entre -1 y 1")
        return math.acos(valor)
    
class NodoTan(NodoNumero):
    def evaluar(self, memoria):
        return math.tan(self.valor.evaluar(memoria))
    
class NodoAtan(NodoNumero):
    def evaluar(self, memoria):
        return math.atan(self.valor.evaluar(memoria))

class NodoLog(NodoNumero):
    def evaluar(self, memoria):
        valor = self.valor.evaluar(memoria)
        if valor <= 0:
            raise Exception("Error matemático: el argumento de log debe ser mayor a 0")
        return math.log(valor)
    
class NodoAsignacion:
    def __init__(self, var_nombre, var_valor):
        self.var_nombre = var_nombre
        self.var_valor = var_valor

    def evaluar(self, memoria):
        return memoria.declarar(self.var_nombre, self.var_valor.evaluar(memoria))
    
class NodoIdentificador:
    def __init__(self, var_nombre):
        self.var_nombre = var_nombre

    def evaluar(self, memoria):
        return memoria.obtener(self.var_nombre)

class NodoFuncion:
    def __init__(self, nombre, argumentos, cuerpo):
        self.nombre = nombre
        self.argumentos = argumentos
        self.cuerpo = cuerpo

    def evaluar(self, memoria):
        memoria.declarar_funcion(self.nombre, self.argumentos, self.cuerpo)

class NodoLlamada:
    def __init__(self, nombre, argumentos):
        self.nombre = nombre
        self.argumentos = argumentos

    def evaluar(self, memoria):
        func = memoria.llamar_funcion(self.nombre)
        param_nombres = func["argumentos"]
        cuerpo_codigo = func["cuerpo"]

        valores = [arg.evaluar(memoria) for arg in self.argumentos]

        entorno_local = memoria.crear_entorno_local()
        
        for param, valor in zip(param_nombres, valores):
            entorno_local.declarar(param.var_nombre, valor)

        resultado = None
        
        try:
            for instruccion in cuerpo_codigo:
                resultado = instruccion.evaluar(entorno_local)
        except ExepcionReturn as ret:
            return ret
        
        return resultado
    
class ExepcionReturn(Exception):
    def __init__(self, expresion):
        self.expresion = expresion

class NodoReturn:
    def __init__(self, expresion):
        self.expresion = expresion

    def evaluar(self, memoria):
        valor = self.expresion.evaluar(memoria) if self.expresion else None
        raise ExepcionReturn(valor)
    
            