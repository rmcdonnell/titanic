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
test_df = pd.read_csv(  'data/test.csv',  header=0)

X_train = train_df.ix[:,'Pclass':]
X_test = test_df.ix[:,'Pclass':]
y_train = train_df['Survived']
y_test = None


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

ids      =   test_df['PassengerId'].values
X_train =    X_train.drop( col_to_remove, axis=1).fillna(0)
X_test  =    X_test.drop(  col_to_remove, axis=1).fillna(0)

print "\nThe following columns of the data set were used in the analysis:"
print "\t'" + "',  '".join( X_test.columns.values) + "'"

print 'Training...'
forest = RandomForestClassifier( n_estimators=100)

print 'Randomized search'
n_iter_search = 20
random_search = RandomizedSearchCV(estimator            = forest, 
                                   param_distributions  = param_dist,
                                   n_iter               = n_iter_search)
#print dir(random_search)
#print X_train
#random_search.fit(X_test)
forest = random_search.fit( X_train.values, y=y_train.values)

print 'Predicting...'
y_test = forest.predict(X_test)

predictions_file = open( "results/20150620_6_prediction_result.csv", "wb")
open_file_object = csv.writer( predictions_file)
open_file_object.writerow( [ "PassengerId","Survived" ])
open_file_object.writerows( zip( ids, y_test))
predictions_file.close()
print 'Done.'
