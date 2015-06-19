# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 13:46:10 2015

@author: bmcdonnell
"""
import pylab as P
import pandas as pd
import numpy as np
import csv as csv
from sklearn.ensemble import RandomForestClassifier

def Family(input_data):
    input_data['Family'] = input_data['SibSp'] + input_data['Parch']
    
def AgeRange(input_data):
    median_age = input_data['Age'].dropna().median()
    if len(input_data.Age[ input_data.Age.isnull() ]) > 0:
        input_data.loc[ (input_data.Age.isnull()), 'Age'] = median_age
    input_data['AgeRange'] = (input_data['Age']%5)*5
    
def Gender(input_data):
    mf_set = {'female': 0, 'male': 1}
    input_data['Gender'] = input_data['Sex'].map( mf_set ).astype(int)
    
def AdjFare(input_data):
    input_data['AdjFare'] = input_data['Fare']*100

train_df = pd.read_csv('data/train.csv', header=0)

test_df = pd.read_csv('data/test.csv', header=0)

Family(train_df)    ;   Family(test_df)
AgeRange(train_df)  ;   AgeRange(test_df)
Gender(train_df)    ;   Gender(test_df)
AdjFare(train_df)   ;   AdjFare(test_df)

ids = test_df['PassengerId'].values
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
answers = train_df['Survived']
train_df =    train_df.drop(col_to_remove, axis=1)
test_df =     test_df.drop( col_to_remove, axis=1)

print "\nThe following columns of the data set were used in the analysis:"
print "\t'"+"',  '".join(test_df.columns.values)

train_data = train_df.values.astype(int)
test_data = test_df.values.astype(int)

print 'Training...'
forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit( train_data[0::,1::], train_data[0::,0] )

print 'Predicting...'
output = forest.predict(test_data)
output = output.astype(int)

predictions_file = open("results/myAnalysisOfTitanicDS.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["PassengerId","Survived"])
open_file_object.writerows(zip(ids, output))
predictions_file.close()
print 'Done.'