# Final Project
Contemporary American Poetry (post war to today)

*This repository contains all the files including terrible notes and slow learning*

Analysis Plan:

1. Specific Aim
    Data Source
        poetry.org
        poetryfoundation
    N (Sample Size)
    Time Period (of data)
        Poems published between WWII and now
    1o Hypothesis
        Given a particular poem text, it is possible to predict the poetic style or movement it is classified as.

2. Methods
    Outcome:
        Poem classifications: Confessional vs Black Mountain, New York, Beat, vs Language
    Predictors/Covar:
        Type Token ratio
        Alliteration
        Concrete object words
        Abstract concept words
        NEED dict of Political words
        Psychological words
    Algorithms:
        K means Cluster for unsupervised learning to see if 1o hyp.
        if 1o hyp then either logistic regression or bayes

3. Result
    Given a particular poem text, it is possible to predict the poetic style or movement it is classified as.

4. Limitations/Assumptions of my data
    The most recent classification as agreed upon by "institutional" players actually represents the universe of Contemporary American Poetry accurately.

5. Expected Hurdles
    If 4. fails

6. Where I need help
    NLTK
    Research Linguistics

7. Going to have to repeat 1-6 for secondary hypothesis

Assumptions:

Gather and explore these clusters:
* Beat (2)
  - characterized by its intentional defiance of the literary forms and standard narrative values of previous generations.
  - a means of questioning societal norms, challenging materialism, exploring various types of spirituality and even challenging sexual normatives all in a question to defy and expand consciousness and explore limitless creativity.
* Confessional (2)
  - I
  - Private, subjective experiences
  - attention to prosody": e.g. rhythm, intonation
* New York (2)
  - surrealistic
  - ironic
* Black Mountain (1) aka. projective verse
  - Composition by field" vs. "poetic composition based on received form and measure
  - syntax be shaped by sound rather than sense, with nuances of breath and motion to be conveyed to the reader through typographical means
  - one perception must immediately and directly lead to a further perception
* Language Poetry
  - focus on language, interaction with reader, engaging the reader into the process of producing meaning from the text

### Extra Pastries: 
Poetry Recommender tool

To investigate conceptual trends in American contemporary poetry create graphs/charts from the data. 

----
__Design__

1. scrapy
2. mongodb
3. NLTK
