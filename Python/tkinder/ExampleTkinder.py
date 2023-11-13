from tkinter import *

# Creamos una ventana de fondo
root = Tk()

# Creamos dos listas
li = ["Diego", "Matias", "Lorena", "Roberto", "Rosario"]
movie = ["El padrino", "Naruto", "La gran estafa", "Los juegos del hambre"]

# Creamos dos Listbox
listb = Listbox(root)
listb2 = Listbox(root)

# Insertamos los nombres en el primer Listbox
for item in li:
    listb.insert(0, item)

# Insertamos las películas en el segundo Listbox
for item in movie:
    listb2.insert(0, item)

# Hacemos el pack() de los dos Listbox
listb.pack()
listb2.pack()

# Corremos el loop
root.mainloop()
