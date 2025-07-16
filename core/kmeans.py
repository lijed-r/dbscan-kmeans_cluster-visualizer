import numpy as np
from config import COLORS

def my_kmeans(dots, k, h):
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
        clr = COLORS[labels[i] % len(COLORS)]
        dots[i][2] = clr
