def evaluar_instrucciones(instrucciones : list, memoria) -> list | None:
    cola_salida = None
    if instrucciones:
        for instruccion in instrucciones:
            if isinstance(instruccion, list):
                for sub_instruccion in instruccion:
                    sub_instruccion.evaluar(memoria)
            else:
                instruccion.evaluar(memoria)
        cola_salida = memoria.cola_salida
    return cola_salida
       


