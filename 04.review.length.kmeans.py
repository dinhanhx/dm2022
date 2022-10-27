import numpy as np
import math
from random import seed, randint
seed(1)

data = [randint(1, 100) for i in range(100)]
print(data)

num_centroids = 3
clusters = {k: {'points': [], 'center': randint(1, 100), 'movable': True} for k in range(num_centroids)}

print(clusters)

while True:
    for point in data:
        point_2_center_dist_list = []
        for index, cluster in clusters.items():
            dist = abs(cluster['center'] - point)
            point_2_center_dist_list.append((dist, index))
        _, index = min(point_2_center_dist_list, key=lambda x:x[0])
        clusters[index]['points'].append(point)

    for index, cluster in clusters.items():
        new_center = sum(cluster['points'])/len(cluster['points'])
        if abs(cluster['center'] - new_center) < 0.005:
             cluster['movable'] = False
        else:
            cluster['center'] = new_center
    print('===')
    print(clusters)
    print('===')

    if True in [cluster['movable'] for index, cluster in clusters.items()]:
        for index, cluster in clusters.items():
            cluster['points'] = []
    else:
        break
