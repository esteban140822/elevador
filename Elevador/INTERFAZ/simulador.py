""" Tecnológico Nacional de México
  
  Instituto Tecnológico de Pachuca
  
  Ingeniería en Sistemas Computacionales

  Materia: Sistemas Programables
  Practica: Elevador con Interfaz Gráfica

  ALUMNOS:
  Bautista Arreola Esteban Misael
  Ibarra Hernández Héctor Napoleón 

  Version: Finalizada
  Comentarios: Este archivo simulador.py es para obtener valores especificos
  de la base de datos los cuales serviran para hacer una pequeña simulacion
  funcional de lo que hizo el elevador en el tiempo determinado.
  
  25/Mayo/2023
"""
from tkinter import *
from tkinter.ttk import *
import mysql.connector
from collections import deque
import tkinter as tk
import subprocess
import serial
arduino = serial.Serial('COM3', 9600)

# Conectarse a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="elevador"
)
cursor = db.cursor()

ventana_principal = Tk()
ventana_principal.geometry("512x588") 
ventana_principal.title("SIMULADOR DEL ELEVADOR")
ventana = tk.Tk()
ventana.title("SIMULADOR")

mensaje = Tk()
mensaje.geometry("512x150")
ventana.title("MENSAJE DE SIMULACIÓN")
lbTitulo_mensaje = tk.Label(mensaje,text = " ",
                 bg="black",fg="white",font=("Arial",14))
lbTitulo_mensaje.place(x=10, y=20)

text_widget = tk.Text(ventana)
text_widget.pack()
tituloHora1 = tk.Label(ventana, text="DIA Y HORA:")
tituloEspacio = tk.Label(ventana, text="ENTRE:")
tituloHora2 = tk.Label(ventana, text="DIA Y HORA:")

tituloHora1.pack()
campo_hora = Entry(ventana)
campo_hora.insert(0, "2023-00-00 00:00:00")
campo_hora.pack()

tituloEspacio.pack()  # ESPACIO

tituloHora2.pack()
campo_hora_2 = Entry(ventana)
campo_hora_2.insert(0, "2023-00-00 00:00:00")
campo_hora_2.pack()

valores = []  # Lista para guardar los valores


# Función que realiza la consulta en la base de datos de los datos ingresados por el admin
def buscar():
    text_widget.delete("1.0", "end")  # Borrar contenido existente en el widget Text
    valores.clear()  # Limpiar la lista de valores
    query = "SELECT Piso, Hora, Puerta, Distancia, Nombre FROM posicion, operador WHERE idOperador=Operador_idOperador and (Hora BETWEEN '{}'AND '{}');".format(
        campo_hora.get(), campo_hora_2.get()) # Obtener los datos de la tabla
    cursor.execute(query)
    result = cursor.fetchall()

    # Crear una cola para guardar los resultados
    resultados = deque()
    auxiliar = ""

    # Agregar los resultados a la cola
    for fila in result:
        resultados.append(fila[0])
    auxiliar
    valores
    for valor in resultados:
        if valor != auxiliar:
            auxiliar = valor
            valores.append(valor)  # Agregar valor a la lista
            titulo = (valor[:6])
            titulo_2 = (valor[:11])
            if (titulo_2 == "PLANTA BAJA"):
                text_widget.insert(tk.END, str(titulo_2) + "\n")
            if (titulo == "PISO 1"):
                text_widget.insert(tk.END, str(titulo) + "\n")
            if (titulo == "PISO 2"):
                text_widget.insert(tk.END, str(titulo) + "\n")
            if (titulo == "PISO 3"):
                text_widget.insert(tk.END, str(titulo) + "\n")
        else:
            auxiliar = valor
    text_widget.insert(tk.END, "--------------------" + "\n")


# Función que se ejecuta al presionar el botón
def imprimir_valor():
        lbTitulo_mensaje.config(text="SIMULACIÓN EN PROCESO",bg="green",fg="white")
        if len(valores) > 0:
            valor = valores.pop(0)  # Obtener el siguiente valor de la lista
            titulo = (valor[:6])
            titulo_2 = (valor[:11])
            if (titulo_2 == "PLANTA BAJA"):
                numero = 1
                print(numero)
                text_widget.insert(tk.END, str(titulo_2)+"  ✓" + "\n")
                arduino.write(b"1")
            if (titulo == "PISO 1"):
                numero = 2
                print(numero)
                text_widget.insert(tk.END, str(titulo)+"  ✓"  + "\n")
                arduino.write(b"2")
            if (titulo == "PISO 2"):
                numero = 3
                print(numero)
                text_widget.insert(tk.END, str(titulo) + "\n")
                arduino.write(b"3")
            if (titulo == "PISO 3"):
                numero = 4
                print(numero)
                text_widget.insert(tk.END, str(titulo) + "\n")
                arduino.write(b"4")
        else:
            lbTitulo_mensaje.config(text="SIMULACIÓN TERMINADA",bg="red",fg="white") 
            text_widget.insert(tk.END, "NO HAY MÁS VALORES." + "\n")

# Funcion para visualizar la tabla posicion por si se desea buscar algun registro
def ver_tabla():
    subprocess.Popen(["python", "tablas/tabla_posicion.py"])

# Funcion para cerrar las interfaces
def cerrarInterfaz():
    ventana.destroy()
    mensaje.destroy()
    ventana_principal.destroy()
    arduino.close() 

# Crear una ventana con un botón para imprimir los valores de la cola
boton_imprimir = tk.Button(ventana, text="SIMULAR", command=imprimir_valor)
boton_imprimir.place(x=400, y=20)

boton_buscar = tk.Button(ventana, text="BUSCAR", command=buscar)
boton_buscar.place(x=420, y=400)

boton_ver_tabla = tk.Button(ventana, text="VER TABLA", command=ver_tabla)
boton_ver_tabla.place(x=60, y=450)

boton_cerrar = tk.Button(ventana, text="CERRAR", command=cerrarInterfaz)
boton_cerrar.place(x=560, y=450)


def centrar_ventana(ventana_principal):
    """Centra una ventana de Tkinter en la pantalla."""
    ventana_principal.update_idletasks()
    ancho = ventana_principal.winfo_width()
    altura = ventana_principal.winfo_height()
    x = (ventana_principal.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana_principal.winfo_screenheight() // 2) - (altura // 2)
    ventana_principal.geometry('{}x{}+{}+{}'.format(ancho, altura, x, y))

# Funciones principales
def piso():
    if arduino.in_waiting > 0:
        # Depende el valor que mande arduino este obtendra valores especificos
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
        elif(titulo_2=="PLANTA BAJA"):
            nivel=(mensaje[:11])
            puerta=(mensaje[12:19])
            distancia=(mensaje[20:24])
            lbPiso.config(text=" "+titulo_2)
            lbPuerta.config(text="PUERTA "+puerta)
            lbDistancia.config(text=" "+distancia)
        elif(titulo_3=="DETENIDO"):
            nivel=(mensaje[:8])
            puerta=(mensaje[9:16])
            distancia=(mensaje[17:21])
            lbPiso.config(text=" "+titulo_3)
            lbPuerta.config(text="PUERTA "+puerta)
            lbDistancia.config(text=" "+distancia)
        elif(titulo_3=="CONTINUA"):
            nivel=(mensaje[:8])
            puerta=(mensaje[9:16])
            distancia=(mensaje[17:21])
            lbPiso.config(text=" "+titulo_3)
            lbPuerta.config(text="PUERTA "+puerta)
            lbDistancia.config(text=" "+distancia)  
        elif(titulo_3=="SUBIENDO"):
            nivel=(mensaje[:8])
            puerta=(mensaje[9:16])
            distancia=(mensaje[17:20])
            lbPiso.config(text=" "+titulo_3)
            lbPuerta.config(text="PUERTA "+puerta)
            lbDistancia.config(text=" "+distancia)
        elif(titulo_4=="BAJANDO"):
            nivel=(mensaje[:7])
            puerta=(mensaje[8:15])
            distancia=(mensaje[16:19])
            lbPiso.config(text=" "+titulo_4)
            lbPuerta.config(text="PUERTA "+puerta)
            lbDistancia.config(text=" "+distancia)
    ventana_principal.after(10,piso)

# Fondos
fondo_titulo = tk.Frame()
fondo_titulo.config(bg="black",width="512", height="88")
fondo_titulo.place(x=0, y=0)

fondo_botones=tk.Frame()
fondo_botones.config(bg="#3B83BD",width="512", height="500")
fondo_botones.place(x=0, y=80)

# Etiqueta con imagen.
image = tk.PhotoImage(file="img/elevator.png")
label = tk.Label(fondo_botones,image=image,width="512", height="512")
label.pack()

image_P = tk.PhotoImage(file="img/tapar.png")
lbboton = tk.Label(fondo_botones,image=image_P,width="90",height="200")
lbboton.place(x=380, y=180)

# Letreros
lbTitulo = tk.Label(fondo_titulo,text = "BIENVENIDO ADMIN",
                 bg="black",fg="white",font=("Arial",16))
lbTitulo.place(x=150, y=20)

lbPiso = tk.Label(fondo_botones,text = " ",
                 bg="black",fg="white",font=("Arial",15))
lbPiso.place(x=150, y=40)

lbPuerta = tk.Label(fondo_botones,text = "PUERTA ",
                 bg="black",fg="white",font=("Arial",15))
lbPuerta.place(x=130, y=470)

lbDistancia = tk.Label(fondo_botones,text = " ",
                 bg="black",fg="white",font=("Arial",12))
lbDistancia.place(x=330, y=42)

piso()

# Mostrar la ventana principal
centrar_ventana(ventana)
ventana.mainloop()