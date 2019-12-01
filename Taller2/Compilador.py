
from tkinter import *
from math import *

ventana = Tk() #Crea la ventana

#Configuración de ventana -------------
ventana.title("Compilador MIPS")
ventana.geometry("800x600")
ventana.resizable(0,0) #Bloquear el tamaño de la ventana
ventana.configure(background="#B1C340")

#Configuración de botones -------------
ColorBoton=("#3FC3D8")
AnchoBoton=11
AltoBoton=3

#Tablas de instrucciones y registros MIPS
Tabla = open("InstruccionesMIPS","r")
SetInstrucciones = Tabla.read()
TablaR = open("InstruccionesTipoR","r")
SetInstruccionesR = TablaR.read()
BancoRegistros = open("BancoDeRegistros","r")
Registros = BancoRegistros.read()
CodigoEjemplo = open("Ejemplo","r")
Ejemplo = CodigoEjemplo.read()

def convertirAmatriz(Texto):
    Lista = Texto.split("\n")
    n = len(Lista)
    Matriz = [None] * (n-1)
    for i in range(0,n-1):
        Lista[i] = Lista[i].replace(",","")
        Lista[i] = Lista[i].replace("("," ")
        Lista[i] = Lista[i].replace(")","")
        Matriz[i] = Lista[i].split(" ")
    return Matriz

#MatrizCodigo = ""
MatrizCodigo = convertirAmatriz(Ejemplo)
Labels = {}
BancoRegistros = Registros.split(" ")
DireccionBase = 0x00400000

def capturarLabels():
    global MatrizCodigo, Labels
    n = len(MatrizCodigo)
    for i in range(0,n-1):
        if MatrizCodigo[i][0][-1] == ":":
            Labels[MatrizCodigo[i][0]] = DireccionBase+i*4
            """
            label = []
            label.append(MatrizCodigo[i][0])
            label.append(hex(DireccionBase+i*4))
            Labels.append(label)
            """
            MatrizCodigo.pop(i)

def buscarLabel(label):
    Direccion = None
    for i in range(len(Labels)):
        if Labels[i][0] == label:
            Direccion = Labels[i][1]
    return Direccion

def getOpcode():
    #print("Opcode: \n")
    #print(SetInstrucciones)
    print(MatrizCodigo)
    print("\n\n")
    capturarLabels()
    print(MatrizCodigo)
    print("\n\n")
    print(Labels)
    print("\n\n")
    print(Labels["L1:"])

def capturarCodigo():
    global MatrizCodigo
    Codigo = CodigoMips.get(1.0,END)
    MatrizCodigo = convertirAmatriz(Codigo)
    print("Codigo: \n", Codigo)

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
    EstructuraInstruccion = ""
    for i in range(len(Matriz)):
        if Instruccion == Matriz[i][0]:
            EstructuraInstruccion = Matriz[i]
    return EstructuraInstruccion

#Matrices
MatrizInstrucciones = convertirAmatriz(SetInstrucciones)
MatrizInstruccionesR = convertirAmatriz(SetInstruccionesR)

#Botones -----------------------------
Iniciar = Boton0=Button(ventana,text="Iniciar",bg=ColorBoton,width=AnchoBoton,height=AltoBoton,command=lambda:capturarCodigo()).place(x=17,y=17)
Exportar = Boton0=Button(ventana,text="Exportar",bg=ColorBoton,width=AnchoBoton,height=AltoBoton,command=lambda:getOpcode()).place(x=17+115+17,y=17)
BorrarTodo = Boton0=Button(ventana,text="Borrar todo",bg=ColorBoton,width=AnchoBoton,height=AltoBoton,command=lambda : borrar()).place(x=17+115+17+115+17,y=17)

#Código MIPS ---------------------------
CodigoMips = Text(ventana,width=92,height=15, padx = 10, pady = 10)
CodigoMips.place(x=17,y=100)
CodigoMips.insert(END,"Escriba aquí su código Mips...")

#Estado del programa --------------------
Estatus = 'Compilando...'
EstadoEtiqueta = Message(ventana, text = "Estado:", width = 115, bg="#BEC7C9").place(x=17,y=400)
Estado = Label(ventana, text = Estatus, width=95, height=5, bg = "black", fg = "white").place(x=17,y=450)

"""
opcode
rs
rt
rd
shamt
func
imm
addr
tipo
"""
"""

for i in range(len(MatrizCodigo)):
    Instruccion = MatrizCodigo[i][0]
    Estructura = buscarInstruccion(MatrizInstrucciones, Instruccion)
    TipoR = False
    Tipo = Estructura[2]
    if Estructura == "":
        Estructura = buscarInstruccion(MatrizInstruccionesR, Instruccion)
        TipoR = True
    
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

    #Instruccion tipo I o J
    elif TipoR == False:

        Opcode = int(Estructura[1])

        #Tipo J
        if Tipo == "J":
            addr = Instruccion[1]

        #Tipo I1
        elif Tipo == "I1":
            rt = buscarRegistro(Instruccion[1])
            rs = buscarRegistro(Instruccion[2])
            imm = Instruccion[3]

        #Tipo I2
        elif Tipo == "I2":
            rt = buscarRegistro(Instruccion[1])
            imm = Instruccion[2]
            rs = buscarRegistro(Instruccion[3])

        #Tipo I3
        elif Tipo == "I3":
            rs = buscarRegistro(Instruccion[1])
            #label
            rt = Estructura[3]

        #Tipo I4
        elif Tipo == "I4":
            rs = buscarRegistro(Instruccion[1])
            rt = buscarRegistro(Instruccion[2])
            #label

        #Tipo I5
        elif Tipo == "I5":
            rt = buscarRegistro(Instruccion[1])
            imm = Instruccion[2]
            rs = 0

        #Tipo I6
        elif Tipo == "I6":
            rt = buscarRegistro(Instruccion[1])
            rd = buscarRegistro(Instruccion[2])
            rs = Estructura[3]

        #Tipo I7
        elif Tipo == "I7":
            #label
            rt = Estructura[3]
            rs = 0

"""
#print(buscarRegistro(MatrizRegistros, "$s5"))

#imprimir(MatrizInstrucciones)

"""
def hexaAentero(Cadena):
    Cadena = Cadena.replace("0x","")
    return hex(Cadena)

a = 0x400004
b = str(hex(a))
print(a)
print(b)
print(hexaAentero(b))
print(hex(hexaAentero(b)))
"""

ventana.mainloop() #Corre la ventana
