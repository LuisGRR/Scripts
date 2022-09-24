import numpy as  np
import errno
import shutil
import cv2
import os

#Comparacion de imagenes de la carpeta superficial
dirCarpeta = input("Ingresar la ruta de las imagenes: ") +'/'
#dirCarpeta = '/home/luisgerardo_rr/pythonProyect/scripts/'

def crearCarpetas(nombreDir):
    try:
        print('Se esta creando la carpeta -> '+nombreDir)
        os.mkdir(nombreDir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

crearCarpetas(dirCarpeta+'imagenes-iguales')
crearCarpetas(dirCarpeta+'imagenes-unicas')

imagenes=[]
imgenesPivote = []

imagenesIguales = []
imagenesDiferentes = []

with os.scandir(dirCarpeta)as ficheros:
    for fichero in ficheros:
        if os.path.isfile(os.path.join(dirCarpeta, fichero)) and fichero.name.endswith('.jpeg'):
            imagenes.append(fichero.name)
            imgenesPivote.append(fichero.name)
  

def moverImagenes(arrayImg, phatImagen):
    print('Se mueven los archivos a la carpeta -> '+phatImagen)
    for imagen in arrayImg:
        shutil.move(dirCarpeta+imagen, phatImagen+'/'+imagen)

def guardarImagenesUnicas(pivote):
    if pivote not in imagenesDiferentes:
        imagenesDiferentes.append(pivote)

#Funcion para compara imagenes enbase la deteccion de caracterisricas y la conincidencia de caracteristicas
def comparaDeteccionCoincidencia(pivote, comparar):
    shift = cv2.xfeatures2d.SIFT_create()
    kp_1, desc_1 = shift.detectAndCompute(pivote, None)
    kp_2, desc_2 = shift.detectAndCompute(comparar, None)
    print("Keypoints 1st image", str(len(kp_1)))
    print("Keypoints 2st image", str(len(kp_2)))

    index_params = dict(algorithm=0, trees=5)
    search_params = dict()

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(desc_1, desc_2, k=2)

    good_points = []
    for m, n in matches:
        if m.distance < 0.6*n.distance:
            good_points.append(m)

    number_keypoints = 0
    if (len(kp_1) <= len(kp_2)):
        number_keypoints = len(kp_1)
    else:
        number_keypoints = len(kp_2)
    
    print("GOOD matches",len(good_points))
    print("Que tan bueno es el match", len(good_points) / number_keypoints * 100, "%")

    result = cv2.drawMatches(pivote, kp_1, comparar, kp_2, good_points, None)
    cv2.imshow("Result", cv2.resize(result, None, fx = 0.4, fy=0.4))
    cv2.imwrite("Feature_matching.jpg", result)

    cv2.imshow("Original", pivote)
    cv2.imshow("Duplicate", comparar)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#Compara si la imagen es la misma
def comparaImg(pivote, imgCompare):
    imgPivote = cv2.imread(dirCarpeta+pivote)
    imgC =  cv2.imread(dirCarpeta+imgCompare)
    if pivote!=imgCompare:
        if imgPivote.shape == imgC.shape:
            diferencia = cv2.subtract(imgPivote, imgC)
            b, g, r = cv2.split(diferencia)
            if(cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r)== 0):
                print('La imagen -> '+pivote+' es igual a -> '+imgCompare)
                imagenesIguales.append(imgCompare)
            else:
                     #   print('La imagen -> '+pivote+'es diferente de -> '+imgCompare+' se movera a la carpeta imagens unicas')
                guardarImagenesUnicas(pivote);
        else:
                    #print('La imagen -> '+pivote+' es diferente a -> '+imgCompare)
            guardarImagenesUnicas(pivote)


for pivote in imgenesPivote:
    print('---------------------------------------------')
    print('Se esta comparando la imgen -> '+pivote)
    if pivote not in imagenesIguales:
        for imgCompare in imagenes:
            comparaImg(pivote,imgCompare)

print('Las imagenes que se moveran son -> ')
print(imagenesIguales)

moverImagenes(imagenesIguales,dirCarpeta+'imagenes-iguales')

moverImagenes(imagenesDiferentes,dirCarpeta+'imagenes-unicas')
