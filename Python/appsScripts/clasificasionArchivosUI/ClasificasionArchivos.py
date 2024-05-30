import errno
import os
import shutil
import logging

dirExtenciones = set()
diccionarioArchivos = []
archivos_fallidos = []

# configuracion de loggion
logging.basicConfig(filename="ClasificasionArchivos.log", level=logging.INFO)


# funciones del programa
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
            os.makedirs(
                f"{dirCarpeta}Clasificasion-archivos/Archivos-{ext}", exist_ok=True
            )
        return True
    except FileExistsError as e:
        logging.error(f"Error: {e}")
        return False
    except Exception as err:
        logging.error(f"Error: {err}")


def crearCarpetaRaiz(dirCarpeta):
    try:
        os.makedirs(f"{dirCarpeta}Clasificasion-archivos", exist_ok=True)
    except FileExistsError as e:
        if e.errno != errno.EEXIST:
            logging.error(f"Error: {e}")
            raise
    except Exception as err:
        logging.error(f"Error: {err}")


def moverArchivosExtencion(dirCarpeta, extencion, name):
    try:
        destino = os.path.join(
            dirCarpeta, "Clasificasion-archivos", f"Archivos-{extencion}", name
        )
        shutil.move(os.path.join(dirCarpeta, name), destino)
        diccionarioArchivos.remove((extencion, name))
    except FileNotFoundError as err:
        logging.error(f"Archivo no encontrado: {err}")
        archivos_fallidos.append((extencion, name))
    except PermissionError as err:
        logging.error(f"Error de permiso: {err}")
        archivos_fallidos.append((extencion, name))
    except Exception as err:
        logging.error(f"Error: {err}")
        archivos_fallidos.append((extencion, name))
