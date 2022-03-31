from sklearn.decomposition import PCA
import numpy as np
from datetime import datetime
from time import time

start = datetime.now().strftime("%H:%M:%S")
print(f'the start time: {start}')

vectors = open('output3/vectors.txt')
data = [[i for i in line.strip().split('\t')] for line in vectors]
X = np.array(data)
pca = PCA(n_components='mle')
pca.fit(X)
print(pca.explained_variance_ratio_)

eigenVectors = pca.transform(X)

out = open('output3/eigenVectors.txt', 'w')
# check 一下是否与 eigenVectors 一致。 是一样的～
m = len(eigenVectors)
n = len(eigenVectors[0])
print(len(eigenVectors[0]))
# >> 627 在浮点运算中，原 679 维
# >> 146 在整数运算中，原 679 维
for i in range(m):
    for j in range(n):
        out.write('%d\t' % eigenVectors[i][j])
    out.write('\n')


end = datetime.now().strftime("%H:%M:%S")
print(f'the end time: {end}')


def euclidean(v1, v2):
    return pow(sum((v1[i] - v2[i]) ** 2 for i in range(len(v1))), 0.5)


# compute distance
t0 = time()
print('compute distance start')
with open('result/distance.txt', 'w') as distance:
    # id1 id2 distance
    for i in range(m):
        distance.write('%d\t%d\t%d\n' % (i+1, i+1, 0))
        for j in range(i+1, m):
            dis = euclidean(eigenVectors[i], eigenVectors[j])
            distance.write('%d\t%d\t%d\n' % (i+1, j+1, dis))

print("done in %0.3fs." % (time() - t0))
