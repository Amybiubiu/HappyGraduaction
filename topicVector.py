from time import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import json
import csv

n_features = 500
n_components = 30

file = open('dataset/author2.json')
data = json.load(file)
file.close()

data_interest = [item['interest'] for item in data]

print("Extracting tf features for LDA...")

# Use tf (raw term count) features for LDA.
tf_vectorizer = CountVectorizer(
    max_df=0.95, min_df=2, max_features=n_features, stop_words="english"
)
t0 = time()
tf = tf_vectorizer.fit_transform(data_interest)
print("done in %0.3fs." % (time() - t0))
print()

# 去除重复名字
authors_v = [sum(i) for i in tf.toarray()]
n = len(data)
i = 1
filter_id = []
while i < n:
    max_id = i-1
    while i < n and data[i]['id'] == data[i-1]['id']:
        if authors_v[i] > authors_v[max_id]:
            max_id = i
        i += 1
    filter_id.append(max_id)
    i += 1
print(f'the filter author number is {len(filter_id)}')

filter_data = [data[i] for i in filter_id]
# with open('dataset/author-filter2.json', 'w', encoding='utf-8') as f:
#     json.dump(filter_data, f, ensure_ascii=False, indent=4)
with open('dataset/author-filter.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_MINIMAL)
    for i in filter_id:
        spamwriter.writerow(data[i].values())
#
# # fit the LDA
# print('fit the LDA')
# tf = tf.toarray()
# tf = [tf[i] for i in filter_id]
# lda = LatentDirichletAllocation(
#     n_components=n_components,
#     max_iter=5,
#     learning_method="online",
#     learning_offset=50.0,
#     random_state=0,
# )
# t0 = time()
# lda.fit(tf)
# print("done in %0.3fs." % (time() - t0))
#
# text_topic = lda.transform(tf)
#
# # 记下作者的主题向量
# out = open('output3/topicVectors2.txt', 'w')
# for i in range(len(filter_id)):
#     out.write('%0.3f\t' % filter_id[i])
#     for j in range(n_components):
#         out.write('%0.3f\t' % text_topic[i][j])
#     out.write('\n')
# out.close()
#
#
# def cosine(v1, v2, m):
#     d1 = sum([i*2 for i in v1])
#     d2 = sum([i*2 for i in v2])
#     # float ?
#     return sum([v1[i]*v2[i] for i in range(m)])/pow(d1*d2, 0.5)
#
#
# # 计算主题临近度
# t0 = time()
# print(f'compute topic similarity')
# with open('result/similarity.txt', 'w') as similarity:
#     # id1 id2 similarity
#     for i in range(len(filter_id)):
#         id1 = data[filter_id[i]]['id']
#         similarity.write('%d\t%d\t%0.3f\n' % (id1, id1, 1))
#         for j in range(i+1, len(filter_id)):
#             id2 = data[filter_id[j]]['id']
#             simi = cosine(text_topic[i], text_topic[j], n_components)
#             similarity.write('%d\t%d\t%0.3f\n' % (id1, id2, simi))
#
# print("done in %0.3fs." % (time() - t0))
