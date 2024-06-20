""" Tecnológico Nacional de México
  
  Instituto Tecnológico de Pachuca
  
  Ingeniería en Sistemas Computacionales

  Materia: Sistemas Programables
  Practica: Elevador con Interfaz Gráfica

  ALUMNOS:
  Bautista Arreola Esteban Misael
  Ibarra Hernández Héctor Napoleón 

  Version: Finalizada
  Comentarios: Este archivo admin.py es unicamente para registrar un nuevo operador.
  
  25/Mayo/2023
"""
from tkinter import *
import tkinter as tk
import mysql.connector
import os

# Configurar la conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="elevador"
)

# Crear una ventana principal
ventana_principal = tk.Tk()
ventana_principal.geometry("500x350") 
ventana_principal.title("REGISTRO")

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
fondo_titulo.config(bg="gray",width="500", height="80")
fondo_titulo.place(x=0, y=0)

fondo_botones=Frame()
fondo_botones.config(bg="orange",width="500", height="270")
fondo_botones.place(x=0, y=80)

boton_inicio=Frame()
boton_inicio.config(width="200", height="270")
boton_inicio.place(x=140, y=100)

boton_registro=Frame()
boton_registro.config(width="200", height="270")
boton_registro.place(x=200, y=150)

boton_cerrar=Frame()
boton_cerrar.config(width="200", height="270")
boton_cerrar.place(x=205, y=270)

# Letreros
lbTitulo = Label(fondo_titulo,text = "REGISTRO",
                 bg="gray",fg="white",font=("Arial",15))
lbTitulo.place(x=180, y=20)

# Crear los campos de entrada
tk.Label(boton_inicio, text="Nombre").grid(row=0, column=0)
campo_nombre = tk.Entry(boton_inicio)
campo_nombre.grid(row=0, column=1)

tk.Label(boton_inicio, text="Contraseña").grid(row=1, column=0)
password_entry = tk.Entry(boton_inicio, show="*")
password_entry.grid(row=1, column=1)

# Crear la función de registro
def registro():
    nombre = campo_nombre.get()
    contrasena = password_entry.get()
    if(nombre=="" and contrasena==""):
        print("PARAMETROS VACIOS")
    else:
        cursor = db.cursor()
        query = "INSERT INTO operador (Nombre,Contrasena) VALUES (%s, %s)"
        values = (nombre, contrasena)
        cursor.execute(query, values)
        db.commit()
        print("REGISTRO EXITOSO")

# Limpiar los campos de entrada después del registro
campo_nombre.delete(0, tk.END)
password_entry.delete(0, tk.END)
    
def regresar():
    ventana_principal.destroy()
    os.system("python "+"login.py")

# Crear el botón de registro
tk.Button(boton_registro, text="Registrarse", command=registro).grid(row=4, column=1)
tk.Button(boton_cerrar, text="Regresar", command=regresar).grid(row=4, column=1)

# Mostrar la ventana principal
centrar_ventana(ventana_principal)
ventana_principal.mainloop()

