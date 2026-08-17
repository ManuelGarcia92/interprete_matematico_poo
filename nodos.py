class NodoBinario:
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda
        self.derecha = derecha
    
class NodoSuma(NodoBinario):
    def evaluar(self):
        return self.izquierda.evaluar() + self.derecha.evaluar()

class NodoResta(NodoBinario):
    def evaluar(self):
        return self.izquierda.evaluar() - self.derecha.evaluar()
    
class NodoMulti(NodoBinario):
    def evaluar(self):
        return self.izquierda.evaluar() * self.derecha.evaluar()
    
class NodoDiv(NodoBinario):
    def evaluar(self):
        if self.derecha.evaluar() == 0:
            raise Exception("No se puede dividir por 0.")
        return self.izquierda.evaluar() / self.derecha.evaluar()
    
class NodoDivEntera(NodoBinario):
    def evaluar(self):
        if self.derecha.evaluar() == 0:
            raise Exception("No se puede dividir por 0.")
        return self.izquierda.evaluar() // self.derecha.evaluar()

class NodoPotencia(NodoBinario):
    def evaluar(self):
        return self.izquierda.evaluar() ** self.derecha.evaluar()
    
class NodoRaizEnesima(NodoBinario):
    def evaluar(self):
        if self.izquierda.evaluar() < 0 and self.derecha.evaluar() % 2 != 0:
            return -(-self.izquierda.evaluar()) ** (1 / self.derecha.evaluar())
        return self.izquierda.evaluar() ** (1 / self.derecha.evaluar())
    
class NodoNumero:
    def __init__(self, valor):
        self.valor = valor

    def evaluar(self):
        if "." in self.valor:
            return float(self.valor)
        return int(self.valor)

class NodoPositivo(NodoNumero):
    def evaluar(self):
        return self.valor.evaluar()
    
class NodoNegativo(NodoNumero):
    def evaluar(self):
        return -self.valor.evaluar()

