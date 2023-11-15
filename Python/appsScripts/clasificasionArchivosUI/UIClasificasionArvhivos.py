import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import ClasificasionArchivos as clasificasion

class AppMain:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Clasificasión de archivos")
        self.ventana.geometry("500x500")
        self.etiqueta = tk.Label(self.ventana,text="Ingresa la ruta de la carpeta")
        self.etiqueta.grid(row=0,column=0,sticky="w", padx=5,pady=5)
        self.entry = tk.Entry(self.ventana)
        self.entry.grid(row=0,column=1, padx=5,pady=5)
        self.entry.config(justify="left",state="normal")
        self.boton = tk.Button(self.ventana, text="Mover archivos", command=self.imprimir_contenido)
        self.boton.grid(row=1, column=0)
        self.ventana.mainloop()

    def listExtenciones(self,contenido):
        extencion_STR = ""
        extenciones =  clasificasion.extencionArchivo(contenido)
        if extenciones is not None:
            extencion_STR = '\n'.join(extenciones)
        listExt = tk.Label(self.ventana,text=extencion_STR)
        listExt.grid(row=3,column=0, padx=5,pady=5)

    def directorio(self, contenido):
        create_dir = clasificasion.crearCarpetasExtenciones(contenido)
        create_dir_str = "Ocurrio un error al crear las carpetas"
        if create_dir:
            create_dir_str = "Se han creado las carpetas con exito"
        labelCreateDir = tk.Label(self.ventana,text=create_dir_str)
        labelCreateDir.grid(row=4,column=0, padx=5,pady=5)

    def numArchivos(self,contenido):
        numeroArchivos = clasificasion.buacarArchivos(contenido)
        if numeroArchivos is not None:
            listExt = tk.Label(self.ventana,text=f"Se moveran los {numeroArchivos} archivos " )
            listExt.grid(row=5,column=0, padx=5,pady=5)

    def progresbasArchive(self,contenido):
        barra_progreso = ttk.Progressbar(self.ventana, length=200, mode='determinate')
        barra_progreso.grid(row=6,column=0, padx=5,pady=5)
        barra_progreso['maximum'] = len(clasificasion.diccionarioArchivos)
        for i, (extencion, name) in enumerate( clasificasion.diccionarioArchivos):
            clasificasion.moverArchivosExtencion(contenido,extencion,name)
            barra_progreso['value'] = i
            self.ventana.update()

    def imprimir_contenido(self):
        if self.entry.get() != "" :
            contenido = self.entry.get()+"\\"
            if os.path.exists(contenido):
                etiquetaEntrada = tk.Label(self.ventana, text=contenido)
                etiquetaEntrada.grid(row=2, column=0, sticky="w", padx=5, pady=5)
                self.listExtenciones(contenido)
                self.directorio(contenido)
                self.numArchivos(contenido)
                self.progresbasArchive(contenido)
            else:
                messagebox.showerror("Error", "El directorio no existe.")

if __name__ == '__main__':
    app = AppMain()
