import nltk
import random

from nltk.corpus import movie_reviews
documents = [(list(movie_reviews.words(fileid)), category)
    for category in movie_reviews.categories()
    for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)

lowercase_words = [w.lower() for w in movie_reviews.words()]

word_frequencies = nltk.FreqDist(lowercase_words)
word_features = [word for word, frequency in word_frequencies.most_common(1000)] 

all_bigrams = nltk.bigrams(lowercase_words)
bigram_frequencies = nltk.FreqDist(all_bigrams)
bigram_features = [bigram for bigram, frequency in bigram_frequencies.most_common(1000)] 

def common_words_feature(document):
    features = {}
    document_words = set(document) 
    for word in word_features :
        features['contains({})'.format(word)] = (word in document_words)
    return features

def beginning_words_feature(document):
    features = {}
    if len(document)>30 :
        start_of_document = document[:30]
    else:
        start_of_document = document
    for word in word_features :
        features['begins({})'.format(word)] = (word in start_of_document)
    return features

def ending_words_feature(document):
    features = {}
    if len(document)>30 :
        end_of_document = document[-30:]
    else:
        end_of_document = document
    for word in word_features :
        features['ends({})'.format(word)] = (word in end_of_document)
    return features

def bigram_feature(document):
    features = {}
    document_bigrams = set(nltk.bigrams(document))
    for bigram in bigram_features :
        features['bigram({0} {1})'.format(bigram[0], bigram[1])] = (bigram in document_bigrams)
            
    return features

def test_classifier(feature_functions) :
    featuresets = []
    for (document, category) in documents:
        features = {}
        if "common" in feature_functions : 
            features.update(common_words_feature(document))
        if "begins" in feature_functions :
            features.update(beginning_words_feature(document))
        if "ends" in feature_functions :
            features.update(ending_words_feature(document))
        if "bigrams" in feature_functions :
            features.update(bigram_feature(document))
        
        featuresets.append((features, category))
    
    train_set, test_set = featuresets[100:], featuresets[:100]
    bayes_classifier = nltk.NaiveBayesClassifier.train(train_set)

    print("Classifier accuracy: ", nltk.classify.accuracy(bayes_classifier, test_set))
    bayes_classifier.show_most_informative_features(30)
    print()

def main():
    print("Testing using common words only.") 
    test_classifier(["common"])
    # Accuracies: 0.83 0.75 0.77 0.75 0.77 0.75 0.84

    print("Testing using first 30 words only.") 
    test_classifier(["begins"])
    # Accuracies: 0.62 0.58 0.53 0.59 0.56 0.51 0.6

    print("Testing using last 30 words only.") 
    test_classifier(["ends"])
    # Accuracies: 0.64 0.72 0.6 0.65 0.53 0.68 0.68

    print("Testing using common bigrams only.") 
    test_classifier(["bigrams"])
    # Accuracies: 0.76 0.69 0.73 0.73 0.68 0.77 0.7

    print("Testing a combination common-ends-begins-bigrams.")
    test_classifier(["common", "ends", "begins", "bigrams"])
    # Accuracies: 0.85 0.8 0.75 0.78 0.74 0.78 0.8

main()

# Ranking: BEST -> Combination - Common words - Bigrams - Last 30 words - First 30 words <- WORST
#
# The 'most common words' classifier functions quite well, with accuracy consistently about 0.8.
#
# Combination of all features seems to function slightly better than most common words, and better than any other combination I tested. 
# In the most informative features list of the combination, most fetures are either begins(word) or ends(word)
# so I tested using just those features, but that drastically lowers the accuracy.
#
# The bigram classifier seems not very useful as most common bigrams in the movie review data are mostly too common,
# for example "of the", "there is" or "have been". Also, I didn't remove punctuation from the original words list
# but it seems necessary. However, accuracy is quite consistently around 0.7. 
#
# The first/last 30 words classifiers performed quite poorly in these tests. However, the accuracies for these
# fluctuate the most, in earlier tests I saw values around 0.8 as well. 

