"""
BobbyMcD did most of this. I'm adding grid search for parameter optimization.
"""
import time
import csv
from operator import itemgetter
from scipy.stats import randint as sp_randint
import numpy as np
import pandas as pd

from sklearn.grid_search import GridSearchCV, RandomizedSearchCV
from sklearn.datasets import load_digits
from sklearn.ensemble import RandomForestClassifier


#Creates a Family column which is the sum of siblings, spouces, parents and 
#children aboard who are related to the individual.
def Family( input_data):
    input_data[ 'Family' ] = input_data[ 'SibSp' ] + input_data[ 'Parch' ]

#Creates an AgeRange column which is a rounded off age value based on VALUE.
def AgeRange( input_data):
    VALUE = 5
    median_age = input_data[ 'Age' ].dropna().median()
    if len( input_data.Age[ input_data.Age.isnull() ]) > 0:
        input_data.loc[ input_data.Age.isnull(), 'Age'] = median_age
    input_data[ 'AgeRange' ] = ( input_data[ 'Age' ] % VALUE) * VALUE

#Creates a Gender column which indicates 1 for male and 0 for female.
def Gender( input_data):
    mf_set = {'female': 0, 'male': 1}
    input_data[ 'Gender' ] = input_data[ 'Sex' ].map( mf_set ).astype(int)

#Creates a AdjFare column which makes the float fare into an integer
def AdjFare( input_data):
    input_data[ 'AdjFare' ] = input_data[ 'Fare' ]*100
    input_data[ 'AdjFare' ].fillna(0).astype(int)

#Converts the Embarked column into an integer
def Embarking( input_data):
    embark_set = {}
    for something in input_data:
        element_count = 1
        if embark_set.has_key( something):
            pass
        else:
            embark_set[ something ] = element_count
            element_count += 1
    input_data[ 'ComingFrom' ] = input_data[ 'Embarked' ].map( embark_set )
    input_data[ 'ComingFrom' ].fillna(0).astype(int)

# Load the data

#Read the data sets
train_df = pd.read_csv( 'data/train.csv', header=0)
test_df  = pd.read_csv( 'data/test.csv',  header=0)

ids     = test_df['PassengerId'].values
X_train = train_df.ix[:,'Pclass':]
X_test  = test_df.ix[:,'Pclass':]
y_train = train_df['Survived']
y_test  = None


# Grid search stuff

# specify parameters and distributions to sample from
param_dist = {"max_depth": [3, None],
#              "max_features": sp_randint(1, 11),
              "min_samples_split": sp_randint(1, 11),
              "min_samples_leaf": sp_randint(1, 11),
              "bootstrap": [True, False],
              "criterion": ["gini", "entropy"]}

#Adds the specified columns to the data sets
Family(    X_train)    ;   Family(    X_test)
AgeRange(  X_train)    ;   AgeRange(  X_test)
Gender(    X_train)    ;   Gender(    X_test)
AdjFare(   X_train)    ;   AdjFare(   X_test)
Embarking( X_train)    ;   Embarking( X_test)

#Remove the unused columns, the commented out columns are included in the data
col_to_remove = [
#                'PassengerId',
#                'Survived',
#                'Pclass',
                'Name',
                'Sex',
                'Age',
                'SibSp',
                'Parch',
                'Ticket',
                'Fare',
                'Cabin',
                'Embarked',
#                'Gender',
#                'AgeRange',
#                'Family',
#                'AdjFare',
#                'ComingFrom',
                 ]

X_train =    X_train.drop( col_to_remove, axis=1).fillna(0)
X_test  =    X_test.drop(  col_to_remove, axis=1).fillna(0)

print "\nThe following columns of the data set were used in the analysis:"
print "\t'" + "',  '".join( X_test.columns.values) + "'"

# get some data
iris = load_digits()
X, y = iris.data, iris.target
print len( X[0]), y
# build a classifier
clf = RandomForestClassifier(n_estimators=20)


# Utility function to report best scores
def report(grid_scores, n_top=3):
    top_scores = sorted(grid_scores, key=itemgetter(1), reverse=True)[:n_top]
    for i, score in enumerate(top_scores):
        print("Model with rank: {0}".format(i + 1))
        print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
              score.mean_validation_score,
              np.std(score.cv_validation_scores)))
        print("Parameters: {0}".format(score.parameters))
        print("")


# specify parameters and distributions to sample from
param_dist = {"max_depth": [3, None],
              "max_features": sp_randint(1, 11),
              "min_samples_split": sp_randint(1, 11),
              "min_samples_leaf": sp_randint(1, 11),
              "bootstrap": [True, False],
              "criterion": ["gini", "entropy"]}

# run randomized search
n_iter_search = 20
random_search = RandomizedSearchCV(clf, param_distributions=param_dist,
                                   n_iter=n_iter_search)

start = time()
random_search.fit(X, y)
print("RandomizedSearchCV took %.2f seconds for %d candidates"
      " parameter settings." % ((time() - start), n_iter_search))
report(random_search.grid_scores_)

# use a full grid over all parameters
param_grid = {"max_depth": [3, None],
              "max_features": [1, 3, 10],
              "min_samples_split": [1, 3, 10],
              "min_samples_leaf": [1, 3, 10],
              "bootstrap": [True, False],
              "criterion": ["gini", "entropy"]}

# run grid search
grid_search = GridSearchCV(clf, param_grid=param_grid)
start = time()
grid_search.fit(X, y)

print("GridSearchCV took %.2f seconds for %d candidate parameter settings."
      % (time() - start, len(grid_search.grid_scores_)))
report(grid_search.grid_scores_)
#
#print 'Training...'
#forest = RandomForestClassifier( n_estimators=100)
#
#print 'Randomized search'
#n_iter_search = 20
##random_search = RandomizedSearchCV(estimator            = forest, 
##                                   param_distributions  = param_dist,
##                                   n_iter               = n_iter_search)
##newstuff = random_search.fit( X_train.values, y=y_train.values)
#a = 0.0#newstuff.score( X_train.values, y=y_train.values)
#b = 0.0
#while a >= b:
#    n_iter_search += 2
#    b = a
#    random_search = RandomizedSearchCV(estimator            = forest, 
#                                       param_distributions  = param_dist,
#                                       n_iter               = n_iter_search)
#    newstuff = random_search.fit( X_train.values, y=y_train.values)
#    a = newstuff.score( X_train.values, y=y_train.values)
#    print 'a=',a,'b=',b,'n_iter_search=',n_iter_search
#print newstuff.get_params()
#
#print 'Predicting...'
#y_test = newstuff.predict(X_test)
#
#predictions_file = open( "results/20150620_8_prediction_result.csv", "wb")
#open_file_object = csv.writer( predictions_file)
#open_file_object.writerow( [ "PassengerId","Survived" ])
#open_file_object.writerows( zip( ids, y_test))
#predictions_file.close()
#print 'Done.'
