
from tkinter import *
from math import *

ventana = Tk() #Crea la ventana

#Configuración de ventana -------------
ventana.title("Compilador MIPS")
ventana.geometry("800x600")
ventana.configure(background="#B1C340")

#Configuración de botones -------------
ColorBoton=("#3FC3D8")
AnchoBoton=11
AltoBoton=3

def getOpcode():
    print("Opcode: \n")

#Botones -----------------------------
Iniciar = Boton0=Button(ventana,text="Iniciar",bg=ColorBoton,width=AnchoBoton,height=AltoBoton,command=getOpcode).place(x=17,y=17)
Exportar = Boton0=Button(ventana,text="Exportar",bg=ColorBoton,width=AnchoBoton,height=AltoBoton,command=getOpcode).place(x=17+115+17,y=17)

#Código MIPS ---------------------------
CodigoMips = Text(ventana,width=95,height=15, padx = 10, pady = 10).place(x=17,y=100)
#CodigoMips.pack()
CodigoMips.insert(END,"Escriba aquí su código Mips...")

#Estado del programa --------------------
Estatus = 'Compilando...'
EstadoEtiqueta = Message(ventana, text = "Estado:", width = 115, bg="#BEC7C9").place(x=17,y=400)
Estado = Label(ventana, text = Estatus,width=95,height=5, bg = "black", fg = "white").place(x=17,y=450)

ventana.mainloop() #Corre la ventana
