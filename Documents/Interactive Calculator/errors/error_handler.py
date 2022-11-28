class InvalidCharacterWrittenError(Exception):
    """
    Excepción que se invoca cuando un carácter no admitido se escribe en la operación.

    ----------------------------
    Atributos:
    ----------------------------

        operacion -- La operación ejecutada
        mensaje -- Explicación del error
    """

    def __init__(self, operacion, mensaje="Un carácter no admitido se ha introducido en la operación"):
        self.operacion = operacion
        self.mensaje = mensaje
        super().__init__(self.mensaje)

    def __str__(self):
        return "{} -> {}".format(self.operacion, self.mensaje)


class CouldNotResolveError(Exception):
    """
    Excepción que se invoca cuando la operación indicada no se ha podido realizar

    ----------------------------
    Atributos:
    ----------------------------

        operacion -- La operación ejecutada
        mensaje -- Explicación del error
    """

    def __init__(self, operacion, mensaje="La operación no se ha podido resolver"):
        self.operacion = operacion
        self.mensaje = mensaje

        super().__init__(self.mensaje)

    def __str__(self):
        return "{} -> {}".format(self.operacion, self.mensaje)


class InvalidOptionGiven(Exception):
    def __init__(self, respuesta, mensaje="Esa opción no es una admitida por el código"):
        self.respuesta = respuesta

        self.mensaje = mensaje

        super().__init__(self.mensaje)

    def __str__(self):
        return "{} -> {}".format(self.respuesta, self.mensaje)