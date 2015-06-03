""" Explain stuff...
Author : BobbyMcD
Date : 30 May 2015
"""
#VARIABLE DESCRIPTIONS:
#survival        Survival
#                (0 = No; 1 = Yes)
#pclass          Passenger Class
#                (1 = 1st; 2 = 2nd; 3 = 3rd)
#name            Name
#sex             Sex
#age             Age
#sibsp           Number of Siblings/Spouses Aboard
#parch           Number of Parents/Children Aboard
#ticket          Ticket Number
#fare            Passenger Fare
#cabin           Cabin
#embarked        Port of Embarkation
#                (C = Cherbourg; Q = Queenstown; S = Southampton)



############## New Model

import csv as csv
#import numpy as np

def age_range(input):
    input = input[Age]
    if input.isdigit():
        input =  int( int( input)/10.0)*10
        if input == 80 or input >= 90:  return 'Elderly'
        if input == 60 or input == 70:  return 'Senior'
        if input == 40 or input == 50:  return 'Adult'
        if input == 20 or input == 30:  return 'Youth'
        if input == 0  or input == 10:  return 'Child'
    else:                               return 'AgeRange'

def family_count(input):
    if input[SibSp].isdigit():
        if input[Parch].isdigit():
            temp = int( input[SibSp]) + int(input[ Parch])
            return str( temp)
    else: return 'FamilyCount'
    
csv_file_object = csv.reader(open('train.csv', 'rb'))

data=[]
survival_set = []
titanic_class = ('1', '2', '3')
titanic_sex = ('male', 'female')
titanic_age = ('Elderly','Senior','Adult','Youth','Child')
survived_dict = {}
not_survived_dict = {}

for row in csv_file_object:
    data.append(row)
    
number_on_board = float( len( data)-1)
PassengerId = data[0].index('PassengerId')  ###
Survived    = data[0].index('Survived')
Pclass      = data[0].index('Pclass')
Name        = data[0].index('Name')         ###
Sex         = data[0].index('Sex')
Age         = data[0].index('Age')
SibSp       = data[0].index('SibSp')
Parch       = data[0].index('Parch')
Ticket      = data[0].index('Ticket')       ###
Fare        = data[0].index('Fare')         ###
Cabin       = data[0].index('Cabin')        ###
Embarked    = data[0].index('Embarked')     ###
    
for row in range( len( data)):
    if data[row][Survived] == '1':  data[row][Survived] = True
    if data[row][Survived] == '0':  data[row][Survived] = False
    data[row].append( age_range( data[row]))
    data[row].append( family_count( data[row]))
AgeRange    = data[0].index('AgeRange')
FamilyCount = data[0].index('FamilyCount')

# 'PassengerId', 'Survived', 'Pclass', 'Name','Sex', 'Age', 'SibSp', 'Parch',
# 'Ticket', 'Fare', 'Cabin', 'Embarked', 'AgeRange', 'FamilyCount'  
hash_variables = ['Survived', 'Pclass','Sex', 'AgeRange', 'FamilyCount' ]
v = []


new_hash = {}
for s in hash_variables:
    if s not in new_hash:
        new_hash.setdefault(s,0)

print new_hash.items()
