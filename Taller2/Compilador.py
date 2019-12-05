
from tkinter import *
from math import *
from random import randrange
#from PIL import Image, ImageTk as itk

#-----------------------BACK-END: PARTE FUNCIONAL DEL PROGRAMA---------------------------------

#Tablas de instrucciones y registros MIPS
Tabla = open("InstruccionesMIPS","r")#Instrucciones tipo I y J
SetInstrucciones = Tabla.read()
TablaR = open("InstruccionesTipoR","r")#Instrucciones tipo R
SetInstruccionesR = TablaR.read()
TablaF = open("InstruccionesTipoF","r")#Instrucciones tipo F
SetInstruccionesF = TablaF.read()
BancoRegistros = open("BancoDeRegistros","r")#Banco de registros
Registros = BancoRegistros.read()
BancoRegistros = Registros.split(" ")#Vector que contiene los registros
BancoRegistrosF = open("BancoDeRegistrosF","r")#Banco de registros de punto flotante (tipo F)
RegistrosF = BancoRegistrosF.read()
BancoRegistrosF = RegistrosF.split(" ")#Vector que contiene los registros F

MatrizCodigo = []#Matriz que almacena el código escrito por el usuario
Labels = {} #Diccionario para almacenar los label y sus direcciones de memoria
DireccionBase = None

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
MatrizInstruccionesF = convertirAmatriz(SetInstruccionesF)
MatrizHexa = "" #Matriz que almacenará el código hexadecimal

#Borra el texto escrito por el usuario
def borrar():
    CodigoMips.delete(1.0,END)

#Función para imprimir una vector por vector (no hace parte funcional del programa, solo se usó para ir depurando el código)
def imprimir(Matriz):
    for i in Matriz:
        print(i)

#Complemento a 2 para números negativos
def complementoAdos(num):
    Complemento = num
    if num < 0:
        Complemento = 65536 + num #(65536)dec=(10000)hex=(FFFF+1)hex
    return Complemento

#Escribe código en hexadecimal sobre el archivo memfile.dat
def exportar():
    NombreArchivo = CuadroExportacion.get(1.0,END) + ".dat" #Obtiene el nombre del archivo de la interfaz y le agrega la extensión .dat
    NombreArchivo = NombreArchivo.replace("\n","") #Quita el salto de línea al final del nombre
    CodigoHexa = open(NombreArchivo,"w")#Archivo sobre el cual se exporta el hexadecimal
    CodigoHexa.write("")
    CodigoHexa.write(MatrizHexa) 
    CodigoHexa.close()
    TextoExportado = "Exportado como: \"" + NombreArchivo +"\""
    Estatus.set(Estatus.get().replace("Compilado y listo para exportar",TextoExportado))


#Busca una instrucción en la lista de instrucciones MIPS
def buscarInstruccion(Matriz, Instruccion):
    EstructuraInstruccion = None
    for i in range(len(Matriz)):
        if Instruccion == Matriz[i][0]:
            EstructuraInstruccion = Matriz[i]
    return EstructuraInstruccion #retorna un vector con la información de la instrución: Tipo de instrucción, opcode, func (para las tipo r) y al valor de algun registro (para algunas instrucciones especiales)

#Encuentra el número que corresponde al registro
def buscarRegistro(Registro, Banco):
    NumeroRegistro = None
    for i in range(len(Banco)):
        if Registro == Banco[i]:
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
    Opcode, rs, rt, rd, Shamt, Func, imm, addr, cop, fd, fs, ft = 0,0,0,0,0,0,0,0,0,0,0,0
    InstruccionHexa = None #Variable para almacenar el hexadecimal de una instrucción
    Estructura = buscarInstruccion(MatrizInstrucciones, Instruccion[0])#Busca la información de la instrucción (opcode, tipo,...) en la lista tipo I y J
    TipoR = False #Bandera para indicar que no es tipo R
    TipoF = False

    #Si no las encuentra en la lista de tipo I y J entonces las busca en la lista tipo R
    if Estructura == None:
        #print("buscando en R")
        Estructura = buscarInstruccion(MatrizInstruccionesR, Instruccion[0])
        TipoR = True #Bandera para indicar que es tipo R
    
    #Si tampoco las encuentra en la tipo R las busca en la tipo F
    if Estructura == None:
        #print("buscando en F")
        Estructura = buscarInstruccion(MatrizInstruccionesF, Instruccion[0])
        TipoR = False
        TipoF = True #Bandera para indicar que es tipo R

    Tipo = Estructura[2] #Específica el tipo de instrucción
    #print("Tipo: ", Tipo)
    
    #Si la instruccion tipo R:
    if TipoR == True:

        Opcode = 0 #El opcode siempre es cero para las tipo R
        Func = int(Estructura[1])

        #Para cada subtipo hay un orden en los registros:

        #Tipo R1
        if Tipo == "R1":
            rd = buscarRegistro(Instruccion[1], BancoRegistros) 
            rs = buscarRegistro(Instruccion[2], BancoRegistros) 
            rt = buscarRegistro(Instruccion[3], BancoRegistros)
            Shamt = 0

        #Tipo R2
        elif Tipo == "R2":
            rd = buscarRegistro(Instruccion[1], BancoRegistros) 
            rt = buscarRegistro(Instruccion[2], BancoRegistros) 
            rs = buscarRegistro(Instruccion[3], BancoRegistros)
            Shamt = 0

        #Tipo R3
        elif Tipo == "R3":
            rd = buscarRegistro(Instruccion[1], BancoRegistros) 
            rt = buscarRegistro(Instruccion[2], BancoRegistros) 
            if Instruccion[3][0:2] == "0x" or  Instruccion[3][0:2] == "0X": #Si el imm esta escrito en hexadecimal
                Shamt = stringAHexa(Instruccion[3])
            else: Shamt = int(Instruccion[3])  #Si el imm esta escrito en decimal
            rs = 0

        #Tipo R4
        elif Tipo == "R4":
            rs = buscarRegistro(Instruccion[1], BancoRegistros)
            rt = 0
            rd = 0
            Shamt = 0

        #Tipo R5
        elif Tipo == "R5":
            rd = buscarRegistro(Instruccion[1], BancoRegistros)
            rt = 0
            rs = 0
            Shamt = 0

        #Tipo R6
        elif Tipo == "R6":
            rs = buscarRegistro(Instruccion[1], BancoRegistros)
            rt = buscarRegistro(Instruccion[2], BancoRegistros)
            rd = 0
            Shamt = 0

        #Tipo R+
        elif Tipo == "R+":
            rs = buscarRegistro(Instruccion[1], BancoRegistros)
            rt = buscarRegistro(Instruccion[2], BancoRegistros)
            rd = 0
            Shamt = 0
            Opcode = int(Estructura[1])
            Func = int(Estructura[3])

        #Tipo R-
        elif Tipo == "R-":
            rs = 0
            rt = 0
            rd = 0
            Shamt = 0

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

    #Si la instrucción es tipo F:
    elif TipoF == True:

        Opcode = 17 #El opcode siempre es cero para las tipo R
        Func = int(Estructura[1])
        cop = int(Estructura[3]) #Precisión de la instrucción: single o double

        #Tipo F1
        if Tipo == "F1":
            fd = 2 * buscarRegistro(Instruccion[1], BancoRegistrosF) #Los registros F estan númerados de dos en dos
            fs = 2 * buscarRegistro(Instruccion[2], BancoRegistrosF)
            ft = 2 * buscarRegistro(Instruccion[3], BancoRegistrosF)

        #Tipo F2
        if Tipo == "F2":
            fd = 2 * buscarRegistro(Instruccion[1], BancoRegistrosF)
            fs = 2 * buscarRegistro(Instruccion[2], BancoRegistrosF)
            ft = 0

        #Tipo F3
        if Tipo == "F3":
            fs = 2 * buscarRegistro(Instruccion[1], BancoRegistrosF)
            ft = 2 * buscarRegistro(Instruccion[2], BancoRegistrosF)
            fd = 0
        
        InstruccionHexa= Func + fd*pow(2,6) + fs*pow(2,11) + ft*pow(2,16) + cop*pow(2,21) + Opcode*pow(2,26)
                    # op cop ft fs fd func
                    #  6  5  5  5  5  6
                    # 26 =5 +5 +5 +5  +6  => op*2^26
                    #    21= 5 +5 +5  +6  => cop*2^21
                    #       16= 5 +5  +6  => ft*2^16
                    #          11= 5  +6  => fs*2^11
                    #                  6  => fd*2^6
                    #                     => func
        #print("op: ",Opcode,", fs: ",fs,", ft: ",ft,", fd: ",fd,", cop: ",cop,"\n")

    #Si la instruccion es tipo I o J:
    else:

        Opcode = int(Estructura[1])
        TipoJ = False #Bandera para indicar que no es tipo J

        #Para cada subtipo hay un orden en los registros:

        #Tipo J
        if Tipo == "J":
            addr = Labels[Instruccion[1]]/4 #La dirección del label quitandole dos ceros a la derecha
            print(addr)
            TipoJ = True #Bandera para indicar que si es tipo J

        #Tipo I1
        elif Tipo == "I1":
            rt = buscarRegistro(Instruccion[1], BancoRegistros)
            rs = buscarRegistro(Instruccion[2], BancoRegistros)
            #Si el imm esta escrito en hexadecimal
            if Instruccion[3][0:2] == "0x" or  Instruccion[3][0:2] == "0X":
                imm = stringAHexa(Instruccion[3])
            else: imm = int(Instruccion[3])  #Si el imm esta escrito en decimal

        #Tipo I2
        elif Tipo == "I2":
            rt = buscarRegistro(Instruccion[1], BancoRegistros)
            if Instruccion[2][0:2] == "0x" or  Instruccion[2][0:2] == "0X": #Si el imm esta escrito en hexadecimal
                imm = stringAHexa(Instruccion[2])
            else: imm = int(Instruccion[2])  #Si el imm esta escrito en decimal
            rs = buscarRegistro(Instruccion[3], BancoRegistros)

        #Tipo I+
        elif Tipo == "I+":
            rt = 2 * buscarRegistro(Instruccion[1], BancoRegistrosF) #debería ser ft, pero se dejó rt para ser consistente con las otras instrucciones tipo I
            if Instruccion[2][0:2] == "0x" or  Instruccion[2][0:2] == "0X": #Si el imm esta escrito en hexadecimal
                imm = stringAHexa(Instruccion[2])
            else: imm = int(Instruccion[2])  #Si el imm esta escrito en decimal
            rs = buscarRegistro(Instruccion[3], BancoRegistros)

        #Tipo I3
        elif Tipo == "I3":
            rs = buscarRegistro(Instruccion[1], BancoRegistros)
            imm = (Labels[Instruccion[2]] - (DireccionInstruccion+4))/4 #Cantidad de líneas de código que debe saltar el pc para llegar al label
            rt = int(Estructura[3]) #Para este tipo de instrucción el rt viene con un valor por defecto

        #Tipo I4
        elif Tipo == "I4":
            rs = buscarRegistro(Instruccion[1], BancoRegistros)
            rt = buscarRegistro(Instruccion[2], BancoRegistros)
            imm = (Labels[Instruccion[3]] - (DireccionInstruccion+4))/4 

        #Tipo I5
        elif Tipo == "I5":
            rt = buscarRegistro(Instruccion[1], BancoRegistros)
            if Instruccion[2][0:2] == "0x" or  Instruccion[2][0:2] == "0X": #Si el imm esta escrito en hexadecimal
                imm = stringAHexa(Instruccion[2])
            else: imm = int(Instruccion[2])  #Si el imm esta escrito en decimal
            rs = 0

        #Tipo I6
        elif Tipo == "I6":
            rt = buscarRegistro(Instruccion[1], BancoRegistros)
            rd = buscarRegistro(Instruccion[2], BancoRegistros)
            rs = int(Estructura[3])

        #Tipo I7
        elif Tipo == "I7":
            imm = (Labels[Instruccion[1]] - (DireccionInstruccion+4))/4
            rt = int(Estructura[3])
            rs = 0
        
        imm = complementoAdos(imm) #Le hace complemtento a dos solo si es negativo, sino lo deja igual

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
    MatrizHexa = "" #Vacia la matriz
    n = len(MatrizCodigo)

    Estatus.set(Estatus.get() + "\n" + "Dirección:          " + "Instrucción:\n")

    for i in range(len(MatrizCodigo)):

        Instruccion = MatrizCodigo[i]
        DireccionInstruccion = DireccionBase + i*4
        InstruccionHexa = compilarInstruccion(Instruccion,DireccionInstruccion)

        Cadena = str(hex(int(InstruccionHexa))) #Convierte la instrucción en string hexadecimal
        Cadena = Cadena.replace("0x","") #Lo transforma en string y le quita el "0x"
        Cadena = Cadena.zfill(8) #Le añade ceros a la izquierda si hacen falta para completar 8 caracteres

        Direccion = str(hex(int(DireccionInstruccion)))
        Direccion = Direccion.replace("0x","")
        Direccion = Direccion.zfill(8)

        Estatus.set(Estatus.get() + "\n0x" + Direccion.upper() + "      0x"+ Cadena.upper()) #Actualiza elcuadro de estado del programa
        MatrizHexa = MatrizHexa + Cadena.upper() + "\n" #Añade línea por línea a la matriz hexadecimal
    
    Estatus.set(Estatus.get().replace("Compilando...","Compilado y listo para exportar"))

#Captura el texto escrito por el usuario en la interfaz, lo convierte en una matriz, extrae y los labels y compila

#Covierte un hexadecimal (escrito como string) en un entero
def stringAHexa(Palabra):
    Palabra = Palabra.replace("0x","")
    Palabra = Palabra.replace("0X","")
    Palabra = Palabra.replace("\n","")
    Valor = 0
    for i in range(len(Palabra)):
        Cifra = 0
        if Palabra[-1-i] == "A" or Palabra[-1-i] == "a":
            Cifra = 10
        elif Palabra[-1-i] == "B" or Palabra[-1-i] == "b":
            Cifra = 11
        elif Palabra[-1-i] == "C" or Palabra[-1-i] == "c":
            Cifra = 12
        elif Palabra[-1-i] == "D" or Palabra[-1-i] == "d":
            Cifra = 13
        elif Palabra[-1-i] == "E" or Palabra[-1-i] == "e":
            Cifra = 14
        elif Palabra[-1-i] == "F" or Palabra[-1-i] == "f":
            Cifra = 15
        else: Cifra = int(Palabra[-1-i])
        Valor = Valor + int(Cifra*pow(16,i))
    return Valor

def capturarCodigo():
    global MatrizCodigo, DireccionBase

    Estatus.set("\nEstado: Compilando...\n")

    DireccionBase = stringAHexa(CuadroDireccion.get(1.0,END))
    Codigo = CodigoMips.get(1.0,END)
    MatrizCodigo = convertirAmatriz(Codigo)
    capturarLabels()
    compilar()

def extraerEjemplo():
    NumeroAleatorio = randrange(7)+1 #Número de 0 a 7(hay 7 ejemplos)
    NumeroAleatorio = str(NumeroAleatorio)
    Ubicacion = "Ejemplos/" + NumeroAleatorio #Ruta del ejemplo
    Ejemplo = open(Ubicacion,"r")
    Ejemplo = Ejemplo.read()
    Ejemplo = Ejemplo.strip() #Elimina el salto de línea al final del txt
    DireccionEjemplo = Ejemplo[0:10] #Dirección base del ejemplo
    Ejemplo = Ejemplo.replace(DireccionEjemplo + "\n","") #Quita la dirección del txt
    CuadroDireccion.delete(1.0,END) #Borra el contenido del cuadro de texto de dirección
    borrar() #Borra el contenido del cuadro de código assembler
    CuadroDireccion.insert(END,DireccionEjemplo) #Inserta la dirección del ejemplo en la interfaz
    CodigoMips.insert(END,Ejemplo) #Inserta el código del ejemplo en la interfaz

#-----------------------FRONT-END:INTERFAZ GRÁFICA---------------------------------

ventana = Tk() #Crea la ventana

#Configuración de ventana -------------
ventana.title("Compilador MIPS")
ventana.geometry("800x650")
ventana.resizable(0,0) #Bloquear el tamaño de la ventana
ventana.configure(background="#43B1C5") #Color de fondo

#Logo ----------------------------
LogoImg = PhotoImage(file="LogoTaller2_2.png")
Logo = Label(ventana, width=280,height=110, image=LogoImg).place(x=480,y=25)


#Configuración de botones -------------
ColorBoton=("#F3F039")
AnchoBoton=6
AltoBoton=3

#Botones -----------------------------

Iniciar = Boton0=Button(ventana,bg=ColorBoton,text="Iniciar",width=AnchoBoton,height=AltoBoton,command=lambda:capturarCodigo())#Ejecuta capturarCodigo
Iniciar.place(x=362,y=310)

Exportar = Boton0=Button(ventana,text="Exportar",bg=ColorBoton,width=AnchoBoton,height=AltoBoton,command=lambda:exportar())
Exportar.place(x=362,y=410)

BorrarTodo = Boton0=Button(ventana,text="Borrar",bg=ColorBoton,width=AnchoBoton,height=AltoBoton,command=lambda : borrar())
BorrarTodo.place(x=650,y=170)

Ejemplo = Boton0=Button(ventana,text="Ejemplo",bg=ColorBoton,width=AnchoBoton,height=AltoBoton,command=lambda : extraerEjemplo())
Ejemplo.place(x=530,y=170)

#Archivo de exportación
CuadroExportacionEtiqueta = Message(ventana, text = "Inserte el nombre del archivo de exportación:", width = 300, bg="#BEC7C9").place(x=25,y=20)
CuadroExportacion = Text(ventana,width=35,height=1, padx = 10, pady = 10)
CuadroExportacion.place(x=25,y=60)
CuadroExportacion.insert(END,"memfile")

#Dirección base
CuadroDireccionEtiqueta = Message(ventana, text = "Inserte dirección inicial:", width = 300, bg="#BEC7C9").place(x=25,y=120)
CuadroDireccion = Text(ventana,width=35,height=1, padx = 10, pady = 10)
CuadroDireccion.place(x=25,y=160)
CuadroDireccion.insert(END,"0x00400000")

#Código MIPS ---------------------------
CodigoMipsEtiqueta = Message(ventana, text = "Escriba su código MIPS aquí:", width = 300, bg="#BEC7C9").place(x=25,y=220)
CodigoMips = Text(ventana,width=33,height=19, padx = 20, pady = 20) #Cuadro de texto para que el usuario escriba el código
CodigoMips.place(x=25,y=260)

#Estado del programa --------------------
Estatus = StringVar() #Para poder editar dinámicamente
Estatus.set("\nEstado: Esperando a que el usuario pulse iniciar para realizar compilación...")
Estado = Label(ventana, textvariable = Estatus, width=35, height=20, bg = "black", fg = "white", justify = "left", anchor = "n", padx = 10, pady = 10, wraplength = 300).place(x=469,y=260)


ventana.mainloop() #Corre la ventana
