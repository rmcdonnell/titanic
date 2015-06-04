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



# 'PassengerId', 'Survived', 'Pclass', 'Name','Sex', 'Age', 'SibSp', 'Parch',
# 'Ticket', 'Fare', 'Cabin', 'Embarked', 'AgeRange', 'FamilyCount'  

############## New Model

# Imported Packages
import csv as csv

# Methods
def age_range(input, interval):
    input =     input[Age]
    if input.isdigit():
        #age =   int(input)
        input = int(input)/interval * interval
        return  input
    else:       return 'AgeRange'

def family_count(input):
    if input[SibSp].isdigit():
        if input[Parch].isdigit():
            temp = int( input[SibSp]) + int(input[ Parch])
            return str( temp)
    else: return 'FamilyCount'

# Variables
data = []
survival_set = []
output_data = []
survived_dict = {}
not_survived_dict = {}
eval_survival_dict = {}

# Create a csv_file_object to be read into a list of lists (2D matrix), data.
csv_file_object = csv.reader(open('train.csv', 'rb'))
for row in csv_file_object:
    data.append(row)

# Below is s list of the variable column positions for convenience.
number_on_board = float( len( data)-1)
PassengerId = data[0].index('PassengerId') # An int which id's the passenger
Survived    = data[0].index('Survived')    # (0 = No; 1 = Yes)
Pclass      = data[0].index('Pclass')      # (1 = 1st; 2 = 2nd; 3 = 3rd)
Name        = data[0].index('Name')        # String, name of passenger
Sex         = data[0].index('Sex')         # String, male or female
Age         = data[0].index('Age')         # An int for the passenger's age
SibSp       = data[0].index('SibSp')       # Number of Siblings/Spouses Aboard
Parch       = data[0].index('Parch')       # Number of Parents/Children Aboard
Ticket      = data[0].index('Ticket')      # Ticket Number
Fare        = data[0].index('Fare')        # Passenger Fare ($)
Cabin       = data[0].index('Cabin')       # Cabin
Embarked    = data[0].index('Embarked')    # (C = Cherbourg; Q = Queenstown; 
                                           #  S = Southampton)

# altering
interval = 30
for row in data:
    if row[Age].isdigit():
        row.append( int(row[Age])/interval * interval)
    else: row.append( 'AgeRange')
    if row[SibSp].isdigit():
        if row[Parch].isdigit():
            temp = int( row[SibSp]) + int(row[ Parch])
            row.append( str( temp))
        else: pass
    else: row.append( 'FamilyCount')
    if row[ Survived ].isdigit():
        row[ Survived ] =  bool( int( row[ Survived ]))
    
    
AgeRange    = data[ 0 ].index( 'AgeRange' )
FamilyCount = data[ 0 ].index( 'FamilyCount' )

hash_variables = [Sex, AgeRange, FamilyCount]

for rows in data:
    temp = []
    has_not_died = rows[Survived]
    for element in hash_variables:
        temp.append(rows[element])
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

percent_error =  int(hash_fail/float(len(data))*1000)/10.0
print "Can't categorize", percent_error, '% of entries'

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
        effectiveness += int(test)
        
print "Effectiveness:",int(effectiveness/float(len(data))*1000)/10.0,"%"
y = []
for x in hash_variables: 
    y.append( data[0][x])
print y
    
    