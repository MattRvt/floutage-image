import time
from concurrent.futures import thread
from multiprocessing import Process


class Partie(Process):
    # """Thread chargé simplement d'afficher un mot dans la console."""

    def __init__(self, minY, maxY, im, h, w, numeroDeProcessus, queue):
        Process.__init__(self)
        self.queue = queue
        self.minY = minY
        self.maxY = maxY
        self.im = im
        self.h = h
        self.w = w
        self.i = numeroDeProcessus
        self.imIntensite = [[0 for j in range(w)] for i in range(h)]

    def run(self):
        for y in range(self.minY, self.maxY):
            for x in range(self.w):

                # pour chaque pixel
                rayonVoisinageStatic = 10
                sommeR = 0
                sommeG = 0
                sommeB = 0
                n = 0


                #pixel du millieu
                sommeR += self.im[y][x][0]
                sommeG += self.im[y][x][1]
                sommeB += self.im[y][x][2]
                n = n + 1
                for rayonVoisinage in range(0, rayonVoisinageStatic + 1):
                    # si on atteint le pas bord en haut de l'immage
                    if (y - rayonVoisinage >= 0):
                        # px du haut
                        sommeR += self.im[y - rayonVoisinage][x][0]
                        sommeG += self.im[y - rayonVoisinage][x][1]
                        sommeB += self.im[y - rayonVoisinage][x][2]
                        n = n + 1

                        # px haut gauche
                        if (x - rayonVoisinageStatic >= 0):
                            for xTemp in range(x - rayonVoisinageStatic, x + 1):
                                sommeR += self.im[y - rayonVoisinage][xTemp][0]
                                sommeG += self.im[y - rayonVoisinage][xTemp][1]
                                sommeB += self.im[y - rayonVoisinage][xTemp][2]
                                n = n + 1

                        # px haut droit
                        if (x + rayonVoisinageStatic < self.w):
                            for xTemp in range(x + 1, x + rayonVoisinageStatic + 1):
                                sommeR += self.im[y - rayonVoisinage][xTemp][0]
                                sommeG += self.im[y - rayonVoisinage][xTemp][1]
                                sommeB += self.im[y - rayonVoisinage][xTemp][2]
                                n = n + 1

                    #   si on atteint pas la limite bas de l'image
                    if (y + rayonVoisinage < self.h):
                        # px du bas
                        sommeR += self.im[y + rayonVoisinage][x][0]
                        sommeG += self.im[y + rayonVoisinage][x][1]
                        sommeB += self.im[y + rayonVoisinage][x][2]
                        n = n + 1

                        # px haut gauche
                        if (x - rayonVoisinage >= 0):
                            for xTemp in range(x - rayonVoisinage, x + 1):
                                sommeR += self.im[y + rayonVoisinage][xTemp][0]
                                sommeG += self.im[y + rayonVoisinage][xTemp][1]
                                sommeB += self.im[y + rayonVoisinage][xTemp][2]
                                n = n + 1

                        # px bas droit
                        if (x + rayonVoisinageStatic < self.w):
                            for xTemp in range(x + 1, x + rayonVoisinageStatic + 1):
                                sommeR += self.im[y + rayonVoisinage][xTemp][0]
                                sommeG += self.im[y + rayonVoisinage][xTemp][1]
                                sommeB += self.im[y + rayonVoisinage][xTemp][2]
                                n = n + 1

                    # pixel a gauche
                    if (x - rayonVoisinage >= 0):
                        # px du haut
                        sommeR += self.im[y][x - rayonVoisinage][0]
                        sommeG += self.im[y][x - rayonVoisinage][1]
                        sommeB += self.im[y][x - rayonVoisinage][2]
                        n = n + 1
                        #   si on atteint pas la limite bas de l'image
                    if (x + rayonVoisinage < self.w):
                        # px du bas
                        sommeR += self.im[y][x + rayonVoisinage][0]
                        sommeG += self.im[y][x + rayonVoisinage][1]
                        sommeB += self.im[y][x + rayonVoisinage][2]
                        n = n + 1

                r = sommeR / n
                g = sommeG / n
                b = sommeB / n
                self.imIntensite[y][x] = [r,g,b]

        print("thread: ", self.i, " termine")
        rep = [0, 0]
        rep[0] = self.imIntensite
        rep[1] = self.i
        self.queue.put(rep)
