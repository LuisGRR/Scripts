import tkinter as tk
import concurrent.futures
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from os import path
import ClasificasionArchivos as clasificasion


class AppMain:
    def __init__(self):

        self.ruta_carpeta = ""

        # Colores
        self.colorbg = "#31363F"
        self.details1 = "#222831"
        self.color = "#76ABAE"
        self.colorText = "#EEEEEE"

        # definion de ventana
        self.ventana = tk.Tk()
        self.ventana.title("Clasificasión de archivos")

        # Obtener las dimensiones de la pantalla
        ancho_pantalla = self.ventana.winfo_screenwidth()  # método para obtener Ancho
        alto_pantalla = self.ventana.winfo_screenheight()  # método para obtener Alto
        # Calcular las coordenadas para centrar la ventana
        ancho_ventana = 800
        alto_ventana = 600
        posicion_x = (ancho_pantalla - ancho_ventana) // 2
        posicion_y = (alto_pantalla - alto_ventana) // 2

        self.ventana.geometry(
            f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}"
        )
        self.ventana.config(background=self.details1)

        self.marco_head = tk.Frame(self.ventana, bg=self.details1)
        self.marco_head.pack(padx=5, pady=1)

        self.etiqueta = tk.Label(
            self.marco_head, text="Ingresa la ruta de la carpeta", font=("Arial", 15)
        )
        self.etiqueta.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.etiqueta.config(bg=self.details1, fg=self.colorText)

        # self.entry = tk.Entry(self.ventana)
        self.boton_entry = tk.Button(
            self.marco_head,
            text="Seleccionar carpeta",
            command=self.seleccionar_carpeta,
            justify="left",
            state="normal",
            bg=self.color,
            fg=self.colorText,
            height=1,
            width=15,
            activebackground=self.colorbg,
            activeforeground=self.colorText,
        )
        self.boton_entry.grid(
            row=0, column=1, padx=5, pady=5, sticky="nsew"
        )  # Cambia 'row=0' a 'row=1'
        # self.boton_entry.config()

        self.marco_paht = tk.Frame(self.ventana, bg=self.details1)
        self.marco_paht.pack(padx=5, pady=5, fill="x")

        # Crear una etiqueta para mostrar la ruta de la carpeta
        self.etiqueta_ruta = tk.Label(self.marco_paht, text="", font=("Arial", 10))
        self.etiqueta_ruta.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.etiqueta_ruta.config(bg=self.details1, fg=self.colorText)

        self.marco_body = tk.Frame(self.ventana, bg=self.colorbg)
        self.marco_body.pack(padx=5, pady=1, fill=tk.X, side=tk.TOP)

        self.boton = tk.Button(
            self.marco_body,
            text="Mover archivos",
            command=self.imprimir_contenido,
            bg=self.color,
            fg=self.colorText,
            height=1,
            width=15,
            activebackground=self.colorbg,
            activeforeground=self.colorText,
        )
        self.boton.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self.listExt = tk.Label(self.marco_body, bg=self.colorbg, fg=self.colorText)
        self.listExt.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.labelCreateDir = tk.Label(
            self.marco_body, bg=self.colorbg, fg=self.colorText
        )
        self.labelCreateDir.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.listExt = tk.Label(self.marco_body, bg=self.colorbg, fg=self.colorText)
        self.listExt.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.barra_progreso = ttk.Progressbar(
            self.marco_body, length=200, mode="determinate"
        )
        self.barra_progreso.grid(row=5, column=0, padx=5, pady=5)
        self.label_archivos = tk.Label(self.marco_body, text="Archivos movidos: 0")
        self.label_archivos.grid(row=5, column=1, padx=5, pady=5)

        self.marco_error = tk.Frame(self.ventana, bg=self.colorbg)
        self.marco_error.pack(padx=5, pady=1, fill=tk.X, side=tk.TOP)

        self.canvas = tk.Canvas(self.marco_error, bg=self.colorbg)
        self.canvas.pack(side="left", fill="both", expand=True)
        # Crea un scrollbar y lo añade al frame principal
        self.scrollbar = tk.Scrollbar(self.marco_error, command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Configura el canvas para que use el scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Crea un frame interno dentro del canvas
        self.frame_interno = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_interno, anchor="nw")

        self.ventana.mainloop()

    def seleccionar_carpeta(self):
        self.ruta_carpeta = filedialog.askdirectory()
        if self.ruta_carpeta:
            # Actualizar el texto de la etiqueta con la ruta de la carpeta
            self.etiqueta_ruta.config(
                text=f"Carpeta seleccionada: { self.ruta_carpeta}"
            )
        else:
            self.etiqueta_ruta.config(text="No se seleccionó ninguna carpeta.")

    def listExtenciones(self, contenido):
        extencion_STR = ""
        extenciones = clasificasion.extencionArchivo(contenido)
        if extenciones is not None:
            extencion_STR = "\n".join(extenciones)
        self.listExt.config(text=extencion_STR)

    def directorio(self, contenido):
        create_dir = clasificasion.crearCarpetasExtenciones(contenido)
        create_dir_str = "Ocurrio un error al crear las carpetas"
        if create_dir:
            create_dir_str = "Se han creado las carpetas con exito"
        self.labelCreateDir.config(text=create_dir_str)

    def numArchivos(self, contenido):
        numeroArchivos = clasificasion.buacarArchivos(contenido)
        if numeroArchivos is not None:
            self.listExt.config(text=f"Se moveran los {numeroArchivos} archivos ")

    def progresbasArchive(self, contenido):
        total_archivos = len(clasificasion.diccionarioArchivos)
        self.barra_progreso["maximum"] = total_archivos
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i, (extencion, name) in enumerate(clasificasion.diccionarioArchivos):
                executor.submit(
                    clasificasion.moverArchivosExtencion, contenido, extencion, name
                )
                self.barra_progreso["value"] = i + 1  # Suma 1 a i
                self.label_archivos["text"] = (
                    f"Archivos movidos: {i + 1} de {total_archivos}"
                )
                self.ventana.update()
        messagebox.showinfo(message="Se termino de mover los archivos")

    def error_almover_archivos(self):
        if not clasificasion.archivos_fallidos:
            return
        label_info_error = tk.Label(
            self.frame_interno, text="Archivos que presentaron errores al mover"
        )
        label_info_error.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        label_info_error.config(bg=self.colorbg, fg=self.colorText)
        archivos_fallidos_str = "\n".join(
            f"{ext}: {name}" for ext, name in clasificasion.archivos_fallidos
        )
        label_info_archivos_error = tk.Label(
            self.frame_interno, text=archivos_fallidos_str
        )
        label_info_archivos_error.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        label_info_archivos_error.config(bg=self.colorbg, fg=self.colorText)

    def imprimir_contenido(self):
        if not self.ruta_carpeta:
            messagebox.showerror("Error", "No se definio una ruta")
            return
        ruta = self.ruta_carpeta + "\\"
        if not path.exists(ruta):
            messagebox.showerror("Error", "El directorio no existe.")
            return
        self.listExtenciones(ruta)
        self.directorio(ruta)
        self.numArchivos(ruta)
        self.progresbasArchive(ruta)
        self.error_almover_archivos()


if __name__ == "__main__":
    app = AppMain()
