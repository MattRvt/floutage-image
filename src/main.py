import multiprocessing
import os
from copy import deepcopy
from multiprocessing import Queue

import imageio

from definitionIntensite.Intensite import Partie

if __name__ == '__main__':
    print("debut du programme")
    im = imageio.imread('chargementImage/tree.jpg', format='jpg')
    info = im.shape
    h = info[0]
    w = info[1]
    imIntensiteMoy = [[0 for j in range(w)] for i in range(h)]
    queue = Queue()
    # creation des parties de limages
    nombreProcess = multiprocessing.cpu_count()
    parties = []
    for i in range(nombreProcess):
        process = Partie(int(i * (h / nombreProcess)), int((i + 1) * (h / nombreProcess)), im, h, w, i, queue)
        parties.append(process)

    # demarage des thread
    for i in range(nombreProcess):
        parties[i].start()

    # lecture des donnes
    imIntensite = [[0] * len(im[1])] * len(im)  # le tableau a la meme taille que l'image d'origine

    imRecu = []
    for i in range(nombreProcess):
        queueGet = queue.get()
        imRecu = queueGet[0]
        numProcess = queueGet[1]
        imIntensite[int(numProcess * (h / nombreProcess)):int((numProcess + 1) * (h / nombreProcess))] \
            = (imRecu[int(numProcess * (h / nombreProcess)):int((numProcess + 1) * (h / nombreProcess))])

    # verification que les process se sont bien termine
    for i in range(nombreProcess):
        parties[i].join()

    # definit le code RGB de chaque pixel
    print("ecriture de l'image ")
    for y in range(h):
        for x in range(w):
            im[y][x][0] = imIntensite[y][x][0]
            im[y][x][1] = imIntensite[y][x][1]
            im[y][x][2] = imIntensite[y][x][2]
            """
            if imIntensite[y][x] > 100:
                im[y][x][0] = 0
                im[y][x][1] = 0
                im[y][x][2] = 0
            else:
                im[y][x][0] = 255
                im[y][x][1] = 255
                im[y][x][2] = 255
                        """
    imageio.imsave('chargementImage/france.png', im, format='png')
