## An Analysis of Contemporary American Poetry Using K means Clustering & NLTK

### Specific Aim

For this project I applied Natural Language Processing methods to break down the corpus of Contemporary American Poems as scraped from the Academy of American Poets website into numerical representations of the text in terms of style.

Then I used an unsupervised learning method, K-means clustering, to see if these poems would naturally cluster into groups that may or may not represent meaningful stylistic differences.

###Design
*please note that this is a work in progress and I may make a ton of changes*

**please check out the Final Project powerpoint presentation for quick overview of process**

####Libraries Used
* Scrapy
* Pymongo
* Pandas
* Numpy
* SciKit Learn
* NLTK
* Seaborn

####Data Storage
* Mongodb

###Steps to Reproduce

1 Extract From Academy of American Poets Website using Scrapy project
* Currently the project is set to pipe to Mongo database however, to output to json or other format, please change the configurations in settings.py
* Go to Extract/poetryorg directory and run from terminal $ scrapy crawl poetryspider

2 Optional: Store in Mongo Database with two collections: Poets & Poems

3 Go to Transform directory and run Ipython notebooks PoetDataProcessing then PoemDataProcessing (PoemDataProcessing can take up to 3 hours)

4 Make sure you have ExtractHelper.py in the directory as it contains all the helper methods (docstrings available) needed to extract feature variables

5 Go to Analysis directory and run ipython notebook Feature Selection

6 Run ipython notebook Kmeans

7 Run ipython notebook Kmeans\_with\_scaled

###About the Raw Data

* 1,467 poems were scraped from twenty 21st century poetic movements and represent the works of 349 poets published between 1900 and 2015

* There were many different ways of obtaining this data using Scrapy but I chose to scrape only the works from poets that were tagged to a specific movement

* I also scraped the biographical and geographical (if any) information from the poets because why not? Perhaps something could be done with that information if not now, then later

* Some poets and their works had additional movement tags

###Feature Variables Defined Below

* Average line per stanza - the average number of lines that a stanza has within a poem
* Enjambent Score – this is the total number of line breaks within each sentence divided by the total number of sentences in the poem
* Type Token Ratio – number of distinct words over the total number of word
* Abstraction Score - a score representing the abstractness of the poem. It is calculated by 1) tokenizing each sentence into words, 2) using nltk’s parts of speech tagger to label each word, 3) taking each noun tagged word and looking up the noun synsets available in wordnet (nltk) 4) because each noun has multiple senses, I take the total number of abstract senses and divide it against the total number of concrete senses in order calculate how abstract the noun is 5) all the abstraction scores for all the nouns are averaged.
* Lesk Abstraction Score – a score representing the abstractness of the poem in the same way as the abstraction\_score is calculated with the exception being that I am using nltk’s lesk algorithm to calculate the best sense of the noun in its sentence then using that sense to look at how abstract that is, and the score is for all the nouns averaged
* Title Lesk Abstraction Score – same as above except for just the title
* Pronoun Score - this is the distinct number of pronoun occurrences referring to the subject or reader divided by the total number of sentences in the poem
* Conjunction Score - this is the number of conjunctions and subordinate conjunctions found in the poem divided by the total number of sentences
* Noun, Verb, and Adjective Phrase Ratio - this is ratio of the noun, verb, or adjective phrases over the total number of noun, verb, and adjective phrases found in the text
* Average Noun, Verb, and Adjective Phrase Complexity Score - I define a phrase as complex when it contains more than one word. This is divided by the total number of phrases within each poem.
* 1 word, 2 word, and 3 word noun phrase frequency ratio - these variables stand for the frequency of 1, 2, or 3 word noun phrases within each poem

###Ousted Variables:
* wordcount - the total number of words that a poem has
* wordcount\_d - the distinct number of words that a poem has
* numlines - the number of lines that a poem text has
* numstanzas - the number of stanzas that a poem text has
* yrpub - the year the poem was published, two poems were missing the yr published so I just got rid of them
* num\_sentences - the number of sentences that a poem has
