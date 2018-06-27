import pandas as pd
import numpy as np
import nltk
from nltk.tokenize.casual import casual_tokenize as tokenizer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt

''' 
	Helper functions
'''

def __cleanText(text):
	all_words = []
	txt = []
	for line in text:
		sent = tokenizer(line.lower())
		all_words.extend(sent)
		txt.append(sent)
	stop = list(stopwords.words("spanish"))
	stop.extend(['...', 'http', 'https', 'rt'])
	all_words_clean = []
	for word in all_words:
		if (word not in stop) and (len(word) > 2) and (word[0:4]!='http') and (word[0] != '@'):
			all_words_clean.append(word)
	return txt, all_words_clean

#needs text and X
def __obtainTopics(model, category):
	pred = model.predict(X)
	df = pd.DataFrame({'text': text, 'pred': pred})
	df = df[df.pred == category]
	txt = list(df.text)
	_, clean_text = __cleanText(txt)
	topics = nltk.FreqDist(clean_text)
	topics = list(topics)
	return topics, txt

csv = pd.read_csv('sincuotas.csv')
text = list(csv.text)

#clean text
txt, all_words_clean = __cleanText(text)

all_words_clean = nltk.FreqDist(all_words_clean)
word_features = list(all_words_clean)
noX = len(text)
noFeatures = len(word_features)
X = np.zeros((noX, noFeatures))

for i in range(noX):
	line = txt[i]
	for j in range(noFeatures):
		word = word_features[j]
		if word in line:
			X[i][j] = 1


# k means determine k
distortions = []
K = range(1,10)
for k in K:
    kmeanModel = KMeans(n_clusters=k).fit(X)
    kmeanModel.fit(X)
    distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])
 
# Plot the elbow
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('Optimal k')
plt.show()
