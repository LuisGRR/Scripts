__author__ = "Luis Gerardo Rivera Rivera"
#Se redijo el tiempo de comparacion, pero se incremento el conumo de recuro al momento de compara si se tiene muchas imagenes

# from ast import arg
from itertools import islice 
import threading
# import time
import os
import errno
import shutil
import cv2
# import numpy as  np
import datetime

dirCarpeta = input("Ingresar la ruta de las imagenes: ") +'/'

nombreCarpetaIguales = 'imagenes-iguales'
nombreCarpetaUnicos ='imagenes-unicas'

diccionarioPivote = dict()
diccionarioComparar = dict()

diccionarioImagenesIguales = dict()
diccionarioImagenesDiferentes = dict()

def moverImagenes(dictIMG, phatImagen):
    try:
        print('Se mueven los archivos a la carpeta -> '+phatImagen)
        for k,v in dictIMG.items():
            print('la '+k+' en la direcion '+v+' se movera a '+ phatImagen)
            shutil.move(v+k, phatImagen+'/'+k)
    except FileNotFoundError as err:
        if err.errno != errno.EEXIST:
            raise

def crearCarpetas(nombreDir):
    try:
        print('Se esta creando la carpeta -> '+nombreDir)
        os.mkdir(nombreDir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def renombrarImagen(img, phatImagen):
    try:
        dateActual = datetime.datetime.now()
        imagenNueva = str(dateActual.hour)+'_'+str(dateActual.minute)+'_'+str(dateActual.now().microsecond)+'__'+img
        os.rename(phatImagen+'/'+img, phatImagen+'/'+imagenNueva)
        return imagenNueva
    except FileNotFoundError as err:
        if err.errno != errno.EEXIST:
            raise

def recorrerFicheros(dirCarpeta,Separador=""):
    with os.scandir(dirCarpeta) as ficheros:
        for fichero in ficheros:
            if fichero.is_dir() and fichero.name != nombreCarpetaIguales and fichero.name != nombreCarpetaUnicos:
                print(Separador+'>accediendo a la carpeta ->' +fichero.name)
                obtenerArchivos(dirCarpeta+'/'+fichero.name)
                recorrerFicheros(dirCarpeta+'/'+fichero.name,Separador=Separador+"|_-")

def obtenerArchivos(dirCarpeta):
    with os.scandir(dirCarpeta) as ficheros:
        for fichero in ficheros:
            if os.path.isfile(os.path.join(dirCarpeta, fichero)) and fichero.name.endswith(('.jpeg','.jpg','.png')):
                print('Imgen encontrada ->' + fichero.name)
                if fichero.name not in diccionarioPivote:
                    diccionarioPivote[fichero.name]= dirCarpeta+'/'
                    diccionarioComparar[fichero.name]= dirCarpeta+'/'
                else:
                    print(' ')
                    print('Esta imagen ya se encontro en otra carpeta con el mismo nombre se procedera a cambiar el nombre')
                    print(fichero.name+'-------'+dirCarpeta)
                    nuevoNombre = renombrarImagen(fichero.name,dirCarpeta)
                    diccionarioPivote[nuevoNombre]= dirCarpeta+'/'
                    diccionarioComparar[nuevoNombre]= dirCarpeta+'/'
                    nuevoNombre = ''

def guardarImagenesUnicas(pivoteK,pivoteV):
    if pivoteK not in diccionarioImagenesDiferentes:
        diccionarioImagenesDiferentes[pivoteK] = pivoteV

#Compara si la imagen es la misma
def comparaImg(pivoteK,pivoteV, imgCompareK,imgCompareV):
    imgPivote = cv2.imread(pivoteV+pivoteK)
    imgC =  cv2.imread(imgCompareV+imgCompareK)
    if pivoteK != imgCompareK:
        if imgPivote.shape == imgC.shape:
            diferencia = cv2.subtract(imgPivote, imgC)
            b, g, r = cv2.split(diferencia)
            if(cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r)== 0):
                print('La imagen -> '+pivoteK+' es igual a -> '+imgCompareK)
                diccionarioImagenesIguales[imgCompareK] = imgCompareV
            else:
                guardarImagenesUnicas(pivoteK,pivoteV)
        else:
            guardarImagenesUnicas(pivoteK,pivoteV)

def CrearMover():
    if len(diccionarioImagenesIguales) >= 1:
       crearCarpetas(dirCarpeta+'/'+nombreCarpetaIguales) # type: ignore
       moverImagenes(diccionarioImagenesIguales,dirCarpeta+'/'+nombreCarpetaIguales)
    if len(diccionarioImagenesDiferentes) >= 1:
       crearCarpetas(dirCarpeta+'/'+nombreCarpetaUnicos)
       moverImagenes(diccionarioImagenesDiferentes,dirCarpeta+'/'+nombreCarpetaUnicos)

#Region donde se invocan las funciones
obtenerArchivos(dirCarpeta)
recorrerFicheros(dirCarpeta)

def comparaImgHilos(diccionarioPivote):
    for pivoteK,pivoteV in diccionarioPivote.items():
        if pivoteK not in diccionarioImagenesIguales:
            print('-------------------'+threading.current_thread().name+'--------------------------')
            print('Se esta comparando la imgen -> '+pivoteK)
            for imgCompareK,imgCompareV in diccionarioComparar.items():
                comparaImg(pivoteK,pivoteV, imgCompareK,imgCompareV)
            print('---------------------------------------------')

def divide_dict(data, n):
    it = iter(data)
    size = len(data) // n
    return [dict(islice(it, i, i + size)) for i in range(0, len(data), size)]

# Divide el diccionario en 4 partes
partes = divide_dict(diccionarioPivote, 4)

# Crea un hilo para cada parte
hilos = [threading.Thread(target=comparaImgHilos, args=(parte,)) for parte in partes]

# Inicia todos los hilos
for hilo in hilos:
    hilo.start()

# Espera a que todos los hilos terminen
for hilo in hilos:
    hilo.join()


#Crea la carpetas para mover las imagenes 
CrearMover()
