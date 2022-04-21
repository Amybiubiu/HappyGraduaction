from time import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import json
import re
import nltk
import gensim
from nltk.corpus import stopwords

from nltk.stem.snowball import PorterStemmer
from gensim.models import Word2Vec
import gensim.downloader as api


file = open('dataset/author-filter2.json')
data = json.load(file)
data_interest = [item['interest'] for item in data]
data_id = [item['id'] for item in data]


def latent_dirichlet_allocation(text, data_id):
    n_features = 500
    n_components = 30
    print("Extracting tf features for LDA...")

    # Use tf (raw term count) features for LDA.
    tf_vectorizer = CountVectorizer(
        max_df=0.95, min_df=2, max_features=n_features, stop_words="english"
    )
    t0 = time()
    tf = tf_vectorizer.fit_transform(text)
    print("done in %0.3fs." % (time() - t0))

    # fit the LDA
    print('fit the LDA')
    lda = LatentDirichletAllocation(
        n_components=n_components,
        max_iter=5,
        learning_method="online",
        learning_offset=50.0,
        random_state=0,
    )
    t0 = time()
    lda.fit(tf)
    print("done in %0.3fs." % (time() - t0))

    text_topic = lda.transform(tf)

    # 记下作者的主题向量
    out = open('output3/topicVectors-word2vec.txt', 'w')
    for i in range(len(text)):
        out.write('%d\t' % data_id[i])
        for j in range(n_components):
            out.write('%0.3f\t' % text_topic[i][j])
        out.write('\n')
    out.close()

    def cosine(v1, v2, m):
        d1 = sum([i*2 for i in v1])
        d2 = sum([i*2 for i in v2])
        # float ?
        return sum([v1[i]*v2[i] for i in range(m)])/pow(d1*d2, 0.5)


    # 计算主题临近度
    t0 = time()
    print(f'compute topic similarity')
    with open('result/similarity-word2vec.txt', 'w') as similarity:
        # id1 id2 similarity
        for i in range(len(text)):
            id1 = data_id[i]
            similarity.write('%d\t%d\t%0.3f\n' % (id1, id1, 1))
            for j in range(i+1, len(text)):
                id2 = data_id[j]
                simi = cosine(text_topic[i], text_topic[j], n_components)
                similarity.write('%d\t%d\t%0.3f\n' % (id1, id2, simi))

    print("done in %0.3fs." % (time() - t0))


def preprocess_text(sen):
    # Remove punctuations and numbers
    sentence = re.sub('[^a-zA-Z]', ' ', sen)

    # Single character removal
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)

    # Removing multiple spaces
    sentence = re.sub(r'\s+', ' ', sentence)

    stops = stopwords.words('english')
    # print(stops)
    porter = PorterStemmer()
    for word in sentence.split():
        if word in stops:
            sentence = sentence.replace(word, '')
        # sentence = sentence.replace(word, porter.stem(word))
    return sentence.lower()


data_interest = [preprocess_text(i) for i in data_interest]
sentences = [i.split() for i in data_interest]
print(f'sentences: {sentences[:2]}')
# 模型训练
# model = Word2Vec(sentences, sg=0, size=300, window=3, min_count=5, negative=3, sample=0.001, hs=0)
# 保存模型
# model.save('./MyModel')   # 可以在读取后追加训练
# model.save_word2vec_format('./mymodel.txt', binary=False)
# model.save_word2vec_format('./mymodel.bin.gz', binary=True)
# 加载模型和词向量
# model = gensim.models.Word2Vec.load('./mymodel')
# model = gensim.models.KeyedVectors.load_word2vec_format('./vectors.txt', binary=False)
# model = gensim.models.KeyedVectors.load_word2vec_format('./vectors.bin', binary=True)

# 扩充词
t0 = time()
text = []
print(f'start load model')
model = api.load('glove-wiki-gigaword-50')
print(f"done in %0.3fs." % (time() - t0))
print('extend word start')
for i in range(len(sentences)):
    for j in range(len(sentences[i])):
        if sentences[i][j] in model.key_to_index:
            similar = model.most_similar(sentences[i][j])
            similar = list(map(lambda x: x[0], similar[:5]))
            similar.append(sentences[i][j])
            sentences[i][j] = ' '.join(similar)
        # else:
            # print(f'{sentences[i][j]} not present')
    text.append(' '.join(sentences[i]))
    # 存一下扩充文本？
    if i % 50 == 0:
        print(f'I am running')
        # print(f'text: {text[i]}')

with open('output3/text.txt', 'w') as f:
    for i in range(len(text)):
        f.write('%d|%s\n' % (data_id[i], text[i]))

del model
print("done in %0.3fs." % (time() - t0))

# latent_dirichlet_allocation(text, data_id)
