import os
import shutil
import errno

class OrganizadorArchivos:
    def __init__(self, dir_carpeta):
        self.dir_carpeta = dir_carpeta
        self.dir_extenciones = []
        self.diccionario_archivos = []

    def extencion_archivo(self):
        with os.scandir(self.dir_carpeta) as ficheros:
            for fichero in ficheros:
                if os.path.isfile(os.path.join(self.dir_carpeta, fichero)):
                    nombre, extencion = os.path.splitext(fichero)
                    self.validate_extencions_list(extencion)

    def validate_extencions_list(self, extencion):
        if extencion not in self.dir_extenciones:
            print(extencion)
            self.dir_extenciones.append(extencion)

    def buscar_archivo_extencion(self, extencion):
        with os.scandir(self.dir_carpeta) as ficheros:
            for fichero in ficheros:
                if os.path.isfile(os.path.join(self.dir_carpeta, fichero)) and fichero.name.endswith(extencion):
                    print('Se econtro el archivo ->' + fichero.name)
                    self.diccionario_archivos.append((extencion, fichero.name))

    def buscar_archivos(self, list_extenciones):
        for extencion in list_extenciones:
            print('Se estan buscando los archivos con la extencion ->' + extencion)
            self.buscar_archivo_extencion(extencion)

    def crear_carpetas_extenciones(self, nombre_dir):
        try:
            self.crear_carpeta_raiz()
            for ext in nombre_dir:
                print('Se esta creando la carpeta -> ' + ext)
                os.mkdir(self.dir_carpeta + '/Clasificasion/Archivos-' + ext)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def crear_carpeta_raiz(self):
        try:
            os.mkdir(self.dir_carpeta + '/Clasificasion')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def mover_archivos_extencion(self):
        try:
            for archivo in self.diccionario_archivos:
                extencion, name = archivo
                print('Se mueven los archivos a la carpeta -> Archivos-' + extencion)
                shutil.move(self.dir_carpeta + '/' + name, self.dir_carpeta + '/Clasificasion/Archivos-' + extencion + '/')
        except FileNotFoundError as err:
            if err.errno != errno.EEXIST:
                raise

# Uso de la clase OrganizadorArchivos
if __name__ == "__main__":
    dir_carpeta = input("Ingresar la ruta de las imagenes: ") + '/'
    organizador = OrganizadorArchivos(dir_carpeta)
    organizador.extencion_archivo()
    list_extenciones = organizador.dir_extenciones
    organizador.buscar_archivos(list_extenciones)
    organizador.crear_carpetas_extenciones(list_extenciones)
    organizador.mover_archivos_extencion()
