import numpy as np
from collections import deque
from config import COLORS

def my_dbscan(dots, eps, min_pts, h):
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
            dots[i][2] = COLORS[labels[i] % len(COLORS)]
        else:
            dots[i][2] = "black"
