import errno
import os
import shutil

# class clasificasion:
dirCarpeta = input("Ingresar la ruta de los archivos: ") +'/'
dirExtenciones = []
diccionarioArchivos = []

def extencionArchivo(dirCarpeta):
    with os.scandir(dirCarpeta)as ficheros:
        for fichero in ficheros:
            if os.path.isfile(os.path.join(dirCarpeta, fichero)):
                nombre, extencion = os.path.splitext(fichero)
                validateExtancionsList(extencion)

def validateExtancionsList(extencion):
    if extencion not in dirExtenciones:
        print(extencion)
        dirExtenciones.append(extencion)

def buscarArchivoExtencion(extencion):
     with os.scandir(dirCarpeta) as ficheros:
        for fichero in ficheros:
            if os.path.isfile(os.path.join(dirCarpeta, fichero)) and fichero.name.endswith(extencion):
                print('Se econtro el archivo ->'+ fichero.name )
                diccionarioArchivos.append((extencion,fichero.name))

def buacarArchivos(listExtenciones):
    for extencion in listExtenciones:
        print('Se estan buscando los archivo con la extencion ->'+extencion)
        buscarArchivoExtencion(extencion)

def crearCarpetasExtenciones(nombreDir):
    try:
        crearCarpetaRaiz()
        for ext in nombreDir:
            print('Se esta creando la carpeta -> '+ext)
            os.mkdir(dirCarpeta+'/Clasificasion/Archivos-'+ext)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def crearCarpetaRaiz():
    try:
        os.mkdir(dirCarpeta+'/Clasificasion')
    except OSError as e:
          if e.errno != errno.EEXIST:
            raise

def moverArchivosExtencion(diccionarioArchivos):
     try:
        for archivo in diccionarioArchivos:
            extencion, name = archivo
            print('Se mueven los archivos a la carpeta -> Archivos-'+extencion)
            shutil.move(dirCarpeta+'/'+name,dirCarpeta+'/Clasificasion/Archivos-'+extencion+'-/')
     except FileNotFoundError as err:
         if err.errno != errno.EEXIST:
            raise

extencionArchivo(dirCarpeta)
crearCarpetasExtenciones(dirExtenciones)
buacarArchivos(dirExtenciones)
moverArchivosExtencion(diccionarioArchivos)