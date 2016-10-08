import nltk
from nltk.corpus import movie_reviews
import random
import csv
with open('dataset.txt', 'rb') as f:
	reader = csv.reader(f)
	dataset = list()
	for line in reader:
		dataset.append((line[0],line[1]))

documents = dataset
random.shuffle(documents)

all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(all_words)[:2000]

def document_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains({})'.format(word)] = (word in document_words)
	return features

#print(document_features(movie_reviews.words('pos/cv957_8737.txt'))) 

featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)
	
print(nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features(5)