import numpy as np
import re
from nltk.tokenize import *
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from nltk import word_tokenize, pos_tag

#fix issue with ascii encoding errors
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def extract_birth(text, born = True):
    """Helper method that takes a list of two strings of text, converts them into integers
    return the either the first one or the second (if the second isn't empty; empty = 0)
    """
    extracted = 0
    if str(text) != 'nan':
        if not born:
            if len(text)>1:
                extracted = int(text[1])
        else:           
            extracted = int(text[0])
    return extracted


def extract_bio(text, part = 'city'):
    """Helper method to extract city, state, and country string variables from the birthplace column
    """
    split_text_blob = text.split(',')
    
    # based on the data found in the column, the second item as delimited by the comma is the country
    # where the poet represents/is from, the first item in the column is the city state, separated by spaces
    citystate = split_text_blob[0].strip().split(' ')
    
    city = []
    state = ''
    country = ''
    
    for word in citystate:
        #state is two chars long
        if len(word) == 2:
            state = word
        #city names are longer than state abbreviation, could also contain 
        #county or neighborhood if poet is non-US based
        if len(word) > 2:
            city.append(word)
            
    if len(word) > 1:
        country = word[1]
    
    if part == 'city':
        return ' '.join(city).strip()
    elif part == 'state':
        return state.strip()
    else:
        return country.strip()


def countlines(text):
    """Takes in list of strings, or string, returns the number of lines as a float but not count stanzas
    """
    
    #expression to search for
    expression ='.+\n'
    
    #store text into a variable
    strtext = u''.join(text)
    
    #for some poem_texts, newlines are not denoted by \n, rather
    #test is a list of strings, and each string denotes the start of each new line    
    if len(re.findall(expression,strtext)) == 0:
        numnewl = len(text)
    else:
        numnewl = len(re.findall(expression, strtext))
    return float(numnewl)


def countstanza(text):
    """
    Takes in a list of strings, or string, returns the number of stanzas
    """
    #expression to exclude, and expression to search for
    excexpression = '.+\n'
    expression = '.+\n\n'
    
    #store text into a variable
    strtext = u''.join(text)
    
    numstanzas = 0
    
    #for some poem_texts, newlines are not denoted by \n, rather
    #test is a list of strings, and each string denotes the start of each new line, thus I am
    #looking for empty items to denote a stanza separation
    if len(re.findall(excexpression,strtext)) == 0:
        for i in text:
            if len(str(i)) ==0:
                numstanzas += 1
    else:
        numstanzas = len(re.findall(expression, strtext))
        
    return float(numstanzas+1)


def sent_avglines(text):
    """Takes in a list of strings or strings and returns the average number of 
    lines each sentence will contain
    """
    nlines = []
    text = u''.join(text)
    
    #tokenize the text blob into sentences
    t_sent = sent_tokenize(text)
    
    for t in t_sent:
        nlines.append(countlines(t))
        
    return np.mean(nlines)


def count_words(text, distinct = False):
    """
    Takes in a list of strings or string and tokenizes all words, ignoring numbers, and returns
    the number of words or the number of distinct words based on the parameter distinct
    """    
    #instantiate nltk's regex tokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    tokenized = tokenizer.tokenize(u''.join(text))
    
    numwords = len(tokenized)
    
    if distinct:
        numwords = len(list(set(tokenized)))
    return numwords


def grab_numerical(text):
    """Takes in text, extracts numerical data and returns it as integer
        Set it as 0 if nothing found
    """
    number = 0
    
    try:
        text = u''.join(re.findall('\\d+', text))
        number = int(text)
    except:
        pass
    
    return number

def calculate_scores(synset):
    """Takes in a synset and returns an abstraction score based on the closure name of hypernym synsets
    ###TODO### may be missing some closures
    """
    hyper = lambda x: x.hypernyms()
    
    #both a_score and c_score are set to one to prevent the cannot divide by 0 error
    a_score = 1
    c_score = 1
    
    for closure in synset.closure(hyper):
        #print closure.name()
        if closure.name().startswith("abstraction"):
            a_score +=1
        if closure.name().startswith("physical"):
            c_score +=1
    return float(a_score)/float(c_score)
    

def abstraction_score(text, uselesk = False):
    """Takes in a list of sentences, tags the parts of speech from the word tokenized sentence,
    looks for part of speech beginning with N (a type of noun) returns the mean abstraction score by 
    calling calculate_scores.
    
    Optional, uses the default lesk algorithm from NLTK
    """
    nouns = []
    
    for sent in text:
        nouns.append([token for token, pos in pos_tag(word_tokenize(sent)) if pos.startswith('N')])

    #print nouns
    nouns = [item for sublist in nouns for item in sublist]
    
    scores=[]
    for i in nouns:
        if uselesk:
            y = lesk(sent, i)
            if y is not None:
                #print y.definition()
                scores.append(calculate_scores(y))
        else:
            synsets = wn.synsets(i, "n")
            for synset in synsets:
                #print synset
                scores.append(calculate_scores(synset))
    return np.mean(scores)


def pronoun_score(text):
    """Returns number of distinct pronouns"""
    pronouns = []
    list_words = ['i','me','my','you','we','us','myself', 'ourself','ourselves','yourselves']
    for sent in text:
        pronouns.append([token for token, pos in pos_tag(word_tokenize(sent))if pos.startswith('PRP')])
#         print nouns
    pronouns = [item for sublist in pronouns for item in sublist]
    imp_words = set(pronouns).intersection(list_words)
    return float(len(imp_words))