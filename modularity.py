import numpy as np


def Q(array, cluster):
    # 总边数
    m = sum(sum(array)) / 2
    k1 = np.sum(array, axis=1)
    k2 = k1.reshape(k1.shape[0], 1)
    # 节点度数积
    k1k2 = k1 * k2
    # 任意两点连接边数的期望值
    Eij = k1k2 / (2 * m)
    # 节点v和w的实际边数与随机网络下边数期望之差
    B = array - Eij
    # 获取节点、社区矩阵
    node_cluster = np.dot(cluster, np.transpose(cluster))
    results = np.dot(B, node_cluster)
    # 求和
    sum_results = np.trace(results)
    # 模块度计算
    Q = sum_results / (2 * m)
    print("Q:", Q)
    # Q: 0.35409333970966117
    return Q


if __name__ == '__main__':
    vectors = open('output3/vectors.txt')
    data = [[int(i) for i in line.strip().split('\t')] for line in vectors]
    array1 = np.array(data)
    n = len(data)
    categories = {}
    with open('result/res.txt') as file:
        for line in file:
            index, category = list(map(lambda x: int(x), line.strip().split('\t')))
            if category in categories:
                categories[category].append(index)
            else:
                categories[category] = [index]
    print(f'cate:{categories}')
    data2 = [[0 for j in range(len(categories))] for i in range(n)]
    for i in range(n):
        for j in range(len(categories)):
            if i in categories[j]:
                data2[i][j] = 1
            else:
                data2[i][j] = 0
    # clusters1 = np.array([[1 if i in categories[j] else 0 for j in range(len(categories))] for i in range(n)])
    clusters1 = np.array(data2)
    Q(array1, clusters1)
    # 邻接矩阵，2表示节点2和节点3之间有两条边相连
    array = np.array([[0, 1, 1],
                      [1, 0, 2],
                      [1, 2, 0]])

    # 节点类别分别是1,2,2
    cluster = np.array([[1, 0], [0, 1], [0, 1]])
    # Q(array, cluster)

