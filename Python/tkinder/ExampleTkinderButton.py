import tkinter as tk

def imprimir_mensaje():
    print("¡Hola, mundo!")

# Crea una nueva ventana
ventana = tk.Tk()

# Crea un nuevo botón
boton = tk.Button(ventana, text="Haz clic en mí", command=imprimir_mensaje)

# Añade el botón a la ventana
boton.pack()

# Inicia el bucle principal de la ventana
ventana.mainloop()
