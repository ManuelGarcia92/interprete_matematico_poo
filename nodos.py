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
            raise Exception("ERROR: No se puede dividir por 0")
        return self.izquierda.evaluar(memoria) / self.derecha.evaluar(memoria)
    
class NodoDivEntera(NodoBinario):
    def evaluar(self, memoria):
        if self.derecha.evaluar(memoria) == 0:
            raise Exception("ERROR: No se puede dividir por 0")
        return self.izquierda.evaluar(memoria) // self.derecha.evaluar(memoria)

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

class NodoAsignacion:
    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor

    def evaluar(self, memoria):
        valor_evaluado = self.valor.evaluar(memoria)
        return memoria.declarar(self.nombre, valor_evaluado)
    
class NodoIdentificador:
    def __init__(self, nombre):
        self.nombre = nombre

    def evaluar(self, memoria):
        return memoria.obtener(self.nombre)