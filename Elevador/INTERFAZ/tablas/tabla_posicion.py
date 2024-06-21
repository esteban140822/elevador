""" Tecnológico Nacional de México
  
  Instituto Tecnológico de Pachuca
  
  Ingeniería en Sistemas Computacionales

  Materia: Sistemas Programables
  Practica: Elevador con Interfaz Gráfica

  ALUMNO:
  Bautista Arreola Esteban Misael

  Version: Finalizada
  Comentarios: Este archivo tabla_posicion es para observar todos 
  los movimientos del elevador guardados en la base de datos, 
  de manera que pueden ser visualizados de manera específica, 
  por el nombre del operador, la hora, el dia, etc.
    
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
ventana_principal.title("TABLA DE POSICIÓN")

# crear campo de búsqueda
titulo = tk.Label(ventana_principal, text="PISO:")
titulo2 = tk.Label(ventana_principal, text="HORA:")
titulo3 = tk.Label(ventana_principal, text="PUERTA:")
titulo4= tk.Label(ventana_principal, text="DISTANCIA:")
titulo5 = tk.Label(ventana_principal, text="NOMBRE:")
tituloHora1 = tk.Label(ventana_principal, text="DIA Y HORA:")
tituloEspacio= tk.Label(ventana_principal, text="ENTRE:")
tituloHora2= tk.Label(ventana_principal, text="DIA Y HORA:")

titulo.pack()
search_box = Entry(ventana_principal)
search_box.pack()

titulo2.pack()
search_box2 = Entry(ventana_principal)
search_box2.pack()

titulo3.pack()
search_box3 = Entry(ventana_principal)
search_box3.pack()

titulo4.pack()
search_box4 = Entry(ventana_principal)
search_box4.pack()

titulo5.pack()
search_box5 = Entry(ventana_principal)
search_box5.pack()

# Función que realiza la consulta
def buscar_empleado():
    query = "SELECT Piso, Hora, Puerta,Distancia,Nombre FROM posicion,operador WHERE Piso LIKE '%{}%' AND Hora LIKE '%{}%' AND Puerta LIKE '%{}%' AND Distancia LIKE '%{}%' AND Nombre LIKE '%{}%'AND idOperador=Operador_idOperador;".format(search_box.get(),search_box2.get(),search_box3.get(),search_box4.get(),search_box5.get(),"""hora_box.get(),hora2_box.get()""")
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

# Crear tabla para mostrar resultados
tabla = Treeview(ventana_principal, columns=("Piso", "Hora", "Puerta","Distancia","Nombre"))
tabla.pack()

# Agregar encabezados de columna
tabla.heading("Piso", text="PISO")
tabla.heading("Hora", text="HORA")
tabla.heading("Puerta", text="PUERTA")
tabla.heading("Distancia", text="DISTANCIA")
tabla.heading("Nombre", text="NOMBRE")

scrollbar = Scrollbar(ventana_principal, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scrollbar.set)

# ubicar la tabla y la barra de desplazamiento en la ventana_principal

# mostrar ventana_principal
centrar_ventana_principal(ventana_principal)
ventana_principal.mainloop()
