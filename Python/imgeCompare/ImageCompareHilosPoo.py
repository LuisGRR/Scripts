import os
import errno
import shutil
import cv2
import threading
from itertools import islice 
from datetime import datetime

class ImageOrganizer:
    def __init__(self, dir_carpeta):
        self.dir_carpeta = dir_carpeta
        self.nombre_carpeta_iguales = 'imagenes-iguales'
        self.nombre_carpeta_unicos = 'imagenes-unicas'
        self.diccionario_pivote = {}
        self.diccionario_comparar = {}
        self.diccionario_imagenes_iguales = {}
        self.diccionario_imagenes_diferentes = {}

    def mover_imagenes(self, dict_img, phat_imagen):
        try:
            print('Se mueven los archivos a la carpeta -> ' + phat_imagen)
            for k, v in dict_img.items():
                print('la ' + k + ' en la direccion ' + v + ' se movera a ' + phat_imagen)
                shutil.move(v + k, phat_imagen + '/' + k)
        except FileNotFoundError as err:
            if err.errno != errno.EEXIST:
                raise

    def crear_carpetas(self, nombre_dir):
        try:
            print('Se esta creando la carpeta -> ' + nombre_dir)
            os.mkdir(nombre_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    def renombrar_imagen(self, img, phat_imagen):
        try:
            date_actual = datetime.now()
            imagen_nueva = f"{date_actual.hour}_{date_actual.minute}_{date_actual.microsecond}__{img}"
            os.rename(phat_imagen + '/' + img, phat_imagen + '/' + imagen_nueva)
            return imagen_nueva
        except FileNotFoundError as err:
            if err.errno != errno.EEXIST:
                raise

    def recorrer_ficheros(self, dir_carpeta, separador=""):
        with os.scandir(dir_carpeta) as ficheros:
            for fichero in ficheros:
                if fichero.is_dir() and fichero.name != self.nombre_carpeta_iguales and fichero.name != self.nombre_carpeta_unicos:
                    print(separador + '>accediendo a la carpeta ->' + fichero.name)
                    self.obtener_archivos(dir_carpeta + '/' + fichero.name)
                    self.recorrer_ficheros(dir_carpeta + '/' + fichero.name, separador=separador + "|_-")

    def obtener_archivos(self, dir_carpeta):
        with os.scandir(dir_carpeta) as ficheros:
            for fichero in ficheros:
                if os.path.isfile(os.path.join(dir_carpeta, fichero)) and fichero.name.endswith(('.jpeg', '.jpg', '.png')):
                    print('Imagen encontrada ->' + fichero.name)
                    if fichero.name not in self.diccionario_pivote:
                        self.diccionario_pivote[fichero.name] = dir_carpeta + '/'
                        self.diccionario_comparar[fichero.name] = dir_carpeta + '/'
                    else:
                        print(' ')
                        print('Esta imagen ya se encontro en otra carpeta con el mismo nombre se procedera a cambiar el nombre')
                        print(fichero.name + '-------' + dir_carpeta)
                        nuevo_nombre = self.renombrar_imagen(fichero.name, dir_carpeta)
                        self.diccionario_pivote[nuevo_nombre] = dir_carpeta + '/'
                        self.diccionario_comparar[nuevo_nombre] = dir_carpeta + '/'
                        nuevo_nombre = ''

    def guardar_imagenes_unicas(self, pivote_k, pivote_v):
        if pivote_k not in self.diccionario_imagenes_diferentes:
            self.diccionario_imagenes_diferentes[pivote_k] = pivote_v

    def compara_img(self, pivote_k, pivote_v, img_compare_k, img_compare_v):
        img_pivote = cv2.imread(pivote_v + pivote_k)
        img_c = cv2.imread(img_compare_v + img_compare_k)
        if pivote_k != img_compare_k:
            if img_pivote.shape == img_c.shape:
                diferencia = cv2.subtract(img_pivote, img_c)
                b, g, r = cv2.split(diferencia)
                if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                    print('La imagen -> ' + pivote_k + ' es igual a -> ' + img_compare_k)
                    self.diccionario_imagenes_iguales[img_compare_k] = img_compare_v
                else:
                    self.guardar_imagenes_unicas(pivote_k, pivote_v)
            else:
                self.guardar_imagenes_unicas(pivote_k, pivote_v)

    def comparar_imagenes_hilos(self, diccionario_pivote):
        for pivote_k, pivote_v in diccionario_pivote.items():
            if pivote_k not in self.diccionario_imagenes_iguales:
                print('-------------------' + threading.current_thread().name + '--------------------------')
                print('Se esta comparando la imagen -> ' + pivote_k)
                for img_compare_k, img_compare_v in self.diccionario_comparar.items():
                    self.compara_img(pivote_k, pivote_v, img_compare_k, img_compare_v)
                print('---------------------------------------------')

    def crear_mover(self):
        if len(self.diccionario_imagenes_iguales) >= 1:
            self.crear_carpetas(self.dir_carpeta + '/' + self.nombre_carpeta_iguales)
            self.mover_imagenes(self.diccionario_imagenes_iguales, self.dir_carpeta + '/' + self.nombre_carpeta_iguales)
        if len(self.diccionario_imagenes_diferentes) >= 1:
            self.crear_carpetas(self.dir_carpeta + '/' + self.nombre_carpeta_unicos)
            self.mover_imagenes(self.diccionario_imagenes_diferentes, self.dir_carpeta + '/' + self.nombre_carpeta_unicos)

if __name__ == "__main__":
    dir_carpeta = input("Ingresar la ruta de las imagenes: ") + '/'
    organizer = ImageOrganizer(dir_carpeta)
    organizer.obtener_archivos(dir_carpeta)
    organizer.recorrer_ficheros(dir_carpeta)

    # Particion de Diccionario pivote
    inc_pv = iter(organizer.diccionario_pivote.items())
    res1_pv = dict(islice(inc_pv, len(organizer.diccionario_pivote) // 2))
    res2_pv = dict(inc_pv)

    inc1_pv = iter(res1_pv.items())
    res11 = dict(islice(inc1_pv, len(res1_pv) // 2))
    res12 = dict(inc1_pv)

    inc2_pv = iter(res2_pv.items())
    res21 = dict(islice(inc2_pv, len(res2_pv) // 2))
    res22 = dict(inc2_pv)

    # Creacion de hilos para comparar las imagenes
    hilo1 = threading.Thread(name='hilo1', target=organizer.comparar_imagenes_hilos, args=(res11,))
    hilo2 = threading.Thread(name='hilo2', target=organizer.comparar_imagenes_hilos, args=(res12,))
    hilo3 = threading.Thread(name='hilo3', target=organizer.comparar_imagenes_hilos, args=(res21,))
    hilo4 = threading.Thread(name='hilo4', target=organizer.comparar_imagenes_hilos, args=(res22,))

    hilo1.start()
    hilo2.start()
    hilo3.start()
    hilo4.start()

    hilo1.join()
    hilo2.join()
    hilo3.join()
    hilo4.join()

    # Crea las carpetas para mover las imagenes
    organizer.crear_mover()
