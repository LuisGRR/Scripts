import tkinter as tk

# Crea una nueva ventana principal
ventana = tk.Tk()

# Cambia el nombre de la ventana
ventana.title("Mi Aplicación")

# Especifica las dimensiones de la ventana
ventana.geometry("300x200")

# Crea una nueva etiqueta
etiqueta = tk.Label(ventana, text="¡Hola, mundo!")
etiqueta.pack()

# Crea un nuevo campo de entrada de texto
entrada = tk.Entry(ventana)
entrada.pack()

# Crea una nueva variable de instancia
texto = tk.StringVar()
texto.set("Escribe algo aquí...")

# Crea un nuevo campo de texto y lo llena con el valor de la variable de instancia
campo_texto = tk.Text(ventana)
campo_texto.insert(tk.END, texto.get())
campo_texto.pack()

# Crea una función para imprimir el contenido del campo de texto cuando se hace clic en el botón
def imprimir_contenido():
    print(campo_texto.get("1.0", tk.END))

# Crea un nuevo botón que llama a la función imprimir_contenido cuando se hace clic en él
boton = tk.Button(ventana, text="Imprimir contenido", command=imprimir_contenido)
boton.pack()

# Inicia el bucle principal de la ventana
ventana.mainloop()
