from random import randint, seed
from typing import Dict, List

seed(1)

def flat_kernel(x, bandwidth):
    return 1 if x < bandwidth else 0

def shift_mode(data: list, mode: List[Dict], current_i: int, current_k: int):
    numerator = 0
    for j in data:
        numerator += j * flat_kernel(j - mode[current_i][current_k], 20)
    denominator = 0
    for j in data:
        denominator += flat_kernel(j - mode[current_i][current_k], 20)
    return numerator / denominator

def mean_shift_cluster(data: list, threshold: float):
    mode = [{} for _ in data]
    for i, p in enumerate(data):
        k = 0
        mode[i][k] = p
        while True:
            mode[i][k+1] = shift_mode(data, mode, i, k)
            k = k + 1
            if abs(mode[i][k] - mode[i][k-1]) < threshold:
                break
        mode[i][0] = mode[i][k]

    clusters = []
    for i, p in enumerate(data):
        if mode[i][0] not in clusters:
            clusters.append(mode[i][0])

    return clusters

if '__main__' == __name__:
    data = [randint(1, 100) for i in range(100)]
    print(data)
    clusters = mean_shift_cluster(data, 0.005)
    print(clusters)