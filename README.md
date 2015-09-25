# Final Project
Contemporary American Poetry (post war to today)

*This repository contains all the files including terrible notes and slow learning*

Assumptions:

1. Given a particulat text [scope to be defined], it is possible to predict the poetic style or movement it is classified as, or similar to.
2. The most recent classification as agreed upon by "institutional" players actually presents the universe of Contemporary American Poetry accurately.

To gather and explore these clusters:
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

Tables:

Poems - table of unique poems, poem_identifier

PoemAttributes - table of unique poem_identifier, poet_id, computed columns of results from text analysis

PoemTags - table of poems classified and classification (poem_identifier, tag, tag_source)

Poet - table of unique poets, poet_identifier, name, gender, year-born, affiliated_schools, day_jobs, degrees, race/ethnicity etc.
