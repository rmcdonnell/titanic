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

def age_range(input, interval):
    input = input[Age]
    if input.isdigit():
        age = int(input)
        input =  (age/interval)*interval
        return input
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
survived_dict = {}
not_survived_dict = {}
eval_survival_dict = {}
interval = 20

for row in csv_file_object:
    data.append(row)

# 'PassengerId', 'Survived', 'Pclass', 'Name','Sex', 'Age', 'SibSp', 'Parch',
# 'Ticket', 'Fare', 'Cabin', 'Embarked', 'AgeRange', 'FamilyCount'  
    
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
    if data[row][Survived] == '1':  
        data[row][Survived] = True
    if data[row][Survived] == '0':  
        data[row][Survived] = False
    age = age_range( data[row], interval = 30)
    data[row].append( age)
    data[row].append( family_count( data[row]))
AgeRange    = data[0].index('AgeRange')
FamilyCount = data[0].index('FamilyCount')

hash_variables = [Sex, AgeRange, FamilyCount]
# [Pclass, Sex, AgeRange, FamilyCount]

for rows in data:
    temp = []
    for element in hash_variables:
        temp.append(rows[element])
    has_not_died = rows[Survived]
    temp = tuple(temp)
    if has_not_died:
        if survived_dict.has_key(temp):
            survived_dict[temp] += 1
        else:
            survived_dict[temp] = 1
    if not has_not_died:
        if not_survived_dict.has_key(temp):
            not_survived_dict[temp] += 1
        else:
            not_survived_dict[temp] = 1
    
hash_count = len( not_survived_dict.keys())
hash_fail = 0
for hashes in survived_dict.keys():
    if not_survived_dict.has_key(hashes):
        temp = cmp(survived_dict[hashes], not_survived_dict[hashes])
        eval_survival_dict[hashes] = temp
        hash_count -= 1
    else:
        eval_survival_dict[hashes] = 0
for hashes in not_survived_dict.keys():
    if not eval_survival_dict.has_key(hashes):
        eval_survival_dict[hashes] = 0
        hash_count -= 1

for h,i in eval_survival_dict.items():
    if i == 0:
        hash_fail += 1
        del eval_survival_dict[h]
    if i == 1:
        eval_survival_dict[h] = True
    if i == -1:
        eval_survival_dict[h] = False
#print eval_survival_dict
print "Can't categorize", int(hash_fail/float(len(data))*1000)/10.0,'% of entries'
#print len( )
output_data = []
effectiveness = 0.0
for index in data:
    output_data.append(PassengerId)
    has_not_died = index[Survived]
    temp = []
    for element in hash_variables:
        temp.append(index[element])
    temp = tuple(temp)
    if eval_survival_dict.has_key(temp):
        test = has_not_died == eval_survival_dict[temp]
        #print test
        effectiveness += int(test)
        
print "Effectiveness:",int(effectiveness/float(len(data))*1000)/10.0,"%"
y = []
for x in hash_variables: 
    y.append( data[0][x])
print y
    
    