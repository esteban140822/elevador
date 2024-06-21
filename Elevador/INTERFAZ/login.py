""" Tecnológico Nacional de México
  
  Instituto Tecnológico de Pachuca
  
  Ingeniería en Sistemas Computacionales

  Materia: Sistemas Programables
  Practica: Elevador con Interfaz Gráfica

  ALUMNO:
  Bautista Arreola Esteban Misael

  Version: Finalizada
  Comentarios: Este archivo login.py es para revisar en la base de datos
  si los datos ingresados son del operador o del administrador, si no corresponden
  mandara un mensaje de datos errones.
  Si ingreso el operador manda los datos a la base de datos.
  
  25/Mayo/2023
"""
from tkinter import *
import tkinter as tk
from PIL import Image
import mysql.connector
import os
from datetime import datetime

# Conexion a la base de datos de donde se esta obteniendo los valores
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="elevador"
)

# Crear una ventana_principal principal
ventana_principal = tk.Tk()
ventana_principal.geometry("300x400") 
ventana_principal.title("LOGIN")

def centrar_ventana_principal(ventana_principal):
    """Centra una ventana_principal de Tkinter en la pantalla."""
    ventana_principal.update_idletasks()
    ancho = ventana_principal.winfo_width()
    altura = ventana_principal.winfo_height()
    x = (ventana_principal.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana_principal.winfo_screenheight() // 2) - (altura // 2)
    ventana_principal.geometry('{}x{}+{}+{}'.format(ancho, altura, x, y))

# Crear la función de inicio de sesión
def login():
    username = username_entry.get()
    password = password_entry.get()
    if username=="admin" and password=="admin":
        ventana_principal.destroy()
        os.system("python "+"admin.py")
    else:
        cursor = db.cursor()
        query = "SELECT idOperador FROM operador WHERE Nombre=%s AND Contrasena=%s"
        cursor.execute(query, (username, password))
        resultado= cursor.fetchone()
        
        if resultado is not None:
            # El usuario ha iniciado sesión correctamente
        
            now = datetime.now()
            fecha_hora_actual = now.strftime("%Y-%m-%d %H:%M:%S")
            print("Inicio de sesión", "Bienvenido, " + username)
            
            lbValores = Label(buttonsSFrame,text = "VALORES CORRECTOS",
            bg="#92C5FC",fg="green",font=("Arial",10))
            lbValores.place(x=70, y=5)

            idOperador=int(resultado[0])
            cursor = db.cursor()
            query = "INSERT INTO ingreso (Inicio,Hora,Operador_idOperador) VALUES (%s, %s,%s)"
            values = ("SI",fecha_hora_actual,idOperador)
            cursor.execute(query, values)
            db.commit()

            ventana_principal.destroy()
            os.system("python "+"main.py")
        else:
            # Las credenciales son incorrectas
            print("INCORRECTO")
            lbValores = Label(buttonsSFrame,text = "VALORES INCORRECTOS",
            bg="#92C5FC",fg="RED",font=("Arial",10))
            lbValores.place(x=70, y=5)

# Funcion para ir a la parte del registro
def registro():
    ventana_principal.destroy()
    os.system("python "+"registro.py")

# Fondos
titleFrame = Frame()
titleFrame.config(bg="white",width="300", height="150")
titleFrame.place(x=0, y=0)

buttonsSFrame=Frame()
buttonsSFrame.config(bg="#92C5FC",width="300", height="250")
buttonsSFrame.place(x=0, y=150)

buttonsInicio=Frame()
buttonsInicio.config(width="100", height="270")
buttonsInicio.place(x=50, y=180)

buttonsSesion=Frame()
buttonsSesion.config(width="100", height="270")
buttonsSesion.place(x=110, y=250)

buttonsCerrar=Frame()
buttonsCerrar.config(width="100", height="270")
buttonsCerrar.place(x=115, y=360)

# Imagenes
image = tk.PhotoImage(file="img/inicio.png")

# Letreros
lbTitulo = Label(titleFrame,text = "INICIO DE SESIÓN",
                 bg="white",fg="black",font=("Arial",15))
lbTitulo.place(x=55, y=100)

lbImagen = Label(titleFrame,image=image)
lbImagen.place(x=105, y=10)

lbValores = Label(buttonsSFrame,text = "Ingrese los valores",
                 bg="#92C5FC",fg="black",font=("Arial",10))
lbValores.place(x=90, y=5)

# Crear los campos de entrada
tk.Label(buttonsInicio, text="Usuario").grid(row=5, column=10)
username_entry = tk.Entry(buttonsInicio)
username_entry.grid(row=5, column=11)

tk.Label(buttonsInicio, text="Contraseña").grid(row=10, column=10)
password_entry = tk.Entry(buttonsInicio, show="*")
password_entry.grid(row=10, column=11)

# Crear el botón de inicio de sesión
tk.Button(buttonsSesion, text="Iniciar sesión", command=login).grid(row=12, column=11)
tk.Button(buttonsCerrar, text="Registrarse", command=registro).grid(row=12, column=11)

# Mostrar la ventana_principal principal
centrar_ventana_principal(ventana_principal)
ventana_principal.mainloop()
