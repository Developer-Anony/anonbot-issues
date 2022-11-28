from errors.error_handler import *

def calc(oper:str):

    if 'x' in oper or '/' in oper or '÷' in oper or '×' in oper or '+' in oper or '-' in oper:
        o = oper.replace("x" or "×", "*")
        p = o.replace("÷" or "/", "/")
        pass

    else:
        raise InvalidCharacterWrittenError(oper)


    


    try:
        res = str(eval(p))

    except:
        raise CouldNotResolveError(oper)

    print("""Operación:
    {}
    
Resultado:
    {}""".format(oper, res))