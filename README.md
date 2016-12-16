# IndProject
Independent Project for Bio331


## Data
The data is an updated version of the data used in Weber et. al. (2013). This data was requested by Anna Ritz in the early fall of 2016.The data is held in two files BadgerInfo.txt and BadgerMatrix.txt.

* __BadgerInfo.txt__.  This contains demographic information about the badgers in in the study.  It contains four columns: badger name, sex,whether or not they are infected with tuberculosis, and the social group the badger is a part of.

* __BadgerMatrix.txt__.  This contains the interaction data of the badgers.  This matrix is constructed as usual with each cell being the interaction between the row and column badger.  The number in the cell denotes the amount of time (minutes/seconds?) that the two badgers were in close contact

## Code
The code is contained in badger.py and graphing.py.

*__badger.py__ This contains the import code for finding flow betweenness, the Girvan-Newman method.  Most of the other functions are helper functions for those three functions.  

*__graphing.py__ This has some examples for using and graphing the data on GraphSpace none of the important information.

*__hw5.py__ This has some the code for k-center clustering it was used for only for comparing clusters

##Other files

Any file ending in .json is used for graphing the networs on GraphSpace they don't have any other purpose.  There are some toy graph stuff


Nicola Weber, Stephen P Carter, Sasha RX Dall, Richard J Delahay, Jennifer L McDonald, Stuart Bearhop, and Robbie A McDonald. Badger social networks correlate with tuberculosis infection. Current Biology, 23(20):R915–R916, 2013.
