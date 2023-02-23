import random
import os.path
import pickle
from Tp4.registro import *
import time

#Crea el vector y lo carga
def crear_arreglo():
    n = int(input("Ingrese la cantidad de arreglos: "))
    v = []
    for i in range(n):
        nombre = random.choice(["Placa Grafica","Perfumes","Mouse","Teclado","Auriculares","Pantalla","Parlantes"])
        codigo = random.randint(1,9999)
        precio = random.randint(1000,40000)
        ubicacion_g = random.choice(["Buenos Aires", "Cordoba", "Tucuman", "Salta", "La Rioja", "San Juan", "Santiago del Estero",
                  "Santa Fe", "Entre Rios", "Misiones", "Formosa", "Corrientes", "San Luis", "Mendoza",
                  "Neuquen", "Chubut", "Santa Cruz", "Rio Negro", "Tierra del Fuego", "Catamarca", "Jujuy",
                  "Chaco", "La Pampa"])
        estado = random.choice(["nuevo","usado"])
        cantidad_d = random.randint(1,10000)
        puntuacion = random.randint(1,5)
        m = Objeto(codigo,precio,ubicacion_g,estado,cantidad_d,puntuacion,nombre)
        add_in_order(v,m)

    return v


#Muestra los datos del vector
def mostrar_articulos(v):
    for i in v:
        print(to_string(i))

#CREACION DE ARCHIVOS---------------------------------------------------------------------------------------------------
#Crea el archivo binario con datos de la compra
def crear_archivo(nombre,compra):
    print("Se ah creando el archivo: ",nombre)
    m = open(nombre,"ab")
    pickle.dump(compra,m)
    m.close()


#Crea el archivo de texto con los datos del ticket
def crear_archivo_texto(nombre,ticket):
    print("Se ah creando el archivo: ",nombre,"\n")
    m = open(nombre,"wt")
    m.write(ticket)
    m.close()
#FIN DE SECCION DE ARCHIVOS---------------------------------------------------------------------------------------------


#Punto 3----------------------------------------------------------------------------------------------------------------
#Muestra los datos dentro del archivo que se abre en el punto 2
def mostar_datos_archivo(nombre):
    f = []
    if not os.path.exists(nombre):
        print("El archivo no existe. Debe realizar una compra.")
    else:
        m = open("miscompras.dat", "rb")
        t = os.path.getsize("miscompras.dat")
        while m.tell() < t:
            art = pickle.load(m)
            f.append(art)
        m.close()
        return f

def asignar_fechas(desde,hasta,f):
    for i in f:
        if i is not None:
            if desde < int(i.fecha) < hasta:
                print(to_string2(i))

#Fin del punto 3--------------------------------------------------------------------------------------------------------

#Ordena el vector por codigo
def add_in_order(v, articulo):
    n = len(v)
    pos = n

    for i in range(n):
        if articulo.codigo < v[i].codigo:
            pos = i
            break

    v[pos:pos] = [articulo]


#Punto 2 ---------------------------------------------------------------------------------------------------------------
#Funcion convertidor de fechas
def convertir_fecha(fecha):
    anio = fecha[:4]
    mes = fecha[4:6]
    dia = fecha[6:]
    return dia+"/"+mes+"/"+anio

#Funcion que crea el ticket
def ticket(compra, objeto):
    compra_n = compra.codigo
    total = compra.precio * compra.cantidad_d
    cargo = ((compra.tipo_envio-1)*0.10) * total
    s = "-"*100
    s += "{:<10}{:>20}".format('\nCompra #' + str(compra_n), convertir_fecha(compra.fecha))
    s += "\nResumen de compra"
    s += "\n{:<10}{:^10}{:>10}".format(objeto.nombre + "\t"*3 ,"$" + str(round(total, 2)),
                                       "("+str(compra.cantidad_d) + "x" + "$" + str(compra.precio) + ")")
    s += "\n{:<20}{:>10}".format('Cargo de Envio:', round(cargo, 2))
    s += "\n{:<20}{:>10}\n".format("Tu Pago:", total+cargo)
    s += "-"*100

    fd = "Ticket" + str(compra_n) + ".txt"
    m = open(fd, 'wt')
    m.write(s)
    m.close()
    return s


def comprar(v):
    x = int(input("Ingrese el codigo del articulo a buscar: "))
    c = buscar(v,x)
    if c is not None:
        com = validar(0,3,"Desea realizar una compra [1-Si o 2-No]: ")
        if com == 1:
            print("\n","\t"*5,"La cantidad de articulos disponibles es: ",v[c].cantidad_d,"\n")
            cant = int(input("Ingrese la cantidad de articulos a comprar: "))
            if cant <= v[c].cantidad_d:
                print("\n","\t"*5,"La cantidad que desea comprar es valida""\n","\n""Desea confirmar la compra?[1-Si o 2-No] : ","\n")
                confirmar = validar(0,3,"Confirmar: ")
                if confirmar == 1:
                    print("\n","\t"*5,"Metodo de envio: [1-Sucursal o 2-Domicilio]","\n")
                    envio = validar(0,3,"Confirmar metodo de envio: ")
                    interes = (v[c].precio * 0.10 )* (envio - 1)
                    total = v[c].precio * cant + interes
                    v[c].cantidad_d -= cant
                    compra = Compra(v[c].codigo,v[c].precio,total,envio,cant,time.strftime("%Y%m%d"))
                    t = ticket(compra,v[c])
                    print("\n"+"\t"*5+"Ticket")
                    print(t+"\n")
                    return t,compra

                else:
                    print("Compra cancelada")
            else:
                print("Cantidad en Stock insuficiente")

        else:
            print("Compra cancelada")

    else:
        print("\n"+"\t"*5,"El articulo no existe","\n")


#Busca publicacion ingresada por teclado
def buscar(vector, t):
    izq = 0
    der = len(vector) - 1

    while izq <= der:
        c = (izq + der) // 2
        if t == vector[c].codigo:
            return c
        elif t < vector[c].codigo:
            der = c - 1
        else:
            izq = c + 1
    return None


#Fin punto 2 -----------------------------------------------------------------------------------------------------------

#Inicio Punto 4---------------------------------------------------------------------------------------------------------

def mayor(vec):
    may = 0
    for i in range(len(vec)):
        if may == 0:
            may = vec[i].precio

        if may < vec[i].precio:
            may = vec[i].precio
    return may


def menor(vec):
    men = 0
    for i in range(len(vec)):
        if men == 0:
            men = vec[i].precio

        if men > vec[i].precio:
            men = vec[i].precio
    return men


def validar_r(men,may,mensaje):
    n = int(input(mensaje))
    while n < men or n > may:
        print("Error")
        n = int(input(mensaje))
    return n


def entre_precios(men,may,vec):
    n = validar_r(men,may,"Ingrese el precio minimo dispuesto a pagar superior o igual a [" +str(men)+"]: ")
    m = validar_r(n,may,"Ingrese un precio maximo dispuesto a pagar menor o igual a ["+ str(may) +"]: ")
    print("\n","\t"*5,"Los articulos entre rangos de precios ingresados son: ","\n")
    for i in range(len(vec)):
        if n <= vec[i].precio <= m  :
            print(to_string(vec[i]))
#Final Punto 4----------------------------------------------------------------------------------------------------------

#Inicio Punto 5---------------------------------------------------------------------------------------------------------
def favoritos(vec,fav):
    x = int(input("Ingrese el codigo del articulo que quiere agregar a favoritos para terminar ingrese 0(cero): "))
    while x != 0:
        c = buscar(vec,x)
        if c is not None:
            rep = buscar(fav,x)
            if rep is not None:
                print("\n","\t"*5,"El articulo esta repetido","\n")
            else:
                add_in_order(fav,vec[c])
        else:
            print("\n"+"\t"*5,"EL codigo ingresado no es valido","\n")
        x = int(input("Ingrese el codigo del articulo que quiere agregar a favoritos para terminar ingrese 0(cero): "))
    if len(fav) == 0:
        print("\n"+"\t"*5,"No se agregaron articulos al vector favoritos.","\n")
    else:
        print("\n"+"\t"*5,"A finalizado la carga a Favoritos.","\n")
#Final Punto 5----------------------------------------------------------------------------------------------------------


#Inicio Punto 6---------------------------------------------------------------------------------------------------------


def crear_archivo_favorito(nombre,fav):
    print("\n"+"\t"*5,"Se ha creado el archivo: ",nombre,"\n")
    m = open(nombre,"ab")
    for a in fav:
        pickle.dump(a,m)
    m.close()


def comparar_repetido(fav,nombre):
    v = []
    if os.path.exists(nombre):
        m = open(nombre, "rb")
        t = os.path.getsize(nombre)

        while m.tell() < t:
            v.append(pickle.load(m))
        m.close()
    m = open(nombre, 'ab')
    for i in fav:
        rep = False
        for j in v:
            if i.codigo == j.codigo:
                rep = True
                break
        if not rep:
            pickle.dump(i, m)
    m.close()


def mostar_archivo_fav(nombre):
    if not os.path.exists(nombre):
        print("El archivo no existe. Debe agregar a favoritos.")
    else:
        m = open(nombre, "rb")
        t = os.path.getsize(nombre)
        if t == 0:
            print("\n"+"\t"*5,"No hay datos cargados en el archivo",nombre,"cargue los datos con el punto 5","\n")
        else:
            print("\n"+"\t"*10,"Archivo actualizado con articulos favoritos","\n")
            while m.tell() < t:
                art = pickle.load(m)
                print(to_string(art))
        m.close()


#Fin punto 6------------------------------------------------------------------------------------------------------------


#Codigo de validacion
def validar(min,may,mensaje):
    n = int(input(mensaje))
    while n <= min or n >= may:
        print("Error")
        n = int(input(mensaje))
    return n


#Funcion que crea un menu y esta validado para que no se salga de sus parametros
def menu():
    print("*"*160)
    print("-"*20,"Bienvenido al menu de MERCADO LIBRE.","-"*20)
    print("\n")
    print("1- Ver datos de aritulos.")
    print("2- Comprar.")
    print("3- Mis compras.")
    print("4- Rango de precios.")
    print("5- Agregar a favoritos.")
    print("6- Actualizar favoritos.")
    print("7- Salir.")
    print("\n")
    print("*"*160)
    return validar(0,8,"Ingrese una opcion: ")


def principal():
    op = -1
    #Archivos
    fd = "miscompras.dat"
    tex = "datos.txt"
    fav = "favoritos.dat"

    #Vector con datos
    art = crear_arreglo()
    favo = []

    while op != 8:
        op = menu()

        if op == 1:
            print("\n","\t"*10,"Ariculos disponibles","\n")
            mostrar_articulos(art)


        elif op == 2:
            bus = comprar(art)
            if bus is not None:
                crear_archivo(fd,bus[1])
                crear_archivo_texto(tex,bus[0])


        elif op == 3:
            if not os.path.exists(fd):
                print("El archivo no existe. Debe realizar una compra.")
            else:
                des = int(input("Ingrese la feccha de inicio para buscar en formato aaaammdd: "))
                has = int(input("ingrese la fecha del final para buscar en formato aaaammdd: "))
                print("\n"+"\t"*5,"Articulos comprendidos entre las fechas ingresadas."+"\n")
                asignar_fechas(des,has,mostar_datos_archivo(fd))


        elif op == 4:
            m = mayor(art)
            n = menor(art)
            entre_precios(n,m,art)

        elif op == 5:
            favoritos(art,favo)
            mostrar_articulos(favo)


        elif op == 6:
            if not os.path.exists(fav):
                print("\n"+"\t"*5,"El archivo no existia y ha sido creado.","\n")
                crear_archivo_favorito(fav,favo)
            else:
                comparar_repetido(favo,fav)
            mostar_archivo_fav(fav)


        elif op == 7:
            print("\n","\t"*5,"Gracias por usar la plataforma de MERCADO LIBRE, hasta luego.""\n")
            print("\t"*10,"Fin Del Programa.","\n")
            break


if __name__ == '__main__':
    principal()


