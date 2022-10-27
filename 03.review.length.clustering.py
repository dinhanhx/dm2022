import math
from random import seed, randint
seed(1)

data = [randint(1, 100) for i in range(10)]
dist_mat = [[abs(i - ii) for ii in data] for i in data]
clusters = [[i] for i in range(10)]
print(clusters)

def cal_dist_clus(c1: list, c2: list):
    temp_list = []
    for ec1 in c1:
        for ec2 in c2:
            if ec1 != ec2:
                temp_list.append(dist_mat[ec1][ec2])
    return min(temp_list)

for step in range(3):
    new_clusters = []
    temp_list = []
    for i1, c1 in enumerate(clusters):
        for i2, c2 in enumerate(clusters):
            if i1 != i2:
                temp_list.append([cal_dist_clus(c1, c2), i1, i2])
    _, to_merge1, to_merge2 = min(temp_list, key=lambda e: e[0])

    new_clusters.append(clusters[to_merge1].copy() + clusters[to_merge2].copy())
    for i, c in enumerate(clusters):
        if i == to_merge1:
            continue
        elif i == to_merge2:
            continue
        else:
            new_clusters.append(c)
    clusters = new_clusters.copy()
    print(clusters)
