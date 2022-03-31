import random
from datetime import datetime

#
def generateData(_range, num, file):
    start = _range['start']
    end = _range['end']
    out = open(file, 'w')
    out.write('id\tx\ty\n')
    for i in range(num):
        x = random.randrange(start, end)
        y = random.randrange(start, end)
        out.write('%d\t' % i)
        out.write('%d\t' % x)
        out.write('%d\n' % y)
    out.close()


# generateData({'start': 0, 'end': 100}, 400, 'data.txt')

def readfile(filename):
    lines = [line for line in open(filename)]

    # First line is the column titles
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # First column in each row is the rowname
        rownames.append(p[0])
        # The data for this row is the remainder of the row
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data


def distance(v1, v2):
    return pow(sum((v1[i] - v2[i]) ** 2 for i in range(len(v1))), 0.5)


# divisive analysis
def DIANA(data, distance, k):
    clusters = []
    # 分出 k 类
    # 初始整体为一个簇
    clusters.append([i for i in range(len(data))])
    while len(clusters) < k:
        print(f'I am running, the clusters(num) is {len(clusters)}')
        # 对直径最大的簇分裂
        big_id = 0
        for i in range(len(clusters)):
            # 复杂度计算
            # k*n*(n*m)
            big_id = i if diameter(clusters[i], data, distance) > diameter(clusters[big_id], data, distance) else big_id
        # 找该簇中最远离中心的点放入新簇
        far_id = clusters[big_id][0]
        new_clu = []

        center = getCenter(clusters[big_id], data)
        for id in clusters[big_id]:
            if distance(center, data[id]) > distance(center, data[far_id]):
                far_id = id
        new_clu.append(far_id)
        clusters[big_id].remove(far_id)
        # 将该簇中离新簇更近的点移入新簇中，直到不存在这样的点
        while True:
            count = 0
            c1 = getCenter(clusters[big_id], data)
            c2 = getCenter(new_clu, data)
            for id in clusters[big_id]:
                if distance(c1, data[id]) > distance(c2, data[id]):
                    new_clu.append(id)
                    clusters[big_id].remove(id)
                    count += 1
            if count == 0:
                break

        clusters.append(new_clu)
    return clusters

def kcluster(data, distance, k):
    # 随机选取 k 个样本为类中心
    # clusters = [data[i] for i in random.sample(range(len(data)), k)]

    # clusters = []
    # for i in range(k):
    #     idx = i*(len(data)//k)
    #     clusters.append(data[idx])
    # print(clusters)
    clusters = [getCenter(cluster, data) for cluster in DIANA(data, distance, k)]
    lastmatches = None
    for t in range(300):
        print(f'I am running,the time is {t}')
        # 将距离类中心最近的样本归类
        bestmatches = [[] for i in range(k)]
        # 复杂度计算
        # t*n*k*m
        for j in range(len(data)):
            bestmatch = 0
            for i in range(k):
                d = distance(clusters[i], data[j])
                if d < distance(clusters[bestmatch], data[j]):
                    bestmatch = i
            bestmatches[bestmatch].append(j)

        # 当分类不变时，退出
        if bestmatches == lastmatches: break
        lastmatches = bestmatches

        # 更新类中心坐标
        for i in range(k):
            avgs = [0.0] * len(data[0])
            if len(bestmatches[i]) > 0:
                for id in bestmatches[i]:
                    for dim in range(len(data[id])):
                        avgs[dim] += data[id][dim]
                for j in range(len(avgs)):
                    avgs[j] /= len(bestmatches[i])
                clusters[i] = avgs

    return bestmatches


# def meanDiameter(bestmatches, data, distance):
#     k = len(bestmatches)
#     clusters = [0]*k
#     for i in range(k):
#             avgs=[0.0]*len(data[0])
#             if len(bestmatches[i])>0:
#                 for id in bestmatches[i]:
#                     for dim in range(len(data[id])):
#                         avgs[dim] += data[id][dim]
#                 for j in range(len(avgs)):
#                     avgs[j]/=len(bestmatches[i])
#                 clusters[i]=avgs
#     _sum = 0
#     for i in range(len(bestmatches)):
#         for j in bestmatches[i]:
#             _sum += distance(data[j], clusters[i])
#     return _sum

def getCenter(cluster, data):
    avgs = [0.0] * len(data[0])

    for id in cluster:
        for dim in range(len(data[id])):
            avgs[dim] += data[id][dim]
    for i in range(len(avgs)):
        avgs[i] /= len(cluster)
    return avgs


def diameter(cluster, data, distance):
    # 任意两个样本间的最大距离
    n = len(cluster)
    d = 0
    for i in range(n):
        for j in range(i+1, n):
            d = max(d, distance(data[cluster[i]], data[cluster[j]]))
    return d


def meanDiameter(bestmatches, data, distance):
    n = len(bestmatches)
    sum = 0
    for i in range(len(bestmatches)):
        sum += diameter(bestmatches[i], data, distance)
    return sum / n


def formatNum(x, num):
    return x - x % num


def main():
    rownames, colnames, data = readfile('data.txt')
    ids = [i*10+1 for i in range(0,20)]
    for k in ids:
        bestmatches = kcluster(data, distance, k)
        d = meanDiameter(bestmatches, data, distance)
        print('d:', d, 'k:', k)
    return
    # r 和 _cons 的取值要依据数据
    # 求最优 k，类别数越小，平均直径越大，但到一个值时变化不大
    l, r = 1, len(data) // 2  # r = 40
    _cons = meanDiameter(kcluster(data, distance, r), data, distance)
    print('_cons before', _cons)
    _cons = formatNum(_cons, 1)
    print('_cons', _cons)
    k = 1
    while l < r:
        print('l:', l, 'r:', r)
        mid = (l + r) >> 1
        temp = kcluster(data, distance, mid)
        temp_dis = meanDiameter(temp, data, distance)
        print("temp_distance:", temp_dis, 'mid:', mid)
        temp_dis = formatNum(temp_dis, 1)
        if temp_dis == _cons:
            r = mid
        elif temp_dis > _cons:
            l = mid + 1

    k = mid
    print("after binary search, the best k: ", k)
    # 返回同类 row 的 id 序列的 列表
    categories = kcluster(data, distance, k)
    # 向 txt 写入聚类的结果
    out = open('output2.txt', 'w')
    out.write('id\tx\ty\tcategory\n')
    for i in range(len(categories)):
        for j in categories[i]:
            out.write(rownames[j] + '\t')
            out.write('%d\t' % data[j][0])
            out.write('%d\t' % data[j][1])
            out.write('%d\n' % i)
    out.close()
    # 向 json 写入聚类的结果
    jsonData = []
    for i in range(len(categories)):
        for j in categories[i]:
            item = {}
            item['id'] = rownames[j]
            item['x'] = data[j][0]
            item['y'] = data[j][1]
            item['category'] = i
            jsonData.append(item)
    import json
    with open('output2.json', 'w', encoding='utf-8') as f:
        json.dump(jsonData, f, ensure_ascii=False, indent=4)


# main()

def devide():
    vectors = open('output3/eigenVectors.txt').readlines()
    data = [[float(i) for i in line.strip().split('\t')] for line in vectors]
    # ids = [i*20+1 for i in range(len(data)//20)] # 注意 k 不能取 0
    # start = datetime.now().strftime('%H:%M:%S')
    # print(f'start time: {start}')
    # for k in ids:
    #     bestmatches = kcluster(data, distance, k)
    #     d = meanDiameter(bestmatches, data, distance)
    #     print('d:', d, 'k:', k)
    # end = datetime.now().strftime('%H:%M:%S')
    # print(f'end time: {end}')
    # return # 选出了最优的k为60，接受下降间距为 20；或者 k 为 40，接受下降间距为40
    k = 40

    start = datetime.now().strftime('%H:%M:%S')
    print(f'start time: {start}')
    categories = kcluster(data, distance, k)
    end = datetime.now().strftime('%H:%M:%S')
    print(f'end time: {end}')
    # 向 txt 写入聚类结果
    res = open('result/res2.txt', 'w')
    res.write('id\tcategory\n')
    for i in range(len(categories)):
        for j in categories[i]:
            res.write('%d\t%d\n' % (j+1, i))
    res.close()
    # 向 json 写入聚类结果
    jsondata = []
    for i in range(len(categories)):
        for j in categories[i]:
            item = {}
            item['id'] = j+1
            item['category'] = i
            jsondata.append(item)

    import json
    with open('result/res2.json', 'w', encoding='utf-8') as f:
        json.dump(jsondata, f, ensure_ascii=False, indent=4)


devide()
# 可能可以优化的点
# 1、点与点之间的距离，矩阵存储，避免多次计算
# 2、k-means 聚类，类中心的选取换用别的聚类方式，而不是分裂聚类
# 其他：换用更大的数据分析，变更属性的计算方法？PCA 自己实现。
