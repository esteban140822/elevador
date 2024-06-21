""" Tecnológico Nacional de México
  
  Instituto Tecnológico de Pachuca
  
  Ingeniería en Sistemas Computacionales

  Materia: Sistemas Programables
  Practica: Elevador con Interfaz Gráfica

  ALUMNO:
  Bautista Arreola Esteban Misael

  Version: Finalizada
  Comentarios: Este archivo main.py es para mover el elevador una vez el operador se haya hecho login
  y tambien si el elevador esta en modo de boton de panico, si no es asi solo se puede ver como
  como se mueve el elevador.
  
  25/Mayo/2023
"""
from tkinter import *
from PIL import Image
import tkinter as tk
import mysql.connector
from datetime import datetime
import os
import serial,time
arduino = serial.Serial('COM3',9600)

# Tamaño de pantalla
ventana_principal = Tk()
ventana_principal.geometry("512x588") 
ventana_principal.title("ELEVADOR")

# Base de datos donde se esta guardando y recolectando información
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="elevador"
)

# Formato de dia y hora actual
hora_actual = datetime.now()
fecha_hora_actual = hora_actual.strftime("%Y-%m-%d %H:%M:%S")

# Funciones

def piso_1():
    arduino.write(b"1")
    time.sleep(1)

def piso_2():
    arduino.write(b"2")
    time.sleep(1)

def piso_3():
    arduino.write(b"3")
    time.sleep(1)

def piso_4():
    arduino.write(b"4")
    time.sleep(1)

def automatico():
    arduino.write(b"A")
    time.sleep(1)
    lbboton_manual = Label(fondo_botones,image=image_R,width="10",height="10")
    lbboton_manual.place(x=230, y=362)
    lbboton_automa = Label(fondo_botones,image=image_V,width="10",height="10")
    lbboton_automa.place(x=230, y=322)

# Funcion para que el elevador vuelva a la normalidad
def reiniciar():
    arduino.write(b"C")
    time.sleep(2)
    arduino.write(b"6")
    time.sleep(1)

# Funcion para cambiar a modo manual
def mover_man():
    arduino.write(b"7")
    time.sleep(1)
    lbboton_manual = Label(fondo_botones,image=image_V,width="10",height="10")
    lbboton_manual.place(x=230, y=362)
    lbboton_automa = Label(fondo_botones,image=image_R,width="10",height="10")
    lbboton_automa.place(x=230, y=322)

# Funciones de los botones para mover manualmente el elevador
def subir_send_continuously():
    arduino.write(b"S")
    time.sleep(1)
    if button_pressed:
        ventana_principal.after(100, subir_send_continuously)

def subir_button_press(event):
    global button_pressed
    button_pressed = True
    subir_send_continuously()

def bajar_send_continuously():
    arduino.write(b"B")
    time.sleep(1)
    if button_pressed:
        ventana_principal.after(100, bajar_send_continuously)

def bajar_button_press(event):
    global button_pressed
    button_pressed = True
    bajar_send_continuously()

def button_release(event):
    global button_pressed
    button_pressed = False

button_pressed = False
# Obtener el valor del id del Operador y el nombre -----------------
valor_id = db.cursor()
valor_id.execute("SELECT Operador_idOperador FROM ingreso WHERE (Hora BETWEEN DATE_SUB(NOW(), INTERVAL 30 SECOND) AND NOW()) AND Inicio='SI'")
resultado_1= valor_id.fetchone()
idOperador = int(resultado_1[0])
valor_nombre = db.cursor()
valor_nombre.execute("select Nombre from operador,ingreso where Operador_idOperador=idOperador and Inicio='SI' and (Hora BETWEEN DATE_SUB(NOW(), INTERVAL 30 SECOND) AND NOW())")
resultado_2 = valor_nombre.fetchone()
nom_operador= str(resultado_2[0])

# Funcion para Cerrar la sesión del operador y quede registrado
def cerrarInterfaz():
    cursor = db.cursor()
    query = "INSERT INTO ingreso (Inicio,Hora,Operador_idOperador) VALUES (%s, %s,%s)"
    values = ("NO",fecha_hora_actual,idOperador)
    cursor.execute(query, values)
    db.commit()
    ventana_principal.destroy()
    arduino.close()
    os.system("python "+"login.py")    

# Funcion para abrir puerta
def abrirPuerta():
    arduino.write(b"O")
    time.sleep(2)
    arduino.write(b"9")
    time.sleep(1)

# Funcion para cerrar puerta
def cerrarPuerta():
    arduino.write(b"J")
    time.sleep(2)
    arduino.write(b"8")
    time.sleep(1)

# Funcion que lee y manda los valores para saber donde esta el elevador
def piso():
    if arduino.in_waiting > 0:
        now = datetime.now()
        fecha_hora_actual = now.strftime("%Y-%m-%d %H:%M:%S")
        mensaje= arduino.readline().decode('utf-8').rstrip()
        titulo=(mensaje[:4])
        titulo_2=(mensaje[:11])
        titulo_3=(mensaje[:8])
        titulo_4=(mensaje[:7])
        if(titulo=="PISO"):
            nivel=(mensaje[:6])
            puerta=(mensaje[7:14])
            distancia=(mensaje[15:19])
            lbPiso.config(text=" "+nivel)
            lbPuerta.config(text="PUERTA "+puerta)
            lbDistancia.config(text=" "+distancia)
            cursor = db.cursor()
            query = "INSERT INTO posicion (Piso,Hora,Puerta,Distancia,Operador_idOperador) VALUES (%s,%s,%s,%s,%s)"
            values= (nivel,fecha_hora_actual,puerta,distancia,idOperador)
            cursor.execute(query,values)
            db.commit()
        elif(titulo_2=="PLANTA BAJA"):
            nivel=(mensaje[:11])
            puerta=(mensaje[12:19])
            distancia=(mensaje[20:24])
            lbPiso.config(text=" "+titulo_2)
            lbPuerta.config(text="PUERTA "+puerta)
            lbDistancia.config(text=" "+distancia)
            cursor = db.cursor()
            query = "INSERT INTO posicion (Piso,Hora,Puerta,Distancia,Operador_idOperador) VALUES (%s,%s,%s,%s,%s)"
            values= (nivel,fecha_hora_actual,puerta,distancia,idOperador)
            cursor.execute(query,values)
            db.commit()
        elif(titulo_3=="DETENIDO"):
            lbboton = Label(fondo_botones,image=image_R,width="10",height="10")
            lbboton.place(x=132, y=48)
            nivel=(mensaje[:8])
            puerta=(mensaje[9:16])
            distancia=(mensaje[17:21])
            lbPiso.config(text=" "+titulo_3)
            lbPuerta.config(text="PUERTA "+puerta)
            lbDistancia.config(text=" "+distancia)
            cursor = db.cursor()
            query = "INSERT INTO posicion (Piso,Hora,Puerta,Distancia,Operador_idOperador) VALUES (%s,%s,%s,%s,%s)"
            values= (nivel,fecha_hora_actual,puerta,distancia,idOperador)
            cursor.execute(query,values)
            db.commit()
        elif(titulo_3=="CONTINUA"):
            lbboton = Label(fondo_botones,image=image_V,width="10",height="10")
            lbboton.place(x=132, y=48)
            lbboton_manual = Label(fondo_botones,image=image_R,width="10",height="10")
            lbboton_manual.place(x=230, y=362)
            lbboton_automa = Label(fondo_botones,image=image_V,width="10",height="10")
            lbboton_automa.place(x=230, y=322)
            nivel=(mensaje[:8])
            puerta=(mensaje[9:16])
            distancia=(mensaje[17:21])
            lbPiso.config(text=" "+titulo_3)
            lbPuerta.config(text="PUERTA "+puerta)
            lbDistancia.config(text=" "+distancia)
            cursor = db.cursor()
            query = "INSERT INTO posicion (Piso,Hora,Puerta,Distancia,Operador_idOperador) VALUES (%s,%s,%s,%s,%s)"
            values= (nivel,fecha_hora_actual,puerta,distancia,idOperador)
            cursor.execute(query,values)
            db.commit()   
        elif(titulo_3=="SUBIENDO"):
            nivel=(mensaje[:8])
            puerta=(mensaje[9:16])
            distancia=(mensaje[17:20])
            lbPiso.config(text=" "+titulo_3)
            lbPuerta.config(text="PUERTA "+puerta)
            lbDistancia.config(text=" "+distancia)
            cursor = db.cursor()
            query = "INSERT INTO posicion (Piso,Hora,Puerta,Distancia,Operador_idOperador) VALUES (%s,%s,%s,%s,%s)"
            values= (nivel,fecha_hora_actual,puerta,distancia,idOperador)
            cursor.execute(query,values)
            db.commit()    
        elif(titulo_4=="BAJANDO"):
            nivel=(mensaje[:7])
            puerta=(mensaje[8:15])
            distancia=(mensaje[16:19])
            lbPiso.config(text=" "+titulo_4)
            lbPuerta.config(text="PUERTA "+puerta)
            lbDistancia.config(text=" "+distancia)
            cursor = db.cursor()
            query = "INSERT INTO posicion (Piso,Hora,Puerta,Distancia,Operador_idOperador) VALUES (%s,%s,%s,%s,%s)"
            values= (nivel,fecha_hora_actual,puerta,distancia,idOperador)
            cursor.execute(query,values)
            db.commit() 
    ventana_principal.after(10,piso)

def centrar_ventana(ventana_principal):
    """Centra una ventana de Tkinter en la pantalla."""
    ventana_principal.update_idletasks()
    ancho = ventana_principal.winfo_width()
    altura = ventana_principal.winfo_height()
    x = (ventana_principal.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana_principal.winfo_screenheight() // 2) - (altura // 2)
    ventana_principal.geometry('{}x{}+{}+{}'.format(ancho, altura, x, y))


# Fondos
fondo_titulo = Frame()
fondo_titulo.config(bg="black",width="512", height="88")
fondo_titulo.place(x=0, y=0)

fondo_botones=Frame()
fondo_botones.config(bg="#3B83BD",width="512", height="500")
fondo_botones.place(x=0, y=80)

# Etiqueta con imagen.
image = tk.PhotoImage(file="img/elevator.png")
label = tk.Label(fondo_botones,image=image,width="512", height="512")
label.pack()

image_V = tk.PhotoImage(file="img/boton_V.png")
label_V = tk.Label(fondo_botones,image=image,width="10", height="10")

image_R = tk.PhotoImage(file="img/boton_R.png")
label_R = tk.Label(fondo_botones,image=image,width="10", height="10")

# Letreros
lbTitulo = Label(fondo_titulo,text = f"BIENVENIDO {nom_operador}, PUEDE MOVER EL ELEVADOR",
                 bg="black",fg="white",font=("Arial",14))
lbTitulo.place(x=10, y=20)

lbPiso = Label(fondo_botones,text = " ",
                 bg="black",fg="white",font=("Arial",15))
lbPiso.place(x=150, y=40)

lbboton = Label(fondo_botones,image=image_V,width="10",height="10")
lbboton.place(x=132, y=48)

lbboton_manual = Label(fondo_botones,image=image_R,width="10",height="10")
lbboton_manual.place(x=230, y=362)
lbTitulo_manual = Label(fondo_botones,text = "manual",bg="white",fg="black",font=("Arial",8))
lbTitulo_manual.place(x=250, y=360)

lbboton_automa = Label(fondo_botones,image=image_V,width="10",height="10")
lbboton_automa.place(x=230, y=322)
lbTitulo_automa = Label(fondo_botones,text = "automático",bg="white",fg="black",font=("Arial",8))
lbTitulo_automa.place(x=250, y=320)

lbPuerta = Label(fondo_botones,text = "PUERTA ",
                 bg="black",fg="white",font=("Arial",15))
lbPuerta.place(x=130, y=470)

lbDistancia = Label(fondo_botones,text = " ",
                 bg="black",fg="white",font=("Arial",12))
lbDistancia.place(x=330, y=42)

# Botones
btnPiso_1 = Button(fondo_botones,text="Piso PB",command = piso_1)
btnPiso_1.place(x=116,y=370)

btnPiso_2 = Button(fondo_botones,text="Piso 1",command = piso_2)
btnPiso_2.place(x=120,y=310)

btnPiso_3 = Button(fondo_botones,text="Piso 2",command = piso_3)
btnPiso_3.place(x=120,y=250)

btnPiso_4 = Button(fondo_botones,text="Piso 3",command = piso_4)
btnPiso_4.place(x=120,y=190)

btnNo_Mover = Button(fondo_botones,bg="black",fg="white",text="Automático",command = automatico)
btnNo_Mover.place(x=400,y=90)

btnReiniciar = Button(fondo_botones,bg="black",fg="white",text="Continuar",command = reiniciar)
btnReiniciar.place(x=405,y=150)

btnSubir = Button(fondo_botones,bg="#bdecb6",fg="white",text="   ")
btnSubir.bind("<ButtonPress>", subir_button_press)
btnSubir.bind("<ButtonRelease>", button_release)
btnSubir.place(x=428,y=220)

btnBajar = Button(fondo_botones,bg="#F3464A",fg="white",text="   ")
btnBajar.bind("<ButtonPress>", bajar_button_press)
btnBajar.bind("<ButtonRelease>", button_release)
btnBajar.place(x=427,y=310)

btnManual = Button(fondo_botones,bg="black",fg="white",text="Manual",command = mover_man)
btnManual.place(x=410,y=370)

btnPuerta_Abierta = Button(fondo_botones,bg="white",fg="black",text="Abrir",command = abrirPuerta)
btnPuerta_Abierta.place(x=160,y=440)

btnPuerta_Cerrada = Button(fondo_botones,bg="white",fg="black",text="Cerrar",command = cerrarPuerta)
btnPuerta_Cerrada.place(x=235,y=440)

btnCerrar = Button(fondo_botones,bg="black",fg="white",text="Cerrar",command = cerrarInterfaz)
btnCerrar.place(x=415,y=465)

piso()
# Mostrar la ventana principal
centrar_ventana(ventana_principal)
ventana_principal.mainloop()
