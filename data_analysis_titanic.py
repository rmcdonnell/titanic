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

train_df = pd.read_csv('data/train.csv', header=0)
#['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 
# 'Ticket', 'Fare', 'Cabin', 'Embarked']

train_df['Family'] = train_df['SibSp']+train_df['Parch']

mf_set = {'female': 0, 'male': 1}
train_df['Gender'] = train_df['Sex'].map( mf_set ).astype(int)

median_age = train_df['Age'].dropna().median()
if len(train_df.Age[ train_df.Age.isnull() ]) > 0:
    train_df.loc[ (train_df.Age.isnull()), 'Age'] = median_age
train_df['AgeRange'] = (train_df['Age']%5)*5

test_df = pd.read_csv('data/test.csv', header=0)
#['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 
#'Ticket', 'Fare', 'Cabin', 'Embarked']

test_df['Family'] = test_df['SibSp']+test_df['Parch']

mf_set = {'female': 0, 'male': 1}
test_df['Gender'] = test_df['Sex'].map( mf_set ).astype(int)

median_age = test_df['Age'].dropna().median()
if len(test_df.Age[ test_df.Age.isnull() ]) > 0:
    test_df.loc[ (test_df.Age.isnull()), 'Age'] = median_age
test_df['AgeRange'] = (test_df['Age']%5)*5

train_df['Fare*100'] = train_df['Fare']*100
test_df['Fare*100'] = test_df['Fare']*100

ids = test_df['PassengerId'].values

train_df =    train_df.drop(['PassengerId', 'Name', 'Sex', 'Age', 'Ticket', 'Cabin', \
                             'Embarked','Fare'], axis=1)
test_df =     test_df.drop( ['PassengerId', 'Name', 'Sex', 'Age', 'Ticket', 'Cabin', \
                             'Embarked','Fare'], axis=1)
print train_df.columns.values
print test_df.columns.values

train_data = train_df.values.astype(int)
test_data = test_df.values.astype(int)
print train_data.dtype, test_data.dtype
print 'Training...'
forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit( train_data[0::,1::], train_data[0::,0::] )

print 'Predicting...'
output = forest.predict(test_data).astype(int)

predictions_file = open("results/myfirstforest.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["PassengerId","Survived"])
open_file_object.writerows(zip(ids, output))
predictions_file.close()
print 'Done.'