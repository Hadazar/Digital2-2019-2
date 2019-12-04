
from tkinter import *
from math import *
#from PIL import Image, ImageTk as itk

#-----------------------BACK-END:PARTE FUNCIONAL DEL PROGRAMA---------------------------------

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

#Convierte un string (un texto) en una matriz
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

#Matrices
MatrizInstrucciones = convertirAmatriz(SetInstrucciones) #Tipo I y J
MatrizInstruccionesR = convertirAmatriz(SetInstruccionesR)
MatrizHexa = "" #Matriz que almacenará el código hexadecimal

#Borra el texto escrito por el usuario
def borrar():
    CodigoMips.delete(1.0,END)

#Función para imprimir una vector por vector (no hace parte funcional del programa, solo se usó para ir depurando el código)
def imprimir(Matriz):
    for i in Matriz:
        print(i)

#Escribe código en hexadecimal sobre el archivo memfile.dat
def exportar():
    global CodigoHexa
    CodigoHexa.write(MatrizHexa) 
    CodigoHexa.close()

#Busca una instrucción en la lista de instrucciones MIPS
def buscarInstruccion(Matriz, Instruccion):
    EstructuraInstruccion = None
    for i in range(len(Matriz)):
        if Instruccion == Matriz[i][0]:
            EstructuraInstruccion = Matriz[i]
    return EstructuraInstruccion #retorna un vector con la información de la instrución: Tipo de instrucción, opcode, func (para las tipo r) y al valor de algun registro (para algunas instrucciones especiales)

#Encuentra el número que corresponde al registro
def buscarRegistro(Registro):
    NumeroRegistro = None
    for i in range(len(BancoRegistros)):
        if Registro == BancoRegistros[i]:
            NumeroRegistro = i
            break
    return NumeroRegistro

#Detecta los labels en el código, los almacena en un diccionario junto con sus respectivas posiciones de memoria, y los elimina de la matriz que contiene al código
def capturarLabels():
    global MatrizCodigo, Labels #Se especifican globales, porque se pretende editar variables que estan fuera de la función
    n = len(MatrizCodigo) #Cantidad de líneas de código introducidas por el usuario
    i = 0
    while i<n:
        if MatrizCodigo[i][0][-1] == ":": #Identifica el label (Fila i, columna 0, última letra del string = dos puntos(:))
            label = MatrizCodigo[i][0].replace(":","") #Le quita los dos puntos al label
            Labels[label] = DireccionBase+i*4 #Agrega el label a un diccionario y lo asocia con su posición de memoria
            MatrizCodigo.pop(i) #Elimina el label
            n = n-1
        i = i+1

#Función central del programa: convierte una instrucción en su equivalente hexadecimal
def compilarInstruccion(Instruccion,DireccionInstruccion):

    #Inicializa todas las variables necesarias para codificar las instrucciones
    Opcode, rs, rt, rd, Shamt, Func, imm, addr = 0,0,0,0,0,0,0,0
    InstruccionHexa = None #Variable para almacenar el hexadecimal de una instrucción
    Estructura = buscarInstruccion(MatrizInstrucciones, Instruccion[0])#Busca la información de la instrucción (opcode, tipo,...) en la lista tipo I y J
    TipoR = False #Bandera para indicar que no es tipo R

    #Si no las encuentra en la lista de tipo I y J entonces las busca en la lista tipoR
    if Estructura == None:
        #print("buscando en R")
        Estructura = buscarInstruccion(MatrizInstruccionesR, Instruccion[0])
        TipoR = True #Bandera para indicar que es tipo R

    Tipo = Estructura[2] #Específica el tipo de instrucción
    #print("Tipo: ", Tipo)
    
    #Si la instruccion tipo R:
    if TipoR == True:

        Opcode = 0 #El opcode siempre es cero para las tipo R
        Func = int(Estructura[1])

        #Para cada subtipo hay un orden en los registros:

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

        #Multiplica cada parte de la instrucción por su respectiva potencia de dos y suma, así construye la instrucción completa
        InstruccionHexa= Func + Shamt*pow(2,6) + rd*pow(2,11) + rt*pow(2,16) + rs*pow(2,21) + Opcode*pow(2,26)
                    # op rs rt rd shamt func
                    #  6  5  5  5     5    6
                    # 26 =5 +5 +5    +5   +6  => op*2^26
                    #    21= 5 +5    +5   +6  => rs*2^21
                    #       16= 5    +5   +6  => rt*2^16
                    #             11= 5   +6  => rd*2^11
                    #                      6  => shamt*2^6
                    #                         => func

        #print("op: ",Opcode,", rs: ",rs,", rt: ",rt,", rd: ",rd,", shamt: ",Shamt,"\n")
        #print("Hexa: ",hex(int(InstruccionHexa)),"\n")

    #Si la instruccion es tipo I o J:
    elif TipoR == False:

        Opcode = int(Estructura[1])
        TipoJ = False #Bandera para indicar que no es tipo J

        #Para cada subtipo hay un orden en los registros:

        #Tipo J
        if Tipo == "J":
            addr = Labels[Instruccion[1]]/4 #La dirección del label quitandole dos ceros a la derecha
            print(addr)
            TipoJ = True #Bandera para indicar que no es tipo J

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
            imm = (Labels[Instruccion[3]] - (DireccionInstruccion+4))/4 #Cantidad de líneas de código que debe saltar el pc para llegar al label
            rt = int(Estructura[3]) #Para este tipo de instrucción el rt viene con un valor por defecto

        #Tipo I4
        elif Tipo == "I4":
            rs = buscarRegistro(Instruccion[1])
            rt = buscarRegistro(Instruccion[2])
            imm = (Labels[Instruccion[3]] - (DireccionInstruccion+4))/4 

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
            imm = (Labels[Instruccion[3]] - (DireccionInstruccion+4))/4
            rt = int(Estructura[3])
            rs = 0

        #Complemento a 2 para números negativos
        if imm < 0:
            imm = 65536 + imm #(65536)dec=(10000)hex=(FFFF+1)hex

        if TipoJ == False:
            InstruccionHexa= imm + rt*pow(2,16) + rs*pow(2,21) + Opcode*pow(2,26)
                    # op rs rt imm
                    #  6  5  5  16
                    # 26 =5 +5 +16  => op*2^26
                    #    21= 5 +16  => rs*2^21
                    #           16  => rt*2^16
                    #               => imm

            #print("op: ",Opcode,", rs: ",rs,", rt: ",rt,", imm: ",imm,"\n")
            #print("Hexa: ",hex(int(InstruccionHexa)),"\n")
        else:
            InstruccionHexa= addr + Opcode*pow(2,26)
                    # op addr
                    #  6   26
                    #      26  => op*2^26
                    #          => addr

            #print("op: ",Opcode,", addr: ",addr,"\n")
            #print("Hexa: ",hex(int(InstruccionHexa)),"\n")

    return InstruccionHexa

#Convierte todo el código a su equivalente hexadecimal
def compilar():

    global MatrizHexa
    n = len(MatrizCodigo)

    for i in range(len(MatrizCodigo)):

        Instruccion = MatrizCodigo[i]
        DireccionInstruccion = DireccionBase + i*4
        InstruccionHexa = compilarInstruccion(Instruccion,DireccionInstruccion)
        Cadena = str(hex(int(InstruccionHexa))).replace("0x","") #Lo transforma en string y le quita el "0x"
        Cadena = Cadena.zfill(8) #Le añade ceros a la izquierda si hacen falta para completar 8 caracteres
        MatrizHexa = MatrizHexa + Cadena + "\n" #Añade línea por línea a la matriz hexadecimal

#Captura el texto escrito por el usuario en la interfaz, lo convierte en una matriz, extrae y los labels y compila
def capturarCodigo():
    global MatrizCodigo
    Codigo = CodigoMips.get(1.0,END)
    MatrizCodigo = convertirAmatriz(Codigo)
    capturarLabels()
    compilar()


#-----------------------FRONT-END:INTERFAZ GRÁFICA---------------------------------

ventana = Tk() #Crea la ventana

#Configuración de ventana -------------
ventana.title("Compilador MIPS")
ventana.geometry("800x650")
ventana.resizable(0,0) #Bloquear el tamaño de la ventana
ventana.configure(background="#B1C340") #Color de fondo

#Configuración de botones -------------
ColorBoton=("#3FC3D8")
AnchoBoton=6
AltoBoton=3

#Logo
"""
Logo = Image.open("LogoTaller2.png")
Logo.resize((115,17), Image.ANTIALTAS)
Logo = ImageTk.PhotoImage(Logo)
BotonLogo = Button(ventana, image=Logo, text="abc", compound="top")
BotonLogo.place(x=17+115+17+115+17+115+17,y=17)
"""
#Botones -----------------------------
Iniciar = Boton0=Button(ventana,text="Iniciar",bg=ColorBoton,width=AnchoBoton,height=AltoBoton,command=lambda:capturarCodigo()).place(x=362,y=300) #Ejecuta capturarCodigo
Exportar = Boton0=Button(ventana,text="Exportar",bg=ColorBoton,width=AnchoBoton,height=AltoBoton,command=lambda:exportar()).place(x=362,y=400)
BorrarTodo = Boton0=Button(ventana,text="Borrar",bg=ColorBoton,width=AnchoBoton,height=AltoBoton,command=lambda : borrar()).place(x=650,y=160)
Copiar = Boton0=Button(ventana,text="Copiar",bg=ColorBoton,width=AnchoBoton,height=AltoBoton,command=lambda : borrar()).place(x=530,y=160)

#Código MIPS ---------------------------
CodigoMipsEtiqueta = Message(ventana, text = "Escriba su código MIPS aquí:", width = 300, bg="#BEC7C9").place(x=25,y=200)
CodigoMips = Text(ventana,width=35,height=20, padx = 10, pady = 10) #Cuadro de texto para que el usuario escriba el código
CodigoMips.place(x=25,y=250)

CuadroDireccionEtiqueta = Message(ventana, text = "Inserte dirección inicial:", width = 300, bg="#BEC7C9").place(x=25,y=80)
CuadroDireccion = Text(ventana,width=35,height=1, padx = 10, pady = 10)
CuadroDireccion.place(x=25,y=130)

Estatus = 'Compilando...'
Estado = Label(ventana, text = Estatus, width=38, height=21, bg = "black", fg = "white").place(x=469,y=250)

#LogoImg = PhotoImage(file="LogoTaller2.png")
#self.canvas1.create_image(30, 100, image=LogoImg, anchor="nw")
#LogoImg.zoom()

#LogoImg = Image.open("LogoTaller2.png")
#LogoImg.resize((115,17), Image.ANTIALTAS)
#LogoImg = itk.PhotoImage(LogoImg)
#Logo = Label(ventana, width=300,height=80, image=LogoImg).place(x=469,y=20)
"""
LogoImg = PhotoImage(file="LogoTaller2.png")
#LogoImg._
canvas1 = Canvas(ventana)
canvas1.pack(fill=BOTH)
canvas1.create_image(0, 0, image=LogoImg, anchor=NW)
canvas1.place(x=469,y=20)
canvas1.size
"""
LogoImg = PhotoImage(file="LogoTaller2_2.png")
Logo = Label(ventana, width=280,height=110, image=LogoImg).place(x=480,y=25)
#Estado del programa --------------------

"""
Estatus = 'Compilando...'
EstadoEtiqueta = Message(ventana, text = "Estado:", width = 115, bg="#BEC7C9").place(x=17,y=440)
Estado = Label(ventana, text = Estatus, width=95, height=5, bg = "black", fg = "white").place(x=17,y=490)
"""
ventana.mainloop() #Corre la ventana
