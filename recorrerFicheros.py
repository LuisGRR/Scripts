__author__ = "Luis Gerardo Rivera Rivera"

import os
import numpy as  np

print("Introducir la ruta para recorrer ficheros")
dirCarpeta = input();

print(f"Se recorrea la ruta, {dirCarpeta}")

# Funcion para recorrer los arcivos, utiliznado recursividad para nevegar en subdirectorios
def recorrerFicheros(dirCarpeta,Separador=""):
    with os.scandir(dirCarpeta) as ficheros:
        for fichero in ficheros:
            if fichero.is_dir():
                print(Separador+'>accediendo a la carpeta -> ' +fichero.name)
                obtenerArchivos(dirCarpeta+'/'+fichero.name)
                recorrerFicheros(dirCarpeta+'/'+fichero.name,Separador=Separador+"|_-")

# Funcion para motrar los archivo que se encuntran dentro de las carpetas
def obtenerArchivos(dirCarpeta):
    with os.scandir(dirCarpeta) as ficheros:
        for fichero in ficheros:
            if os.path.isfile(os.path.join(dirCarpeta, fichero)):
                print('Archivo encontrado -> ' + fichero.name)

obtenerArchivos(dirCarpeta)
recorrerFicheros(dirCarpeta)