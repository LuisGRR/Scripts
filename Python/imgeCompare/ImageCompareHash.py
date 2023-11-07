import cv2
import os
from multiprocessing import Pool
from tqdm import tqdm

def image_to_hash(image_path):
    # Abre la imagen
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Reduce el tamaño de la imagen
    img = cv2.resize(img, (8, 8), interpolation = cv2.INTER_AREA)
    # Calcular la diferencia entre los píxeles adyacentes
    difference = img[:, 1:] > img[:, :-1]
    # Calcular el valor del hash
    hash_Value = sum([2**i for i, value in enumerate(difference.flatten()) if value])
    return image_path, hash_Value

def compare_hashes(hashes):
    duplicates = []
    for i in range(len(hashes)):
        for j in range(i+1, len(hashes)):
            if hashes[i][1] == hashes[j][1]:
                duplicates.append((hashes[i][0], hashes[j][0]))
    return duplicates

if __name__ == "__main__":
    # Uso de la función
    image_dir = 'H:/ImgProyecto/'
    image_paths = [os.path.join(image_dir, filename) for filename in os.listdir(image_dir) if filename.endswith(('.jpeg','.jpg','.png'))]

    # Usa múltiples procesos para calcular los hashes de las imágenes
    with Pool() as p:
        hashes = list(tqdm(p.imap(image_to_hash, image_paths), total=len(image_paths)))

    # Compara los hashes
    duplicates = compare_hashes(hashes)

    # Imprime los duplicados
    for filename1, filename2 in duplicates:
        print(f"Las imágenes {filename1} y {filename2} son iguales.")
