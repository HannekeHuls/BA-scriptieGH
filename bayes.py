#!/usr/bin/python3

# Basic classifiction functionality with Naive Bayes. File provided for the assignment on classification (IR course 2016/17)

import nltk.classify
from nltk.tokenize import word_tokenize
from featx import bag_of_words, high_information_words
from classification import precision_recall

from random import shuffle
from os import listdir # to read files
from os.path import isfile, join # to read files
import sys
import re

stopWords = [" de ", " en ", " van ", " ik ", " te ", " dat ", " die ", " in ", " een ", " hij  ",
				" het ", " niet ", " zijn ", " is ", " was ", " op ", " aan ", " met ", " als ", " voor ",
				" had ", " er ", " maar ", " om ", " hem ", " dan ", " zou ", " of ", " wat ", " mijn ",
				" men ", " dit ", " zo ", " door ", " over ", " ze ", " zich ", " bij ", " ook ", " tot ",
				" je ", " mij ", " uit ", " der ", " daar ", " haar ", " naar ", " heb ", " hoe ", " heeft ",
				" hebben ", " deze ", " u ", " want ", " nog ", " zal ", " me ", " zij ", " nu ", " ge ",
				" geen ", " omdat ", " iets ", " worden ", " toch ", " al ", " waren ", " veel ", " meer ", " doen ",
				" toen ", " moet ", " ben ", " zonder ", " kan ", " hun ", " dus ", " alles ", " onder ", "ja",
				" eens ", " hier ", " wie ", " werd ", " altijd ", " wordt ", " wezen ", " kunnen ", " ons ",
				" zelf ", " tegen ", " na ", " reeds ", " wil ", " kon ", " niets ", " uw ", " iemand ", "geweest", 
				" andere "," d66 "," cda ", " sp ", " cu ", " christen ", " unie ", " vvd ", " pvdd ", " dieren ", 
				" tot ", " twee ", " alsnog ", " paar ", " groenlinks ", " castelein "," schaaf "," schroor ",
				" gijsbertsen "," leemhuis ", "honkoop"," dijk ", " brouwer ", " paulusma "," rook "," luhoff "," bolle ",
				" doesen "," benjamin "," gijlswijk "," duin "," greef ", " jongman "," verhoef "," kuik "," koopmans ",
				" kelder ","rooij", "ubbens"," temmink ", "koebrugge"," blom "," rustebiel "," schimmel "," glas ", " eerder ", " steunen ",
				" christenunie ", " heer ", " wethouder ", " der ", " slot ", " partij ", " selwerd ", " daarbij ", " aanzien ", 
				" verwoord ", " instemming "," vast ", " zuidelijke "," koks ", " bestemmingsplan ", " uiteindelijk ",
				" ook ", " zoveel ", " paar "," daarbij ", " alles ", " hele ", " laastste ", " martiniplaza ",
				" vondellaan ", " vvd-fractie ", "keulen", 'wethouder','chakor', 'bloemhoff', 'veen', 'istha',
				" fractie ", " los ", " amendement ", " zoveel ", " tot ", " zullen ", " ringweg ", " hebt ", " is ", 
				" 2015 ", " pvda ", " partij ", " wel ", " ruddijs ", " laan ", " mevrouw "]


# return all the filenames in a folder
def get_filenames_in_folder(folder):
	return [f for f in listdir(folder) if isfile(join(folder, f))]


# reads all the files that correspond to the input list of categories and puts their contents in bags of words
def read_files(categories, stopwords):
	train_feats = [] 
	test_feats = []

	for category in categories:
		files = get_filenames_in_folder('Raad/' + category)	
		feats = []
		train = []
		test = []	
		for f in files:
			data = open('Raad/' + category + '/' + f, 'r', errors="ignore").read()
			data = data.lower()
			for ch in '!"(),?:.\;"':
				data = data.replace(ch," ")
			for ch in '\n':
				data = data.replace(ch," ")

			for word in stopWords:
				pattern = re.compile('(\s*){}(\s*)'.format(word))
				data = pattern.sub(' ', data)

			tokens = word_tokenize(data)
			bag = bag_of_words(tokens)
			feats.append((bag, category))


		split = 0.9	
		cutoff = int(len(feats) * split)
		train, test = feats[:cutoff], feats[cutoff:]
		train_feats = train_feats + train 
		test_feats = test_feats + test

		#print ("  Category %s, %i files read" % (category, num_files))

	return  train_feats, test_feats

def train(train_feats):
	classifier = nltk.classify.NaiveBayesClassifier.train(train_feats)
	return classifier

def calculate_f(precisions, recalls):
	denominator = precisions * recalls
	nominator = precisions + recalls
	f_measures = 2*(denominator / nominator)

	return f_measures

# prints accuracy, precision and recall
def evaluation(classifier, test_feats, categories):
	print("  Accuracy: %f" % nltk.classify.accuracy(classifier, test_feats))
	precisions, recalls = precision_recall(classifier, test_feats)


	for category in categories:
		category, precisions[category], recalls[category]
				
		p =precisions[category]
		r =recalls[category]

		f_measures = calculate_f(p,r)

		print(category, " & ", precisions[category]," & ", recalls[category], " & ", f_measures)


# show informative features
def analysis(classifier):
	classifier.show_most_informative_features(5)



# obtain the high information words
def high_information(feats, categories):

	labelled_words = [(category, []) for category in categories]

	#1. convert the formatting of our features to that required by high_information_words
	from collections import defaultdict
	words = defaultdict(list)
	all_words = list()
	for category in categories:
		words[category] = list()

	for feat in feats:
		category = feat[1]
		bag = feat[0]
		for w in bag.keys():
			words[category].append(w)
			all_words.append(w)
#		break

	labelled_words = [(category, words[category]) for category in categories]
	#print labelled_words

	#calculate high information words
	high_info_words = set(high_information_words(labelled_words))

	return high_info_words


categories = []
for arg in sys.argv[1:]:
	categories.append(arg)


train_feats, test_feats = read_files(categories,stopWords)
classifier = train(train_feats)
evaluation(classifier, test_feats, categories)
analysis(classifier)