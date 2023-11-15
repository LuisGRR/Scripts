import errno
import os
import shutil
import logging

dirExtenciones = set()
diccionarioArchivos = []

#configuracion de loggion
logging.basicConfig(filename="ClasificasionArchivos.log",level=logging.INFO)

#funciones del programa

def extencionArchivo(dirCarpeta):
    for fichero in os.scandir(dirCarpeta):
        if fichero.is_file():
            _, extencion = os.path.splitext(fichero.name)
            if extencion:  # Ignora los archivos sin extensión
                dirExtenciones.add(extencion)
    return dirExtenciones

def buacarArchivos(dirCarpeta):
    for extencion in dirExtenciones:
        buscarArchivoExtencion(extencion, dirCarpeta)
    return len(diccionarioArchivos)

def buscarArchivoExtencion(extencion, dirCarpeta):
     for fichero in os.scandir(dirCarpeta):
        if fichero.is_file() and fichero.name.endswith(extencion):
            diccionarioArchivos.append((extencion, fichero.name))

def crearCarpetasExtenciones(dirCarpeta):
    try:
        crearCarpetaRaiz(dirCarpeta)
        for ext in dirExtenciones:
            os.mkdir(dirCarpeta+'Clasificasion-archivos/Archivos-'+ext)
        return True
    except OSError as e:
        if e.errno != errno.EEXIST:
            logging.error("Error: %s", e)
            return False

def crearCarpetaRaiz(dirCarpeta):
    try:
        os.mkdir(dirCarpeta+'Clasificasion-archivos')
    except OSError as e:
          if e.errno != errno.EEXIST:
            logging.error("Error: %s",e)
            raise

def moverArchivosExtencion(dirCarpeta,extencion,name):
    try:
        destino = os.path.join(dirCarpeta, 'Clasificasion-archivos', 'Archivos-'+extencion, name)
        shutil.move(os.path.join(dirCarpeta, name), destino)
    except (FileNotFoundError, OSError) as err:
        logging.error("Error: %s",err)
