"""
Created on Mon Jun  8 13:46:10 2015

This is my analysis of the titanic dataset which was bestowed uppon me via a
Kaggle competition. I used a forest to predict who lives or dies using the 
specified parameters. I also used a 'functional' aproach to the addition of 
columns to the initial data set (as seen below).

@author: BobbyMcD
"""

import pandas as pd
import csv as csv
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
    input_data['AdjFare'] = input_data['Fare']*100

#Read the data sets
train_df = pd.read_csv( 'data/train.csv', header=0)
test_df = pd.read_csv(  'data/test.csv',  header=0)

#Adds the specified columns to the data sets
Family(   train_df)    ;   Family(   test_df)
AgeRange( train_df)    ;   AgeRange( test_df)
Gender(   train_df)    ;   Gender(   test_df)
AdjFare(  train_df)    ;   AdjFare(  test_df)

col_to_remove = [
                'PassengerId',
#                'Survived',
                'Pclass',
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
                 ]

ids      =    test_df[ 'PassengerId' ].values
train_df =    train_df.drop( col_to_remove, axis=1)
test_df  =    test_df.drop(  col_to_remove, axis=1)

print "\nThe following columns of the data set were used in the analysis:"
print "\t'"+"',  '".join( test_df.columns.values)

train_data = train_df.values.astype( int)
test_data  = test_df.values.astype(  int)

print 'Training...'
forest = RandomForestClassifier( n_estimators=100)
forest = forest.fit( train_data[ 0::,1:: ], train_data[ 0::,0 ])

print 'Predicting...'
output = forest.predict( test_data)
output = output.astype( int)

predictions_file = open( "results/myAnalysisOfTitanicDS.csv", "wb")
open_file_object = csv.writer( predictions_file)
open_file_object.writerow( [ "PassengerId","Survived" ])
open_file_object.writerows( zip( ids, output))
predictions_file.close()
print 'Done.'