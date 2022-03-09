from sklearn.decomposition import PCA
import numpy as np
from datetime import datetime

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
m = len(eigenVectors)
n = len(eigenVectors[0])
print(len(eigenVectors[0]))
# > 627 在浮点运算中，原 679 维
# > 146 在整数运算中，原 679 维
for i in range(m):
    for j in range(n):
        out.write('%d\t' % eigenVectors[i][j])
    out.write('\n')


end = datetime.now().strftime("%H:%M:%S")
print(f'the end time: {end}')

