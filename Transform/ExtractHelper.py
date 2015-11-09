import pandas as pd
import numpy as np
import re
# import inflect
from itertools import groupby
from nltk.tokenize import *
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from nltk import word_tokenize, pos_tag, RegexpParser

#fix issue with ascii encoding errors
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

"""DEFINITIONS FOR LABELS"""

Exp = ['Surrealism', 'Symbolists', 'NewYorkSchool', 'ConcretePoetry', 'LanguagePoetry', 'Imagism', 'JazzPoetry', 'BlackMountain', 'ConceptualPoetry']
Contemp = ['Contemporary', 'Objectivists']
Modern = ['Modernism', 'Beat', 'SanFranciscoRenaissance', 'HarlemRenaissance', 'BlackArts', 'DarkRoomCollective', 'ConfessionalPoetry', 'Slam/SpokenWord']
Trad =['Formalism', 'NewFormalism', 'FiresidePoet']


def labler(text):
    """input primary tags and outputs labels as defined in script"""
    t = []
    t.append(str(text))
#     print t
    label = 0
#     if len(set(t).intersection(Exp))>0:
#         label = 0
    if len(set(t).intersection(Contemp))>0:
        label = 1
#     if len(set(t).intersection(Modern))>0:
#         label = 'Modern'
#     if len(set(t).intersection(Trad))>0:
#         label = 'Trad'
    return label

"""RegexpParser pattern definitions"""

#noun phrase patterns
npatterns = """
    NP: {<JJ.*>*<NN.*><CC>*<NN.*>+}
    {<NN.*><IN>*<NN.*>+}
    {<JJ.*>*<NN.*>+}
    """
#verb phrase patterns
vpatterns = """
    VP: {<VB.*>+<DT|IN>*<JJ.*>*<NN.*>+<R.*>*}
    {<VB.*><VB.*>*}
    """
#adjective phrase patterns
apatterns = """
    AP: {<RB.*><JJ.*><IN><NN.*>+}
    {<JJ.*><IN><NN.*>}
    {<RB.*><JJ.*>}
    {<JJ.*>+}
    """

NPChunker = RegexpParser(npatterns)
VPChunker = RegexpParser(vpatterns)
APChunker = RegexpParser(apatterns)


def unpack_dictionary(df, column, fillna = None):
    """for dealing with dataframe with dictionary in it's column"""
    df = df.reset_index(drop=True)

    ret = None

    if fillna is None:
        ret = pd.concat([df, pd.DataFrame((d for idx, d in df[column].iteritems()))], axis=1)
        del ret[column]

    else:
        ret = pd.concat([df, pd.DataFrame((d for idx, d in df[column].iteritems())).fillna(fillna)], axis=1)
        del ret[column]

    return ret


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


def naive_enj_score(text):
    """Takes in a list of strings or strings and returns the average number of 
    lines each sentence will contain
    """
    nlines = []
    for t in text:
        t_sent = sent_tokenize(t)
#         print t_sent
        for ts in t_sent:
#             print ts
            nlines.append(countlines(ts))
#     print nlines
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
        # print closure.name()
        if closure.name().startswith("abstraction"):
            a_score +=1
            # print a_score,'abstract',synset
        if closure.name().startswith("physical"):
            c_score +=1
            # print c_score,'concrete', synset
        # print float(a_score)/float(c_score)

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
#         print nouns
    nouns = [item for sublist in nouns for item in sublist]

    scores=[]
    for i in nouns:
        if uselesk:
            y = lesk(sent, i)
            if y is not None:
                #print i, calculate_scores(y)
                scores.append(calculate_scores(y))
        else:
            by_word=[]
            synsets = wn.synsets(i, "n")
            for synset in synsets:
                by_word.append(calculate_scores(synset))

            absword = np.mean(by_word)
            scores.append(absword)
            #print absword
    scores = np.array(scores)
    #print scores
    return scores[~np.isnan(scores)].mean()


def pronoun_score(text):
    """Returns number of distinct pronouns"""
    pronouns = []
    list_words = ['i','me','my','you','we','us','myself', 'ourself','ourselves','yourselves']
    for sent in text:
        pronouns.append([token for token, pos in pos_tag(word_tokenize(sent))if pos.startswith('PRP')])
        # print nouns
    pronouns = [item for sublist in pronouns for item in sublist]
    imp_words = set(pronouns).intersection(list_words)
    return float(len(imp_words))


def prepare_text(input):
    """Takes a list of sentences and returns words that have their parts of speech tagged"""
    tokenized_words = [word_tokenize(sent) for sent in input]
    tagged_words = [pos_tag(word) for word in tokenized_words]
    return tagged_words


def make_tree(tagged_words, typetree = 'nps'):
    """takes POS tagged words and returns word tree"""
    if typetree =='nps':
        word_tree = [NPChunker.parse(word) for word in tagged_words]
    if typetree =='vps':
        word_tree = [VPChunker.parse(word) for word in tagged_words]
    if typetree == 'aps':
        word_tree = [APChunker.parse(word) for word in tagged_words]
    return word_tree


def return_a_list_of_Ps(input, ptype ='nps'):
    """takes list of sentences, calls prepare_text, make_tree; parses it returns set of unique phrases 
    depending on the phrase type
    """
    ps = []  # an empty list in which to phrases will be stored.
    t_words = prepare_text(input)
    p_tree = make_tree(t_words, ptype)
#     print p_tree
    for sent in p_tree:
        if ptype =='nps':
            tree = NPChunker.parse(sent)
        if ptype =='vps':
            tree = VPChunker.parse(sent)
        if ptype =='aps':
            tree = APChunker.parse(sent)

        for subtree in tree.subtrees():
            if subtree.label() == ptype.upper()[:2]:
                t = subtree
                t = ' '.join(word for word, tag in t.leaves())
                ps.append(t)
    return list(set(ps))


def p_ratio(text, ptype = 'nps'):
    """takes a list of sentences, returns the ratio of the specific type of phrase over 
    total number of unique phrases
    """
    return_ratio = 0.0
    np = len(return_a_list_of_Ps(text))
    ap = len(return_a_list_of_Ps(text,'aps'))
    vp = len(return_a_list_of_Ps(text,'vps'))
    total_p = np+ap+vp
    if total_p > 0:
        if ptype == 'nps':
            return_ratio = np/float(total_p)
        if ptype == 'aps':
            return_ratio = ap/float(total_p)
        if ptype == 'vps':
            return_ratio = vp/float(total_p)
    return return_ratio


def average_phrasal_complexity(text, ptype = 'nps'):
    """takes a list of sentences, returns the average of lengths of each phrase type"""
    lengths_p = []
    phrases = return_a_list_of_Ps(text, ptype)
#     print phrases
    for p in phrases:
        lengths_p.append(len(word_tokenize(p)))
#     print lengths_p
    lengths_p = np.array(lengths_p)
    complexity_score = lengths_p.mean()
    return complexity_score


def phrasal_freq(text, ptype = 'nps'):
    """returns list of frequency by number of ptype phrases"""
    phrase_freq = []
    lengths_p = []
    phrases = return_a_list_of_Ps(text, ptype)
    for p in phrases:
        lengths_p.append(len(word_tokenize(p)))

    lengths_p = sorted(lengths_p, key=int)
    freqs = [len(list(group)) for key, group in groupby(lengths_p)]
    freq_r = []

    for f in freqs:
        freq_r.append(f/float(len(lengths_p)))

    l_ps = sorted(list(set(lengths_p)))
#     print l_ps

    keynames = []

    m = len(l_ps)

    start = 0
    while start < m:
#         print start
        n = l_ps[start]
#         print n
#         print word
        colname = str(n)+ 'w_'+ptype+'_fr'
        keynames.append(colname)
        start += 1

    dictionary = dict(zip(keynames, freq_r))

    return dictionary


def conjunction_ratio(input):
    """takes in list of sentences, computes the number of conjunctions& subordinate conjunctions
    divided by the number of sentences
    """
    conjunct_ratio = 0.0
    tag_w = prepare_text(input)
    num_sent = float(len(tag_w))
    tag_w = [item for sublist in tag_w for item in sublist]
    conjunctions = len(list(filter(lambda x: x[1] == 'CC' or x[1] == 'IN', tag_w)))
#     print conjunctions, num_sent
    if num_sent > 0:
        conjunct_ratio = conjunctions/num_sent
        
    return conjunct_ratio


