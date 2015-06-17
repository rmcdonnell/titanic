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

col_list = train_df.drop(['PassengerId','Survived','Pclass','Name','Sex',\
                          'Age','Ticket','Fare','Cabin','Embarked'], axis=1)
train_df['Family'] = col_list.sum(axis=1)

mf_set = {'female': 0, 'male': 1}
train_df['Gender'] = train_df['Sex'].map( mf_set ).astype(int)

median_age = train_df['Age'].dropna().median()
if len(train_df.Age[ train_df.Age.isnull() ]) > 0:
    train_df.loc[ (train_df.Age.isnull()), 'Age'] = median_age
#train_df['AgeRange'] = train_df['Age']//5*5
train_df['AgeRange'] = pd.Series(train_df['Age']//5*5, index=train_df['PassengerId'])

print list(train_df.columns.values)
# Pclass
print 'Age'
train_df['AgeRange'].hist()
P.show()

print 'Pclass'
train_df['Pclass'].hist()
P.show()

print 'Family'
train_df['Family'].hist()
P.show()

#print 'Parch'
#train_df['Parch'].hist()
#P.show()

print 'Gender'
train_df['Gender'].hist()
P.show()

print 'Fare'
train_df['Fare'].hist()
P.show()

test_df = pd.read_csv('data/test.csv', header=0)
#['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 
#'Ticket', 'Fare', 'Cabin', 'Embarked']

col_list = train_df.drop(['PassengerId','Pclass','Name','Sex','Age','Ticket',\
                          'Fare','Cabin','Embarked'], axis=1)
train_df['Family'] = col_list.sum(axis=1)

mf_set = {'female': 0, 'male': 1}
train_df['Gender'] = train_df['Sex'].map( mf_set ).astype(int)

median_age = test_df['Age'].dropna().median()
if len(test_df.Age[ test_df.Age.isnull() ]) > 0:
    test_df.loc[ (test_df.Age.isnull()), 'Age'] = median_age
test_df['AgeRange'] = pd.Series(test_df['Age']//5*5, index=test_df['PassengerId'])

ids = test_df['PassengerId'].values

train_df =    train_df.drop(['PassengerId', 'Name', 'Sex', 'Ticket', 'Cabin', \
                             'Embarked', 'Age'], axis=1)
test_df =     test_df.drop( ['PassengerId', 'Name', 'Sex', 'Ticket', 'Cabin', \
                             'Embarked', 'Age'], axis=1)
print pd.isnull(train_df['AgeRange']).sum()
#print test_df['AgeRange'].get_dtype_counts()
train_df['AgeRange'][-0].replace([np.inf, -np.inf, np.nan], 0)
print pd.isnull(train_df['AgeRange']).sum()
#test_df['AgeRange'].replace([np.inf, -np.inf], 0)

#train_data = train_df.values
#test_data = test_df.values
#
#print 'Training...'
#forest = RandomForestClassifier(n_estimators=100)
#forest = forest.fit( train_data[0::,1::], train_data[0::,0] )
#
#print 'Predicting...'
#output = forest.predict(test_data).astype(int)
#
#predictions_file = open("results/myfirstforest.csv", "wb")
#open_file_object = csv.writer(predictions_file)
#open_file_object.writerow(["PassengerId","Survived"])
#open_file_object.writerows(zip(ids, output))
#predictions_file.close()
#print 'Done.'