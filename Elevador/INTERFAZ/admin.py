"""
Tecnológico Nacional de México

Instituto Tecnológico de Pachuca

Ingeniería en Sistemas Computacionales

Materia: Sistemas Programables
Practica: Elevador con Interfaz Gráfica

ALUMNO:
Bautista Arreola Esteban Misael

Versión: Finalizada
Comentarios: Este archivo admin.py es únicamente ejecutado cuando el administrador
se hace login. Este tiene varias opciones para visualizar la base de datos, como 
sus operadores, en qué piso estuvo el elevador, inicios de sesión de operadores, etc.

25/Mayo/2023
"""
from tkinter import *
import subprocess
import os

# Creamos una función para que los botones hagan algo al ser presionados
def boton_operador_presionado():
    print("Botón 1 presionado")
    subprocess.Popen("python tablas/tabla_operador.py")

def boton_ingreso_presionado():
    print("Botón 2 presionado")
    subprocess.Popen("python tablas/tabla_ingreso.py")

def boton_posicion_presionado():
    print("Botón 3 presionado")
    subprocess.Popen(["python", "tablas/tabla_posicion.py"])

def boton_simulador_presionado():
    print("Botón 4 presionado")
    subprocess.Popen(["python", "simulador.py"])

def regresar():
    ventana_principal.destroy()
    os.system("python login.py")

def centrar_ventana(ventana):
    """Centra una ventana de Tkinter en la pantalla."""
    ventana.update_idletasks()
    ancho = ventana.winfo_width()
    altura = ventana.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (altura // 2)
    ventana.geometry('{}x{}+{}+{}'.format(ancho, altura, x, y))

# Creamos la ventana principal
ventana_principal = Tk()

# Definimos el tamaño de la ventana
ventana_principal.geometry("300x450")

# Definimos el título de la ventana
ventana_principal.title("ADMINISTRADOR")

# Creamos los botones
boton_operador = Button(ventana_principal, text="TABLA OPERADOR", command=boton_operador_presionado, bg="#841A1B", fg="white")
boton_ingreso = Button(ventana_principal, text="TABLA SESIÓN", command=boton_ingreso_presionado, bg="#3F744F", fg="white")
boton_posicion = Button(ventana_principal, text="TABLA POSICIÓN", command=boton_posicion_presionado, bg="#3E5F8A", fg="white")
boton_simulador = Button(ventana_principal, text="SIMULADOR", command=boton_simulador_presionado, bg="#B78700", fg="white")
boton_regresar = Button(ventana_principal, text="SALIR", command=regresar, bg="black", fg="white")

# Acomodamos los botones en la ventana
boton_operador.pack(pady=20)
boton_ingreso.pack(pady=20)
boton_posicion.pack(pady=20)
boton_simulador.pack(pady=20)
boton_regresar.pack(pady=60)

# Iniciamos el loop principal de la ventana
centrar_ventana(ventana_principal)
ventana_principal.mainloop()
