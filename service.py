import pandas as pd

def evaluate(text):
    worth_watch = "BAD"
    estimated_runtime = 180 
    estimated_gross = 9999
    estimated_voteaverage = 5.0

    # text for analysis 
    
    import nltk
    import re
    import statistics

    from nltk import word_tokenize
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')

    # processing the text into various formats

    # punctuation separated
    text_punct_sep = re.sub('^(\W+)(\w)', r'\1 \2', text)
    text_punct_sep = re.sub('(\w)(\W+)$', r'\1 \2', text_punct_sep)
    text_punct_sep = re.sub('(\w)(\W+)(\s+)', r'\1 \2\3', text_punct_sep)
    text_punct_sep = re.sub('(\s+)(\W+)(\w)', r'\1\2 \3', text_punct_sep)
    text_punct_sep = text_punct_sep.split()

    # tokenized (same as above except for 's)
    text_tokenize = nltk.word_tokenize(text)

    # sentence-tokenized
    text_sent_tokenize = nltk.sent_tokenize(text)
    text_sent_tokenize = [nltk.word_tokenize(sent) for sent in text_sent_tokenize]

    # lowercase
    text_lower = [word.lower() for word in text_tokenize]

    # with stopwords removed
    stopwords = nltk.corpus.stopwords.words('english')
    text_stopwords = [word for word in text_lower if word.isalpha()]
    text_stopwords = [word for word in text_stopwords if word not in stopwords]

    # with part-of-speech tags
    text_pos = nltk.pos_tag(text_lower)

    # creating numerical features

    # wordcount 
    wordcount = [word for word in text_punct_sep if not re.fullmatch(r'\W+', word)]
    wordcount = len(wordcount)

    # average sentence length
    sentence_wordcount = [[ word for word in sent if not re.fullmatch(r'\W+', word)] for sent in text_sent_tokenize]
    sentence_wordcount = [len(sent) for sent in sentence_wordcount]
    avg_sent_length = statistics.mean(sentence_wordcount)

    # adjective frequency
    adjectives =  [word for word, pos in text_pos if pos=='JJ']
    adjective_ratio = len(adjectives) / wordcount

    # noun frequency
    nouns = [word for word, pos in text_pos if pos.startswith('NN')]
    noun_ratio = len(nouns) / wordcount

    punctuation = [word for word in text_punct_sep if re.fullmatch(r'\W+', word)]

    # number of ellipses
    ellipses = len([punct for punct in punctuation if re.fullmatch('...', punct)])

    # number of exclamation points
    exclamation_points = len([punct for punct in punctuation if re.fullmatch('!', punct)])

    # number of punctuation not . or ,
    unusual_punctuation_count = len([punct for punct in punctuation if not re.fullmatch('[.|,]', punct)])
    
    # combine features into list

    features = [wordcount, avg_sent_length, adjective_ratio, noun_ratio, ellipses, exclamation_points, unusual_punctuation_count]
    
    # calculate goodness score, determine if movie is worth watching
    
    goodness_threshold = 7.1#7.4795 

    goodness_weights = [-7.71407791e-04,  1.03398645e-02,  7.71486628e-01, -4.29889367e-01, -6.32915313e-02, -4.12801859e-02, -3.78410081e-02]
    goodness_intercept = 6.958988761645412
    goodness_prediction = (sum([i*j for (i, j) in zip(features, goodness_weights)])) + goodness_intercept

    if (goodness_prediction >= goodness_threshold):
        worth_watch = 'GOOD'
    else: 
        worth_watch = 'BAD'
        
    # Make some other predictions
        
    # Average vote (rounded to one decimal)
        
    avg_vote_weights = [-9.73543499e-05,  7.69850735e-03,  4.65215483e-01,  5.06789916e-01,  -1.11094320e-01, -4.45053509e-02, -2.61515468e-02]

    avg_vote_intercept = 5.972316452574906

    estimated_voteaverage = round(sum([i*j for (i, j) in zip(features, avg_vote_weights)]) + avg_vote_intercept, 1)
    
    # gross (rounded to millions)

    gross_estimate_weights = [153098.88951514, 1504577.97489657, 63650591.92309033, 86170657.81516224, -16112068.2772915, 4811965.43400595, -4400734.62127683]

    gross_estimate_intercept = 1350657.010381654

    estimated_gross = (sum([i*j for (i, j) in zip(features, gross_estimate_weights)])) + gross_estimate_intercept

    estimated_gross = round(round(estimated_gross, -6))
    
    # runtime (rounded to minutes)
    
    runtime_weights = [-2.08926917e-02, 2.25826341e-02, -6.47820334e+00, 2.27658087e+01, -4.43987245e+00, -4.69880945e+00, -3.39422560e-01]

    runtime_intercept = 104.49783726105622

    estimated_runtime = round((sum([i*j for (i, j) in zip(features, runtime_weights)])) + runtime_intercept)

    goodness_prediction = round(goodness_prediction, 2)

    return(worth_watch, estimated_runtime, estimated_gross, estimated_voteaverage, goodness_prediction)

def recommendation():
    df = pd.read_csv('Data/data_processed_final.csv')
    recommendations = (df[ df["goodness_factor"] > 7.48].sample(3))
    list = []
    for index, recommendation in recommendations.iterrows():
        id = recommendation["id"] 
        title = recommendation["original_title"] 
        goodness = round(recommendation["goodness_factor"], 2)
        movie = [id, title, goodness]
        list.append(movie)
    return(list)

