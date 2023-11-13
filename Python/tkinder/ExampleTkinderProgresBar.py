import tkinter as tk
from tkinter import ttk
import time
# Crea una nueva ventana principal
ventana = tk.Tk()

# Cambia el nombre de la ventana
ventana.title("Mi Aplicación")

# Especifica las dimensiones de la ventana
ventana.geometry("300x200")

# Crea una nueva barra de progreso
barra_progreso = ttk.Progressbar(ventana, orient='horizontal', length=200, mode='determinate')

# Coloca la barra de progreso en la ventana
barra_progreso.pack()

def actualizar_barra():
    for i in range(100):
        # Actualiza la barra de progreso en cada iteración
        barra_progreso['value'] = i
        ventana.update_idletasks()
        time.sleep(0.1)

# Crea un botón que actualiza la barra de progreso cuando se hace clic en él
boton = tk.Button(ventana, text="Iniciar", command=actualizar_barra)
boton.pack()

# Inicia el bucle principal de la ventana
ventana.mainloop()
