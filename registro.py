#Modulo del registro


class Compra():
    def __init__(self,codigo,precio,total,tipo_envio,cantidad_d,fecha):
        self.codigo = codigo
        self.precio = precio
        self.total = total
        self.tipo_envio = tipo_envio
        self.cantidad_d = cantidad_d
        self.fecha = fecha



class Objeto():
    def __init__(self,codigo,precio,ubicacion_g,estado,cantidad_d,puntuacion,nombre):
        self.nombre = nombre
        self.codigo = codigo
        self.precio = precio
        self.ubicacion_g = ubicacion_g
        self.estado = estado
        self.cantidad_d = cantidad_d
        self.puntuacion = puntuacion



def to_string(objeto):
    res = ""
    res += "{:<25}".format("Nombre: " + str(objeto.nombre))
    res += "{:<20}".format("Codigo: " + str(objeto.codigo))
    res += "{:<20}".format("Precio: $" + str(objeto.precio))
    res += "{:<34}".format("Ubicacion : " + str(objeto.ubicacion_g))
    res += "{:<20}".format("Estado: " + str(objeto.estado))
    res += "{:<20}".format("Cantidad: " + str(objeto.cantidad_d))
    res += "{:<15}".format("Puntuacion: " + str(objeto.puntuacion))
    res += "\n"

    return res


def to_string2(compra):
    res = ""
    res += "{:<20}".format("Codigo: " + str(compra.codigo))
    res += "{:<20}".format("Precio: $" + str(compra.precio))
    res += "{:<20}".format("Total: " + str(compra.total))
    res += "{:<20}".format("Tipo de envio: " + str(compra.tipo_envio))
    res += "{:<20}".format("Cantidad: " + str(compra.cantidad_d))
    res += "{:<15}".format("Fecha: " + str(compra.fecha))
    res += "\n"

    return res
