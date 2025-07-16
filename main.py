import pygame
from config import W, H, KMEANS_K, DBSCAN_EPS, DBSCAN_MIN_PTS
from core.utils import redraw, make_bunch
from core.kmeans import my_kmeans
from core.dbscan import my_dbscan

pygame.init()
win = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("Кластеризация: KMeans и DBSCAN")

dots = []
running = True

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        elif e.type == pygame.VIDEORESIZE:
            W, H = e.w, e.h
            win = pygame.display.set_mode((W, H), pygame.RESIZABLE)
            redraw(win, dots)

        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                make_bunch(dots, e.pos[0], e.pos[1])
                redraw(win, dots)

        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_k and dots:
                my_kmeans(dots, KMEANS_K, H)
                redraw(win, dots)
            elif e.key == pygame.K_d and dots:
                my_dbscan(dots, DBSCAN_EPS, DBSCAN_MIN_PTS, H)
                redraw(win, dots)

pygame.quit()
