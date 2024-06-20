""" Tecnológico Nacional de México
  
  Instituto Tecnológico de Pachuca
  
  Ingeniería en Sistemas Computacionales

  Materia: Sistemas Programables
  Practica: Elevador con Interfaz Gráfica

  ALUMNOS:
  Bautista Arreola Esteban Misael
  Ibarra Hernández Héctor Napoleón 

  Version: Finalizada
  Comentarios: Este archivo tabla_ingreso es para
  mandar llamar la tabla de ingreso de la base de datos, de manera
  que se puede visualizar que operador inicio sesión a algun hora
  determinada.
    
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
ventana_principal.title("TABLA DE INGRESO")

# crear campo de búsqueda
titulo = tk.Label(ventana_principal, text="INICIO:")
titulo2 = tk.Label(ventana_principal, text="DIA Y HORA:")
titulo3 = tk.Label(ventana_principal, text="NOMBRE:")

titulo.pack()
search_box = Entry(ventana_principal)
search_box.pack()

titulo2.pack()
search_box_2 = Entry(ventana_principal)
search_box_2.pack()

titulo3.pack()
search_box_3 = Entry(ventana_principal)
search_box_3.pack()

# Función que realiza la consulta
def search_employee():
    query = "SELECT Inicio, Hora, Nombre FROM ingreso,operador WHERE Inicio LIKE '%{}%' AND Hora LIKE '%{}%' AND Nombre LIKE '%{}%' AND idOperador=Operador_idOperador;".format(search_box.get(),search_box_2.get(),search_box_3.get())
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
boton_busqueda = Button(ventana_principal, text="Buscar", command=search_employee)
boton_busqueda.pack()

# Crear tabla para mostrar resultados
tabla = Treeview(ventana_principal, columns=("Inicio", "Hora", "Nombre"))
tabla.pack()

# Agregar encabezados de columna
tabla.heading("Inicio", text="INICIO")
tabla.heading("Hora", text="DIA Y HORA")
tabla.heading("Nombre", text="OPERADOR")

# mostrar ventana_principal
centrar_ventana_principal(ventana_principal)
ventana_principal.mainloop()
