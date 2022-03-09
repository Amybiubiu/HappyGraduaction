
Coauthor = open('/Users/mac/downloads/dataset/AMiner-Coauthor.txt').readlines()
# 对 coauthor 建立 index author_id 表
list = set()
id2index = dict()
index = 0
for line, i in zip(Coauthor, range(len(Coauthor))):
    row = line[1:].strip().split('\t')
    author1, author2 = row[0], row[1]
    if i/1000 == 0:
        print('I am running')
    if not id2index.__contains__(author1):
        id2index[author1] = index
        index += 1
    if not id2index.__contains__(author2):
        id2index[author2] = index
        index += 1

index2id = [0]*len(dict)
for key, value in id2index.items():
    if value/1000 == 0:
        print('I am running')
    index2id[value] = key

# 计算 vector
n = len(index2id)
