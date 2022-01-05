import random 

def generateData(_range, num, file):
    start=_range['start']
    end=_range['end']
    out=open(file, 'w')
    out.write('id\tx\ty\n')
    for i in range(num):
        x=random.randrange(start, end)
        y=random.randrange(start, end)
        out.write('%d\t' % i)
        out.write('%d\t' % x)
        out.write('%d\n' % y)
    out.close()
    
generateData({'start': 0, 'end': 100}, 400, 'data.txt')

def readfile(filename):
  lines=[line for line in open(filename)]
  
  # First line is the column titles
  colnames=lines[0].strip().split('\t')[1:]
  rownames=[]
  data=[]
  for line in lines[1:]:
    p=line.strip().split('\t')
    # First column in each row is the rowname
    rownames.append(p[0])
    # The data for this row is the remainder of the row
    data.append([float(x) for x in p[1:]])
  return rownames,colnames,data

def distance(v1, v2):
    return sum((v1[i]-v2[i])**2 for i in range(len(v1)))

def kcluster(data, distance, k):
    # 随机选取 k 个样本为类中心
    clusters=[data[i] for i in random.sample(range(len(data)), k)]
    # print(clusters)
    lastmatches=None
    for t in range(300):
        # 将距离类中心最近的样本归类
        bestmatches=[[] for i in range(k)]
        for j in range(len(data)):
            bestmatch=0
            for i in range(k):
                d=distance(clusters[i], data[j])
                if d < distance(clusters[bestmatch], data[j]):
                    bestmatch=i
            bestmatches[bestmatch].append(j)

        # 当分类不变时，退出
        if bestmatches==lastmatches: break
        lastmatches=bestmatches

        # 更新类中心坐标
        for i in range(k):
            avgs=[0.0]*len(data[0])
            if len(bestmatches[i])>0:
                for id in bestmatches[i]:
                    for dim in range(len(data[id])):
                        avgs[dim] += data[id][dim]
                for j in range(len(avgs)):
                    avgs[j]/=len(bestmatches[i])
                clusters[i]=avgs

    return bestmatches


def meanDiameter(bestmatches, data, distance):
    k = len(bestmatches)
    clusters = []
    for i in range(k):
            avgs=[0.0]*len(data[0])
            if len(bestmatches[i])>0:
                for id in bestmatches[i]:
                    for dim in range(len(data[id])):
                        avgs[dim] += data[id][dim]
                for j in range(len(avgs)):
                    avgs[j]/=len(bestmatches[i])
                clusters[i]=avgs
    _sum = 0
    for i in bestmatches:
        for j in bestmatches[i]:
            _sum += distance(data[j], cluster[i])
    return _sum 

def main():
    rownames, colnames, data = readfile('data.txt')
    # 求最优 k，类别数越小，平均直径越大，但到一个值时变化不大
    # l, r = 0, len(data[0])
    # _min = meanDiameter([data], data, distance)
    k = 15
    # while(l < r){
    #     k = (l+r)>>1
    #     temp = kcluster(data, distance, k)
    #     if(cal):
    #         l += 1
    #     else

    # }

    # 返回同类 row 的 id 序列的 列表
    categories = kcluster(data, distance, k)
    # 向 txt 写入聚类的结果
    out = open('output.txt', 'w')
    out.write('id\tx\ty\tcategory\n')
    for i in range(len(categories)):
        for j in categories[i]:
            out.write(rownames[j]+'\t')
            out.write('%d\t'%data[j][0])
            out.write('%d\t'%data[j][1])
            out.write('%d\n'%i)
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
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(jsonData, f, ensure_ascii=False, indent=4)   

main()