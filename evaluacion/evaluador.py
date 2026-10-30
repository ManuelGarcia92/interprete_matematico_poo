def evaluar_instrucciones(instrucciones : list, memoria) -> list:
    if instrucciones:
        for instruccion in instrucciones:
            if isinstance(instruccion, list):
                for sub_instruccion in instruccion:
                    sub_instruccion.evaluar(memoria)
            else:
                instruccion.evaluar(memoria)
    return memoria.cola_salida

def evaluar_cuerpo(instrucciones, memoria):
    resultado = None
    if instrucciones:
        for instruccion in instrucciones:
            if isinstance(instruccion, list):
                for sub_instruccion in instruccion:
                    resultado = sub_instruccion.evaluar(memoria)
            else:
                resultado = instruccion.evaluar(memoria)
    return resultado
       


