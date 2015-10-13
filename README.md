Final Project
=============

Contemporary American Poetry (post war to today)

 

*This repository contains all the files including terrible notes and slow
learning*

*Repository \@*https://github.com/huiruru/FinalProject

 

Analysis Plan

 

**Specific Aim**

    1.  Data Sources

        -   Primary source:

            -   Poet information & poems scraped from the Academy of American
                Poets website (https://www.poets.org)

        -   Supplementary source:

            -   Poet information & poems scraped from Poetry Foundation
                (http://www.poetryfoundation.org)

    2.  N (Sample Size)

        -   \~1450 poems from 349 poets (poets.org), 20 movement/styles of poems

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Contemporary                 202
Modernism                     15
Formalism                     14
Language Poetry               13
Surrealism                    12
Confessional Poetry           11
New York School               11
Beat                          11
Black Arts                     9
Symbolists                     8
Jazz Poetry                    7
Harlem Renaissance             7
Conceptual Poetry              6
Objectivists                   6
Black Mountain                 4
Dark Room Collective           4
Concrete Poetry                3
San Francisco Renaissance      3
Slam/Spoken Word               2
New Formalism                  1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    -   \~ 200 poems from \~100 poets (poetryfoundation.org), supplements some
        of the movement/styles we are lacking in data for in the primary source.

    -   Time Period (of data): Poems published between WWII and now

    -   1o Hypothesis: unsupervised learning on the poems to look for patterns
        associated with the movement/classification

    -   Secondary Hypothesis: it is possible to predict the poetic style or
        movement it has been classified/tagged with.

     

**Methods**

1.  Outcome:

        -   By running unsupervised learning on the poem texts, we can decide
            whether to go ahead with the secondary hypothesis

2.  Predictors/Covar:

        -   Poet age

        -   If poet is dead

        -   Year published

        -   Poet’s geographical location: city, state, etc.

        -   Type Token ratio

        -   Alliteration: use nltk.corpus.cmudict to look at sounds

        -   Concrete object words = total number of concrete nouns/total number
            of abstract nouns

        -   Abstract concept words = total number of abstract nouns/the number
            of concrete nouns

        -   Avg named entities - e.g. foreign countries

        -   Length (number of lines), avg \# of words

        -   ? reference to subject (prounoun: I)

        -   Visual, sense adjectives/descriptions

        -   Political nature of text

3.  Algorithms:

    -   K means Cluster for unsupervised learning to see if 1o hyp., if 1o hyp
        then either logistic regression or naive bayes

     

**Result**

    That there are distinctions between groups of poems that align with the
    particular movement/poetic style

1.  Limitations/Assumptions of my data:

    -   2000 poems is not a large dataset, I am severely limited by the data I
        use. The data also needs to be cleaned up and is error prone.

    -   The most recent classification as agreed upon by "institutional" players
        actually represents the universe of contemporary American poetry
        accurately.

2.  Expected Hurdles

    -   Figuring out how to group movement/styles (due to lack of data)

    -   Dirty data, bad calculations

3.  Where I need help

    -   NLTK

    -   Linguistics

4.  Going to have to repeat all steps for secondary hypothesis

 

**Design**

Libraries

1.  Webscraping:

    -   scrapy, BeautifulSoup (for secondary source - javascript pages, scrapy
        not working)

2.  Data retrieval, storage:

    -   pymongo - Mongodb db

3.  Text:

    -   NLTK

    -   Alchemy API

    -   Conceptnet

    -   maybe doc2vec

 
