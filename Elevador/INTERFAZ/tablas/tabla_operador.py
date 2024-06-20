""" Tecnológico Nacional de México
  
  Instituto Tecnológico de Pachuca
  
  Ingeniería en Sistemas Computacionales

  Materia: Sistemas Programables
  Practica: Elevador con Interfaz Gráfica

  ALUMNOS:
  Bautista Arreola Esteban Misael
  Ibarra Hernández Héctor Napoleón 

  Version: Finalizada
  Comentarios: Este archivo tabla_operador es para ver quienes son los
  operadores registrado, con su contraseña de cada uno.
    
  25/Mayo/2023
"""
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="elevador"
)
# crear ventana_principal
ventana_principal = Tk()
ventana_principal.title("TABLA DE OPERADOR")

# crear campo de búsqueda
titulo = tk.Label(ventana_principal, text="NOMBRE:")
titulo2 = tk.Label(ventana_principal, text="CONTRASEÑA:")

titulo.pack()
search_box = Entry(ventana_principal)
search_box.pack()

titulo2.pack()
search_box_2 = Entry(ventana_principal)
search_box_2.pack()

# función que realiza la consulta
def buscar_empleado():
    query = "SELECT Nombre,Contrasena FROM operador WHERE Nombre LIKE '%{}%' AND Contrasena LIKE '%{}%';".format(search_box.get(),search_box_2.get())
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Eliminar filas anteriores
    for row in tabla.get_children():
        tabla.delete(row)
    
    # Agregar resultados a la tabla
    for result in results:
        tabla.insert("", END, values=result)

def centrar_ventana_principal(root):
    """Centra una ventana_principal de Tkinter en la pantalla."""
    root.update_idletasks()
    ancho = root.winfo_width()
    altura = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (ancho // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)
    root.geometry('{}x{}+{}+{}'.format(ancho, altura, x, y))

# Crear botón de búsqueda
boton_buscar = Button(ventana_principal, text="Buscar", command=buscar_empleado)
boton_buscar.pack()

# crear tabla para mostrar resultados
tabla = Treeview(ventana_principal, columns=("Nombre", "Contrasena"))
tabla.pack()

# agregar encabezados de columna
tabla.heading("Nombre", text="NOMBRE")
tabla.heading("Contrasena", text="CONTRASEÑA")

# mostrar ventana_principal
centrar_ventana_principal(ventana_principal)
ventana_principal.mainloop()
