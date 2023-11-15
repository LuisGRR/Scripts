import tkinter as tk

ventana = tk.Tk()

ventana.title("Clasificasión de archivos")

ventana.geometry("500x500")

etiqueta = tk.Label(ventana,text="Ingresa la ruta de la carpeta")
etiqueta.grid(row=0,column=0,sticky="w", padx=5,pady=5)


entry = tk.Entry(ventana)
entry.grid(row=0,column=1, padx=5,pady=5)
entry.config(justify="left",state="normal")

def imprimir_contenido():
    contenido = entry.get()
    if entry.get() != "" :
        etiquetaEntrada = tk.Label(ventana, text=contenido)
        etiquetaEntrada.grid(row=1, column=0, sticky="w", padx=5, pady=5)

boton = tk.Button(ventana, text="Imprimir contenido", command=imprimir_contenido)
boton.grid(row=2, column=0)

ventana.mainloop()