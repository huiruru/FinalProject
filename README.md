# Final Project
Contemporary American Poetry (post war to today)

*This repository contains all the files including terrible notes and slow learning*

Assumptions:

1. Given a particulat text [scope to be defined], it is possible to predict the poetic style or movement it is classified as, or similar to.
2. The most recent classification as agreed upon by "institutional" players actually presents the universe of Contemporary American Poetry accurately.

To gather and explore these clusters:
* Beat (2)
* Confessional (2)
* New York (2)
* Black Mountain (1)
* Flarf

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
