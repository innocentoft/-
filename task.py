# Написати Python-скрипт, який розпізнає обличчя людей на довільних цифрових
# зображеннях. Цифрові зображення зчитуються з заданої директорії. Кожне
# розпізнане обличчя повинно бути збережено в окремому файлі у форматі jpg.
# Для розпізнавання обличчя людей використовувати бібліотеку OpenCV.

import cv2 as cv

from pathlib import Path
from multiprocessing import Pool


DIR = Path(__file__).parent


def detect_face(img):
    classifier = cv.CascadeClassifier(
        f'{DIR}\haarcascade_frontalface_default.xml')

    current_image = cv.imread(str(img))
    gray_image = cv.cvtColor(current_image, cv.COLOR_BGR2GRAY)

    quantity_of_faces = classifier.detectMultiScale(
        gray_image, scaleFactor=1.5, minNeighbors=8)

    if len(quantity_of_faces) >= 1:
        filename = str(DIR.joinpath(f'output/{img.name}'))
        cv.imwrite(filename, current_image)


if __name__ == '__main__':
    for file in DIR.joinpath('output').iterdir():
        file.unlink()

    images_dir = DIR.joinpath('images')
    pool = Pool(len([i for i in images_dir.iterdir()]))

    for img in images_dir.iterdir():
        pool.apply_async(detect_face, (img,))

    pool.close()
    pool.join()