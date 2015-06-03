# -*- coding: utf-8 -*-
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

for a in titanic_class:
    for b in titanic_sex:
        for c in titanic_age:
            temp = ' '.join([a,b,c])
            survival_set.append(temp)
            
survived_dict = survived_dict.fromkeys( survival_set, 0)
not_survived_dict = not_survived_dict.fromkeys( survival_set, 0)

items_of_interest = [Pclass, Sex, AgeRange]

for index in range( len( data)):
    if data[index][Survived]:
        i = ' '.join( map(data[index].__getitem__,items_of_interest))
        if survived_dict.has_key(i):
            survived_dict[i] +=1
    if not data[index][Survived]:
        j = ' '.join( map(data[index].__getitem__,items_of_interest))
        if not_survived_dict.has_key(j):
            not_survived_dict[j] +=1
            
print type(survived_dict.keys())
survived_dict.viewitems()
            
survival_set = survived_dict.copy()
count = 0
while (count < len( survived_dict.items())):
   if survived_dict.items()[count][0] == not_survived_dict.items()[count][0]:
       case                  = survived_dict.items()[count][0]
       survived_case         = survived_dict.items()[count][1]
       not_survived_case     = not_survived_dict.items()[count][1]
       if survived_case ==0 and not_survived_case ==0:
           survival_set[case] = None
       else:
           survival_set[case]    = survived_case - not_survived_case
   count += 1
   
for k,v in survival_set.items(): 
    if v == None:
        del survival_set[k]
    if v > 0:
        survival_set[k] = True
    if v < 0:
        survival_set[k] = False

consumed_data = []
for inst in range( len( data)):
    tester = ' '.join( map(data[inst].__getitem__,items_of_interest))
    temp = [data[inst][PassengerId], data[inst][Survived], tester]
    consumed_data.append(temp)
    
accuracy = 0.0
count = 0
for passenger,survival,instance in consumed_data:
    count += 1
    if instance in survival_set:
        if survival_set[instance] == survival:
            accuracy += 1

print "First Model attempt's accuracy:", str(int(accuracy/count*1000)/10.0)+'%'


