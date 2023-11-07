import errno
import os
import shutil

dirCarpeta = os.path.abspath(input("Ingresar la ruta de los archivos : ")) + os.sep
dirExtenciones = set()
diccionarioArchivos = []

def extencionArchivo(dirCarpeta):
    for fichero in os.scandir(dirCarpeta):
        if fichero.is_file():
            _, extencion = os.path.splitext(fichero.name)
            if extencion:  # Ignora los archivos sin extensión
                dirExtenciones.add(extencion)

def buscarArchivoExtencion(extencion):
     for fichero in os.scandir(dirCarpeta):
        if fichero.is_file() and fichero.name.endswith(extencion):
            print('Se encontró el archivo ->'+ fichero.name )
            diccionarioArchivos.append((extencion, fichero.name))

def buacarArchivos():
    for extencion in dirExtenciones:
        print('Se están buscando los archivos con la extensión ->'+extencion)
        buscarArchivoExtencion(extencion)

def crearCarpetasExtenciones():
    try:
        crearCarpetaRaiz()
        for ext in dirExtenciones:
            print('Se está creando la carpeta -> '+ext)
            os.mkdir(dirCarpeta+'Clasificasion-archivos/Archivos-'+ext)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def crearCarpetaRaiz():
    try:
        os.mkdir(dirCarpeta+'Clasificasion-archivos')
    except OSError as e:
          if e.errno != errno.EEXIST:
            raise

def moverArchivosExtencion():
     for extencion, name in diccionarioArchivos:
        try:
            print('Se mueven los archivos a la carpeta -> Archivos-'+extencion)
            destino = os.path.join(dirCarpeta, 'Clasificasion-archivos', 'Archivos-'+extencion, name)
            shutil.move(os.path.join(dirCarpeta, name), destino)
        except (FileNotFoundError, OSError) as err:
            print(f"No se pudo mover el archivo {name}. Error: {err}")

extencionArchivo(dirCarpeta)
crearCarpetasExtenciones()
buacarArchivos()
moverArchivosExtencion()
