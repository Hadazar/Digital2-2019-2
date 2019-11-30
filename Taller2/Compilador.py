
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
SetInstruccionesR = Tabla.read()
BancoRegistros = open("BancoDeRegistros","r")
Registros = BancoRegistros.read()
CodigoEjemplo = open("Ejemplo","r")
Ejemplo = CodigoEjemplo.read()

MatrizCodigo = ""

def getOpcode():
    print("Opcode: \n")
    print(SetInstrucciones)
    imprimir(MatrizCodigo)

def capturarCodigo():
    global MatrizCodigo
    Codigo = CodigoMips.get(1.0,END)
    MatrizCodigo = convertirAmatriz(Codigo)
    print("Codigo: \n", Codigo)

def borrar():
    CodigoMips.delete(1.0,END)

def convertirAmatriz(Texto):
    Lista = Texto.split("\n")
    n = len(Lista)
    Matriz = [None] * (n-1)
    for i in range(0,n-1):
        Lista[i] = Lista[i].replace(",","")
        Lista[i] = Lista[i].replace("("," ")
        Lista[i] = Lista[i].replace(")","")
        Lista[i] = Lista[i].replace(":","")
        Matriz[i] = Lista[i].split(" ")
    return Matriz

def imprimir(Matriz):
    for i in Matriz:
        print(i)

#Matrices
MatrizIntrsucciones = convertirAmatriz(SetInstrucciones)
MatrizIntrsuccionesR = convertirAmatriz(SetInstruccionesR)
MatrizRegistros = convertirAmatriz(Registros)

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
Estado = Label(ventana, text = Estatus,width=95,height=5, bg = "black", fg = "white").place(x=17,y=450)


ventana.mainloop() #Corre la ventana
