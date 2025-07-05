import pygame
import numpy as np
import random
from collections import deque

pygame.init()

W, H = 600, 400
win = pygame.display.set_mode((W, H), pygame.RESIZABLE)
dots = []
R = 4
running = True

colors = ["red", "blue", "green", "purple", "orange", "cyan", "magenta", "brown", "gray", "pink"]

def redraw():
    win.fill("white")
    for d in dots:
        
        pygame.draw.circle(win, d[2], (d[0], d[1]), R)
    pygame.display.flip()

def make_bunch(x, y, n=10, rad=10):
    for _ in range(n):
        dx = random.randint(-rad, rad)
        dy = random.randint(-rad, rad)
        dots.append([x + dx, y + dy, "black"])

def my_kmeans(k, h):
    data = np.array([[x, h - y] for x, y, _ in dots])
    centers = data[np.random.choice(len(data), k, replace=False)]
    for _ in range(100):
        dists = np.linalg.norm(data[:, None] - centers, axis=2)
        labels = np.argmin(dists, axis=1)
        new_centers = []
        for i in range(k):
            pts = data[labels == i]
            if len(pts) > 0:
                new_centers.append(np.mean(pts, axis=0))
            else:
                new_centers.append(centers[i])
        new_centers = np.array(new_centers)
        if np.allclose(centers, new_centers):
            break
        centers = new_centers
    for i in range(len(dots)):
        clr = colors[labels[i] % len(colors)]
        dots[i][2] = clr

def my_dbscan(eps, min_pts, h):
    data = np.array([[x, h - y] for x, y, _ in dots])
    labels = [-1] * len(data)
    visited = [False] * len(data)
    cid = 0

    def neighbors(i):
        return [j for j in range(len(data)) if np.linalg.norm(data[i] - data[j]) <= eps]

    for i in range(len(data)):
        if visited[i]:
            continue
        visited[i] = True
        nb = neighbors(i)
        if len(nb) < min_pts:
            labels[i] = -1
        else:
            labels[i] = cid
            queue = deque(nb)
            while queue:
                j = queue.popleft()
                if not visited[j]:
                    visited[j] = True
                    new_nb = neighbors(j)
                    if len(new_nb) >= min_pts:
                        queue.extend(new_nb)
                if labels[j] == -1:
                    labels[j] = cid
            cid += 1

    for i in range(len(dots)):
        if labels[i] != -1:
            dots[i][2] = colors[labels[i] % len(colors)]
        else:
            dots[i][2] = "black"

KMEANS_K = 4
DBSCAN_EPS = 35
DBSCAN_MIN_PTS = 4

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        elif e.type == pygame.VIDEORESIZE:
            W, H = e.w, e.h
            win = pygame.display.set_mode((W, H), pygame.RESIZABLE)
            redraw()

        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                make_bunch(e.pos[0], e.pos[1])
                redraw()

        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_k and dots:
                my_kmeans(KMEANS_K, H)
                redraw()

            if e.key == pygame.K_d and dots:
                my_dbscan(DBSCAN_EPS, DBSCAN_MIN_PTS, H)
                redraw()

pygame.quit()
