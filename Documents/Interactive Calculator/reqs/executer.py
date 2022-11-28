from reqs.operations_solver import calc

operacion = str(input("""¿Qué operación he de ejecutar?
(Puede utilizar 'x' para multiplicación y '/' para división):
"""))

def ejecutar():
    try:
        calc(oper=operacion)
    except Exception as e:
        print(e)