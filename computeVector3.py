TopicSubNet = open('/Users/mac/downloads/dataset/graph-T16_sub0.txt').readlines()
rowid = 0
while True:
    if TopicSubNet[rowid].startswith('*Edges'):
        rowid += 1
        break
    rowid += 1
nodes = rowid-3+1

# vectors = [[0 for i in range(nodes)] for i in range(nodes)] # 注意不要用*会引用拷贝
#
# while True:
#     if TopicSubNet[rowid].startswith('*Triangles'):
#         rowid += 1
#         break
#     row = TopicSubNet[rowid].strip().split(' ')
#     author1, author2, collaboration = int(row[0]), int(row[1]), int(row[2])
#     vectors[author1-1][author2-1] = collaboration
#     rowid += 1
#
# for i in range(1, nodes+1):
#     row = TopicSubNet[i].strip().split(' ')
#     # 补充对角线的数据
#     try:
#         vectors[i-1][i-1] = int(row[-1])
#     except BaseException:
#         print(row, i)
#     # 补充下三角区域的数据
#     for j in range(1, i):
#         vectors[i-1][j-1] = vectors[j-1][i-1]

# 用 salton 指数计算向量值
vectors = [[0.0 for i in range(nodes)] for i in range(nodes)]
authorSet = {}
for i in range(nodes):
    authorSet[i] = set()
while True:
    if TopicSubNet[rowid].startswith('*Triangles'):
        rowid += 1
        break
    row = TopicSubNet[rowid].strip().split(' ')
    author1, author2 = int(row[0]), int(row[1])
    authorSet[author1-1].add(author2)
    authorSet[author2-1].add(author1)
    rowid += 1

for i in range(1, nodes+1):
    for j in range(1, i):
        vectors[i-1][j-1] = vectors[j-1][i-1]
    for j in range(i, nodes+1):
        s1 = authorSet[i-1]
        s2 = authorSet[j-1]
        salton = len(s1 & s2)/pow(len(s1)*len(s2), 0.5)
        vectors[i-1][j-1] = salton

out = open('output3/vectors2.txt', 'w')
for i in range(nodes):
    for j in range(nodes):
        out.write('%.5f\t' % vectors[i][j])
    out.write('\n')
    if i % 100 == 0:
        print('I am running')
out.close()
