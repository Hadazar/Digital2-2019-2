
from tkinter import *
from math import *

ventana = Tk() #Crea la ventana

#Configuración de ventana -------------
ventana.title("Compilador MIPS")
ventana.geometry("800x600")
ventana.resizable(0,0) #Bloquear el tamaño de la ventana
ventana.configure(background="#B1C340") #Color de fondo

#Configuración de botones -------------
ColorBoton=("#3FC3D8")
AnchoBoton=11
AltoBoton=3

#Tablas de instrucciones y registros MIPS
Tabla = open("InstruccionesMIPS","r")#Instrucciones tipo I y J
SetInstrucciones = Tabla.read()
TablaR = open("InstruccionesTipoR","r")#Instrucciones tipo R
SetInstruccionesR = TablaR.read()
BancoRegistros = open("BancoDeRegistros","r")#Banco de registros
Registros = BancoRegistros.read()
BancoRegistros = Registros.split(" ")#Vector que contiene los registros

CodigoHexa = open("memfile.dat","w")#Archivo sobre el cual se exporta el hexadecimal
MatrizCodigo = []#Matriz que almacena el código escrito por el usuario
Labels = {} #Diccionario para almacenar los label y sus direcciones de memoria

DireccionBase = 0x00401000

#Convierte un string en una matriz
def convertirAmatriz(Texto):
    Lista = Texto.split("\n")#Convierte el texto en un vector, cada vector es una línea de código
    n = len(Lista)
    Matriz = [None] * (n-1)
    for i in range(0,n-1):
        Lista[i] = Lista[i].replace(",","")#Suprime las comas
        Lista[i] = Lista[i].replace("("," ")#Suprime los paréntesis
        Lista[i] = Lista[i].replace(")","")
        Matriz[i] = Lista[i].split(" ") #Convierte cada línea de código en un vector, cada string es una posición
    return Matriz

#Detecta los labels en el código, los almacena en un diccionario junto con sus respectivas posiciones de memoria, y los elimina de la matriz que contiene al código
def capturarLabels():
    global MatrizCodigo, Labels #Se especifican globales, porque se pretende editar
    n = len(MatrizCodigo) #Cantidad de líneas de código introducidas por el usuario
    i = 0
    while i<n:
        if MatrizCodigo[i][0][-1] == ":":
            label = MatrizCodigo[i][0].replace(":","")
            Labels[label] = DireccionBase+i*4
            print(hex(DireccionBase+i*4))
            MatrizCodigo.pop(i)
            n = n-1
        i = i+1


def exportar():
    global CodigoHexa
    CodigoHexa.write(MatrizHexa)
    CodigoHexa.close()
    
    
def capturarCodigo():
    global MatrizCodigo
    Codigo = CodigoMips.get(1.0,END)
    MatrizCodigo = convertirAmatriz(Codigo)
    print("Codigo: \n", Codigo)
    capturarLabels()
    imprimir(MatrizCodigo)
    print("\n\n")
    compilar()
    print(MatrizHexa)

def borrar():
    CodigoMips.delete(1.0,END)


def imprimir(Matriz):
    for i in Matriz:
        print(i)

def buscarRegistro(Registro):
    NumeroRegistro = None
    for i in range(len(BancoRegistros)):
        if Registro == BancoRegistros[i]:
            NumeroRegistro = i
            break
    return NumeroRegistro


def buscarInstruccion(Matriz, Instruccion):
    EstructuraInstruccion = None
    for i in range(len(Matriz)):
        if Instruccion == Matriz[i][0]:
            EstructuraInstruccion = Matriz[i]
    return EstructuraInstruccion

#Matrices
MatrizInstrucciones = convertirAmatriz(SetInstrucciones)
MatrizInstruccionesR = convertirAmatriz(SetInstruccionesR)
MatrizHexa = "" #Matriz que almacenará el código hexadecimal

#Botones -----------------------------
Iniciar = Boton0=Button(ventana,text="Iniciar",bg=ColorBoton,width=AnchoBoton,height=AltoBoton,command=lambda:capturarCodigo()).place(x=17,y=17)
Exportar = Boton0=Button(ventana,text="Exportar",bg=ColorBoton,width=AnchoBoton,height=AltoBoton,command=lambda:exportar()).place(x=17+115+17,y=17)
BorrarTodo = Boton0=Button(ventana,text="Borrar todo",bg=ColorBoton,width=AnchoBoton,height=AltoBoton,command=lambda : borrar()).place(x=17+115+17+115+17,y=17)

#Código MIPS ---------------------------
CodigoMipsEtiqueta = Message(ventana, text = "Escriba su código MIPS aquí:", width = 300, bg="#BEC7C9").place(x=17,y=100)
CodigoMips = Text(ventana,width=92,height=15, padx = 10, pady = 10)
CodigoMips.place(x=17,y=140)
#CodigoMips.insert(END,"Escriba aquí su código Mips...")

#Estado del programa --------------------
Estatus = 'Compilando...'
EstadoEtiqueta = Message(ventana, text = "Estado:", width = 115, bg="#BEC7C9").place(x=17,y=440)
Estado = Label(ventana, text = Estatus, width=95, height=5, bg = "black", fg = "white").place(x=17,y=490)

def compilar():

    global MatrizHexa
    n = len(MatrizCodigo)

    for i in range(len(MatrizCodigo)):

        Instruccion = MatrizCodigo[i]
        DireccionInstruccion = DireccionBase + i*4
        InstruccionHexa = compilarInstruccion(Instruccion,DireccionInstruccion)
        Cadena = str(hex(int(InstruccionHexa))).replace("0x","") #Lo transforma en string y le quita el "0x"
        Cadena = Cadena.zfill(8) #Le añade ceros a la izquierda y le coloca de nuevo el "0x"
        MatrizHexa = MatrizHexa + Cadena + "\n"


def compilarInstruccion(Instruccion,DireccionInstruccion):

    Opcode, rs, rt, rd, Shamt, Func, imm, addr = 0,0,0,0,0,0,0,0
    InstruccionHexa = None
    Estructura = buscarInstruccion(MatrizInstrucciones, Instruccion[0])#Busca en la lista tipo I y J
    TipoR = False

    #Si no las encuentra en la lista de tipo I y J entonces las busva en la lista tipoR
    if Estructura == None:
        print("buscando en R")
        Estructura = buscarInstruccion(MatrizInstruccionesR, Instruccion[0])
        TipoR = True

    Tipo = Estructura[2]
    print("Tipo: ", Tipo)
    
    #Instruccion tipo R
    if TipoR == True:

        Opcode = 0
        Func = int(Estructura[1])

        #Tipo R1
        if Tipo == "R1":
            rd = buscarRegistro(Instruccion[1]) 
            rs = buscarRegistro(Instruccion[2]) 
            rt = buscarRegistro(Instruccion[3])
            Shamt = 0

        #Tipo R2
        elif Tipo == "R2":
            rd = buscarRegistro(Instruccion[1]) 
            rt = buscarRegistro(Instruccion[2]) 
            rs = buscarRegistro(Instruccion[3])
            Shamt = 0

        #Tipo R3
        elif Tipo == "R3":
            rd = buscarRegistro(Instruccion[1]) 
            rt = buscarRegistro(Instruccion[2]) 
            Shamt = buscarRegistro(Instruccion[3])
            rs = 0

        #Tipo R4
        elif Tipo == "R4":
            rs = buscarRegistro(Instruccion[1])
            rt = 0
            rd = 0
            shamt = 0

        #Tipo R5
        elif Tipo == "R5":
            rd = buscarRegistro(Instruccion[1])
            rt = 0
            rs = 0
            shamt = 0

        #Tipo R6
        elif Tipo == "R6":
            rs = buscarRegistro(Instruccion[1])
            rt = buscarRegistro(Instruccion[2])
            rd = 0
            shamt = 0

        print("op: ",Opcode,", rs: ",rs,", rt: ",rt,", rd: ",rd,", shamt: ",Shamt,"\n")
        InstruccionHexa= Func + Shamt*pow(2,6) + rd*pow(2,11) + rt*pow(2,16) + rs*pow(2,21) + Opcode*pow(2,26)
        print("Hexa: ",hex(int(InstruccionHexa)),"\n")

    #Instruccion tipo I o J
    elif TipoR == False:

        Opcode = int(Estructura[1])
        TipoJ = False
        #Tipo J
        if Tipo == "J":
            addr = Labels[Instruccion[1]]/4
            print(addr)
            TipoJ = True

        #Tipo I1
        elif Tipo == "I1":
            rt = buscarRegistro(Instruccion[1])
            rs = buscarRegistro(Instruccion[2])
            imm = int(Instruccion[3])

        #Tipo I2
        elif Tipo == "I2":
            rt = buscarRegistro(Instruccion[1])
            imm = int(Instruccion[2])
            rs = buscarRegistro(Instruccion[3])

        #Tipo I3
        elif Tipo == "I3":
            rs = buscarRegistro(Instruccion[1])
            imm = Labels[Instruccion[2]] - (DireccionInstruccion-17) #Dirección de la etiqueta menos el PC (dirección de instrucción siguiente)
            rt = int(Estructura[3])

        #Tipo I4
        elif Tipo == "I4":
            rs = buscarRegistro(Instruccion[1])
            rt = buscarRegistro(Instruccion[2])
            imm = (Labels[Instruccion[3]] - (DireccionInstruccion+4))/4 #Dirección de la etiqueta menos el PC (dirección de instrucción siguiente)

        #Tipo I5
        elif Tipo == "I5":
            rt = buscarRegistro(Instruccion[1])
            imm = int(Instruccion[2])
            rs = 0

        #Tipo I6
        elif Tipo == "I6":
            rt = buscarRegistro(Instruccion[1])
            rd = buscarRegistro(Instruccion[2])
            rs = int(Estructura[3])

        #Tipo I7
        elif Tipo == "I7":
            imm = Labels[Instruccion[1]] - (DireccionInstruccion - 17) #Dirección de la etiqueta menos el PC (dirección de instrucción siguiente)
            rt = int(Estructura[3])
            rs = 0

        #Completo a 2 para números negativos
        if imm < 0:
            imm = 65536 + imm #65536dec=10000hex=FFFF+1hex

        if TipoJ == False:
            print("op: ",Opcode,", rs: ",rs,", rt: ",rt,", imm: ",imm,"\n")
            InstruccionHexa= imm + rt*pow(2,16) + rs*pow(2,21) + Opcode*pow(2,26)
            print("Hexa: ",hex(int(InstruccionHexa)),"\n")
        else:
            print("op: ",Opcode,", addr: ",addr,"\n")
            InstruccionHexa= addr + Opcode*pow(2,26)
            print("Hexa: ",hex(int(InstruccionHexa)),"\n")

    return InstruccionHexa


#print(buscarRegistro("$ra"))

#imprimir(MatrizInstrucciones)



ventana.mainloop() #Corre la ventana
