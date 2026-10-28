def evaluar_instrucciones(instrucciones : list, memoria) -> int | float | None:
    resultado = None
    if instrucciones:
        for instruccion in instrucciones:
            if isinstance(instruccion, list):
                for sub_instruccion in instruccion:
                    resultado = sub_instruccion.evaluar(memoria)
            else:
                resultado = instruccion.evaluar(memoria)
    return resultado
       


