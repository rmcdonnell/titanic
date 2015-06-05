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
PassengerId = data[0].index('PassengerId')  # An int which id's the passenger
Survived    = data[0].index('Survived')     # (0 = No; 1 = Yes)
Pclass      = data[0].index('Pclass')       # (1 = 1st; 2 = 2nd; 3 = 3rd)
Name        = data[0].index('Name')         # String, name of passenger
Sex         = data[0].index('Sex')          # String, male or female
Age         = data[0].index('Age')          # An int for the passenger's age
SibSp       = data[0].index('SibSp')        # Number of Siblings/Spouses Aboard
Parch       = data[0].index('Parch')        # Number of Parents/Children Aboard
Ticket      = data[0].index('Ticket')       # Ticket Number
Fare        = data[0].index('Fare')         # Passenger Fare ($)
Cabin       = data[0].index('Cabin')        # Cabin
Embarked    = data[0].index('Embarked')     # (C = Cherbourg; Q = Queenstown; 
                                            #  S = Southampton)
interval = 30       # The interval between age groups 
                    # (i.e. interval = 5 -> [0,5,10,...])
signif = 6
passenger_count = float(len(data))  

# Cleaning the data set.
for row in data:
    if row[ PassengerId].isdigit(): 
        row[ PassengerId] = int( row[ PassengerId])       # PassengerId -> int
        
    if row[ Survived].isdigit():
        row[ Survived] =  bool( int( row[ Survived]))     # Survived -> bool
        
    if row[ Pclass].isdigit():
        row[ Pclass] = int( row[ Pclass])                 # Pclass -> int
        
    if row[ Age].isdigit(): 
        row[ Age] = int( row[ Age])                       # Age -> int
        # Create a new list element, AgeRange, which rounds down Age to the
        # nearest interval value.
        row.append( int( row[ Age])/interval * interval)  # AgeRange -> int
    else: 
        # If Age is not a number, then the string 'AgeRange' is put in its 
        # place. This is to give the column a identifying name.
        row.append( 'AgeRange')
        
    if row[SibSp].isdigit() and row[Parch].isdigit():
        row[ SibSp] = int( row[ SibSp])                   # SibSp -> int
        row[ Parch] = int( row[ Parch])                   # Parch -> int
        # Creates a new list element, FamilyCount, which is the sum of
        # SibSp and Parch.
        temp = row[SibSp] + row[ Parch]
        row.append( str( temp))                           # FamilyCount -> int
#        row[ SibSp] = bool( row[ SibSp])                   # SibSp -> int
#        row[ Parch] = bool( row[ Parch])                   # Parch -> int
    else: 
        # If Age is not a number, then the string 'FamilyCount' is put in its 
        # place. This is to give the column a identifying name.
        row.append( 'FamilyCount')
        
    if row[ Ticket].isdigit():
        row[ Ticket] = int( row[ Ticket])                 # Ticket -> int
    
    # The .isdecimal() operation was giving me trouble, so I made this set of 
    # if/else blocks to assess what kind of number is in row[ Fare].
    if row[ Fare].find('.') !=-1:
        temp = row[ Fare].split( '.')
        row[ Fare] = float( temp[0])                      # Fare -> float
        row[ Fare] += float( temp[1])/10**len( temp[1])
    else:
        if row[ Fare].isdigit():
            row[ Fare] = float( row[ Fare])               # Fare -> float
        else:
            pass
    
AgeRange    = data[ 0].index( 'AgeRange')     # A variable specifying which 
                                              # list element is AgeRange.
FamilyCount = data[ 0].index( 'FamilyCount')  # A variable specifying which 
                                              # list element is FamilyCount.

# A list of the variables being examined in the model.
hash_variables = [ Sex, AgeRange, FamilyCount]

# Prints a list of the names of the variables used in the model.
printable_hash_variable_set = []
for x in hash_variables:  
    printable_hash_variable_set.append( data[ 0][ x])
print '\n',printable_hash_variable_set,'\n'

# Fill both dictionaries, survive_dict and not_survive_dict, with tuples as the
# keys. If has_not_died = True, then a tuple with the components mensioned in
# has_variables is generated as a key. The dictionary is checked to see if the
# key already exists. If the key exists, then the corresponding value is 
# increased by 1, if not, then the key is created and given the default value 
# 1. The value corresponding to each key indicates how many instances of that
# tuple exist in the data set.
for rows in data:
    temp = []
    has_not_died = rows[ Survived]
    for element in hash_variables: 
        temp.append( rows[ element])
    temp = tuple( temp)
    if has_not_died:
        if survived_dict.has_key( temp):
            survived_dict[ temp] += 1
        else:
            survived_dict[ temp] = 1
    if not has_not_died:
        if not_survived_dict.has_key( temp):
            not_survived_dict[ temp] += 1
        else:
            not_survived_dict[ temp] = 1

# Now, we compare the values in survived_dict and the not_survived_dict. If a 
# given key exists in both dictionaries, a new key is created in the 
# eval_survival_dict and is given a value based on how the two key values, from
# their corresponding dictionaries, compare to one another:
# survival_dict[key] > not_survival_dict[key] ->  1
# survival_dict[key] < not_survival_dict[key] -> -1
# survival_dict[key] = not_survival_dict[key] ->  0
test_dict = { 1:True, -1:False , 0:True}    # Used in plase of if/else (or a
                                            #  switch) to given how the 
                                            # dictionaries compare, the boolean
                                            # output specifies if the 
                                            # individual was predicted to lived
                                            # or die.
pct_error = 0.0                             # The percent of keys that exist in 
                                            # one dictionary but not in the 
                                            # other (ie key exists in 
                                            # survival_dict but does not exist
                                            # in not_survival_dict).
increment = int( 1/passenger_count*10**signif)/float( 10**(signif-2)) 
                                            # Rounded percent increment
eval_survival_dict = survived_dict.copy()
eval_survival_dict.update(not_survived_dict)
for hashes in survived_dict.keys():
    try:
        temp = cmp( survived_dict[ hashes], not_survived_dict[ hashes])
    except:
        temp = 0
    if test_dict.has_key( temp):
        eval_survival_dict[ hashes] = test_dict[ temp]
    else:
        pct_error += increment

predicted_data = []
effectiveness = 0.0                 # Initiated model effectiveness variable
fail = 0.0
for index in data:
    new_point = []
    new_point.append( index[ PassengerId])
    has_not_died = index[ Survived]
    temp = []
    for element in hash_variables:
        temp.append( index[ element])
    temp = tuple( temp)
    if isinstance(index[ Survived], str):
        new_point.append( 'Survived')
    else:
        test = has_not_died == eval_survival_dict[ temp]
        new_point.append( int(test))
    if test:
        effectiveness += increment
    output_data.append(new_point)

print "Can't categorize", pct_error, '% of entries\n'
# Can't categorize 1.0089 % of entries

print "Effectiveness:", effectiveness, "%\n"
# Effectiveness: 74.6586 %

print fail,'%'
print fail + effectiveness

with open("mcd_predict_titanic.csv", 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', 
                            quoting=csv.QUOTE_MINIMAL)
    for out_row in output_data:
        spamwriter.writerow(out_row)
    