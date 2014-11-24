from collections import Counter
import fileinput
import glob
import itertools
import operator
from random import shuffle
import random
import re
import string
from sys import argv
from urllib.request import urlopen

import nltk   
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag

names = []
A = ""
B = ""
claims = []
count = 0

def makeSimpleClaim(name, value):
    def claim(solution):
        if A == name and solution[A] == value:
            return True
        elif B == name and solution[B] == value:
            return True
        else:
            return False
    return claim

def makeSimpleANDClaim(name1, value1, name2, value2):
    def claim(solution):
        #print("Evaluating And:", name1, value1, name2, value2)
        if A == name1 and solution[A] == value1 and solution[B] == value2:
            return True
        elif B == name1 and solution[B] == value1 and solution[A] == value2:
            return True
        else:
            return False
    return claim

def makeSimpleORClaim(name1, value1, name2, value2):
    def claim(solution):
        if A == name1 and solution[A] == value1 or solution[B] == value2:
            return True
        elif B == name1 and solution[B] == value1 or solution[A] == value2:
            return True
        else:
            return False
    return claim

def makeANDNestedInORClaim(name1a, value1a, name2a, value2a, name1b, value1b, name2b, value2b):
    #print(name1a, value1a, name2a, value2a, name1b, value1b, name2b, value2b)
    def claim(solution):
        #print("Evaluating AndinOR:", name1a, value1a, name2a, value2a,name1b, value1b, name2b, value2b, solution)
        return (makeSimpleANDClaim(name1a, value1a, name2a, value2a)(solution) or 
                makeSimpleANDClaim(name1b, value1b, name2b, value2b)(solution))
    return claim

def makeORNestedInANDClaim(name1a, value1a, name2a, value2a, name1b, value1b, name2b, value2b):
    def claim(solution):
        return (makeSimpleORClaim(name1a, value1a, name2a, value2a)(solution) and 
                makeSimpleORClaim(name1b, value1b, name2b, value2b)(solution))
    return claim   
 
def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]

def getStatementsFromFile():
    files = glob.glob("./knights/kk")

    for file in files:

        txt = open(file, encoding='utf-8')
        lines = txt.readlines()
        
        if '\n' in lines:
            lines = remove_values_from_list(lines, '\n')
    
    return lines

def getName(statement):
    global names
    if statement.split()[0] == names[0]:
        name = names[1]
    else:
        name = names[0]
    return name

def knightKnaveCheck(statement):
    return "I am a knight" in statement and "is a knight" in statement or "I am a knight" in statement and "is a knave" in statement or "I am a knave" in statement and "is a knight" in statement or "I am a knave" in statement and "is a knave" in statement

def classifyStatement(statement):
    map = {}
    print(statement)
    if "least one of the following is true" in statement.lower():
        if statement.split()[0] != names[0]:
            name = name[1]
            name[1] = name[0]
            name[0] = name

        if "I am a knight" in statement and "is a knight" in statement:
            map[statement.split()[0]] = "(" +names[0] +" == knight) or (" + names[1] + " == knight)"
            claims.append((statement.split()[0],makeSimpleORClaim(names[0],"knight", names[1], "knight")))
        elif "I am a knight" in statement and "is a knave" in statement:
            map[statement.split()[0]] = "(" +names[0] +" == knight) or (" + names[1] + " == knave)"
            claims.append((statement.split()[0],makeSimpleORClaim(names[0],"knight", names[1], "knave")))
        elif "I am a knave" in statement and "is a knight" in statement:
            map[statement.split()[0]] = "(" +names[0] +" == knave) or (" + names[1] + " == knight)"
            claims.append((statement.split()[0],makeSimpleORClaim(names[0],"knave", names[1], "knight")))
        else :
            map[statement.split()[0]] = "(" +names[0] +" == knave) or (" + names[1] + " == knave)"
            claims.append((statement.split()[0],makeSimpleORClaim(names[0],"knave", names[1], "knave")))
    
    elif knightKnaveCheck(statement):
        if statement.split()[0] != names[0]:
            name = names[1]
            names[1] = names[0]
            names[0] = name
        if "I am a knight" in statement and "is a knight" in statement:
            map[statement.split()[0]] = "(" +names[0] +" == knight) or (" + names[1] + "== knight)"
            claims.append((statement.split()[0],makeSimpleORClaim(names[0],"knight", names[1], "knight")))
        elif "I am a knight" in statement and "is a knave" in statement:
            map[statement.split()[0]] = "(" +names[0] +" == knight) or (" + names[1] + "== knave)"
            claims.append((statement.split()[0],makeSimpleORClaim(names[0],"knight", names[1], "knave")))
        elif "I am a knave" in statement and "is a knight" in statement:
            map[statement.split()[0]] = "(" +names[0] +" == knave) or (" + names[1] + "== knight)"
            claims.append((statement.split()[0],makeSimpleORClaim(names[0],"knave", names[1], "knight")))
        else :
            map[statement.split()[0]] = "(" +names[0] +" == knave) or (" + names[1] + "== knave)"
            claims.append((statement.split()[0],makeSimpleORClaim(names[0],"knave", names[1], "knave")))
    
    elif " not the case that" in statement and "is a knave" in statement:
        name = getName(statement)
        
        map[statement.split()[0]] = name +" == knight"
        claims.append((statement.split()[0],makeSimpleClaim(name, "knight")))
    
    elif "false that" in statement:
        type = ""
        if "knave" in statement:
            type = "knight"
        else:
            type = "knave"
        
        name = getName(statement)
        
        map[statement.split()[0]] = name +" == " + type
        claims.append((statement.split()[0],makeSimpleClaim(name, type)))
    
    elif " not the case that" in statement and "is a knight" in statement:
        name = getName(statement)
        
        map[statement.split()[0]] = name +" == knave"
        claims.append((statement.split()[0],makeSimpleClaim(name, "knave")))       
 
    elif " not the case that" in statement and "is a knave" in statement:
        name = getName(statement)
        
        map[statement.split()[0]] = name +" == knight"
        claims.append((statement.split()[0],makeSimpleClaim(name, "knight")))     
                
    elif "exactly one is a knight" in statement.lower() or "are not the same" in statement.lower() or "are different" in statement or "exactly one is a knave"  in statement.lower():
        map[statement.split()[0]] = "(" + names[0] + " == knight " + "and " + names[1] + " == knave) or (" + names[0] + " == knave " + "and " + names[1] + " == knight)"
        claims.append((statement.split()[0],makeANDNestedInORClaim(names[0],"knight", names[1], "knave", names[0],"knave", names[1], "knight")))
    
    elif "both knights or both knaves" in statement or "are the same" in statement:
         map[statement.split()[0]] = "(" + names[0] + " == knight " + "and " + names[1] + " == knight) or (" + names[0] + " == knave " + "and " + names[1] + " == knave)"
         claims.append((statement.split()[0],makeANDNestedInORClaim(names[0],"knight", names[1], "knight", names[0],"knave", names[1], "knave")))

    elif "neither" in statement.lower() : #MOEVD UP FROM BOTTOM
        if "knave" in statement.lower() :
            map[statement.split()[0]] = names[0] + " == knight and " + names[1] + " == knight"
            claims.append((statement.split()[0],makeSimpleANDClaim(names[0],"knight", names[1], "knight")))
        else:
           map[statement.split()[0]] = names[0] + " == knave and " + names[1] + " == knave"
           claims.append((statement.split()[0],makeSimpleANDClaim(names[0],"knave", names[1], "knave")))            
             
    elif "are knights" in statement.lower() or "are both knights" in statement.lower():
        map[statement.split()[0]] = names[1] + " == knight and " + names[0] + " == knight"
        claims.append((statement.split()[0],makeSimpleANDClaim(names[1],"knight", names[0], "knight"))) 
        
    elif "are knaves" in statement.lower() or "are both knaves" in statement.lower():
        map[statement.split()[0]] = names[1] + " == knave and " + names[0] + " == knave"
        claims.append((statement.split()[0],makeSimpleANDClaim(names[1],"knave", names[0], "knave"))) 
    #LOOK AT THIS ONE - I MODIFIED IT HEAVILY
    elif "only a knave would say that" in statement.lower():
        if "only a knave would say that i" in statement.lower():
            if statement.split()[0] == names[0]:
                map[statement.split()[0]] = names[0] + " == " + ("knight" if "knave" == statement.split()[-1] else "knave") # YAY TERNARY! 
                claims.append((statement.split()[0],makeSimpleClaim(names[0], ("knight" if "knave" == statement.split()[-1] else "knave"))))
            else: 
                map[statement.split()[0]] = names[1] + " == " + ("knight" if "knave" == statement.split()[-1] else "knave") 
                claims.append((statement.split()[0],makeSimpleClaim(names[1], ("knight" if "knave" == statement.split()[-1] else "knave"))))
        else:
            if statement.split()[0] == names[0]:
                map[statement.split()[0]] = names[1] + " == " + ("knight" if "knave" == statement.split()[-1] else "knave")
                claims.append((statement.split()[0],makeSimpleClaim(names[1], ("knight" if "knave" == statement.split()[-1] else "knave"))))
            else: 
                map[statement.split()[0]] = names[0] + " == " + ("knight" if "knave" == statement.split()[-1] else "knave") 
                claims.append((statement.split()[0],makeSimpleClaim(names[0], ("knight" if "knave" == statement.split()[-1] else "knave"))))
    
    elif "could say that I am a knave" in statement or "could claim that I am a knave" in statement or "would tell you that I am a knave" in statement:
          map[statement.split()[0]] = (names[1] if statement.split()[0] == names[0] else names[0]) + " == knave" #CHANGED TO ALWAYS MAKE CLAIM ABOUT THE OTHER
          claims.append((statement.split()[0],makeSimpleClaim((names[1] if statement.split()[0] == names[0] else names[0]), "knave")))
    
    elif "could say that I am a knight" in statement or "could claim that I am a knight" in statement or "would tell you that I am a knight" in statement:
          map[statement.split()[0]] = (names[1] if statement.split()[0] == names[0] else names[0]) + " == knight" #CHANGED TO ALWAYS MAKE CLAIM ABOUT THE OTHER
          claims.append((statement.split()[0],makeSimpleClaim((names[1] if statement.split()[0] == names[0] else names[0]), "knight")))
          
    elif "Either" in statement:
        if "knight" in statement:
            map[statement.split()[0]] = "(" + names[0] +" == knight) or (" + names[1] + " == knight)"
            claims.append((statement.split()[0],makeSimpleORClaim(names[0],"knight", names[1], "knight")))
        else:
            map[statement.split()[0]] = "(" + names[0] +" == knave) or (" + names[1] + " == knave)"
            claims.append((statement.split()[0],makeSimpleORClaim(names[0],"knave", names[1], "knave")))
    elif "is a knave" in statement.lower():
        if statement.split()[0] == names[0]:
            map[statement.split()[0]] = names[1] + " == knave"
            claims.append((statement.split()[0],makeSimpleClaim(names[1], "knave"))) 
        else: 
            map[statement.split()[0]] = names[0] + " == knave"
            claims.append((statement.split()[0],makeSimpleClaim(names[0], "knave"))) 
    
    elif "is a knight" in statement.lower() :
        if statement.split()[0] == names[0]:
            map[statement.split()[0]] = names[1] + " == knight"
            claims.append((statement.split()[0],makeSimpleClaim(names[1], "knight"))) 
        else: 
            map[statement.split()[0]] = names[0] + " == knight"
            claims.append((statement.split()[0],makeSimpleClaim(names[0], "knight"))) 
    
     
    else:
        map[statement.split()[0]] = "MISSED A CASE"
    return map

def classifyKnightsAndKnaves(line):
    statements = line.split(".");
    global names
    names = statements[0].replace('You meet two inhabitants: ', "").replace(' and ', ' ').split()
    firstStatement = classifyStatement(statements[1].replace("'",""))
    secondStatement = classifyStatement(statements[2].replace("'",""))
    print(firstStatement)
    print(secondStatement)
    
if __name__ == '__main__':
    lines = getStatementsFromFile()
    
    for line in lines:
        claims = [] # reset for new game
        classifyKnightsAndKnaves(line)
        #print("Claims:", claims)
        A = claims[0][0]
        B = claims[1][0]

        #print("A:", A)
        #print("B:", B)

        solution1 = {A:"knight", B : "knight"}
        solution2 = {A:"knave", B : "knight"}
        solution3 = {A:"knight", B : "knave"}
        solution4 = {A:"knave", B : "knave"}

        if claims[0][1](solution1) and claims[1][1](solution1):
            print("Solution is:", solution1)
        if (not claims[0][1](solution2)) and claims[1][1](solution2):
            print("Solution is:", solution2)
        if claims[0][1](solution3) and (not claims[1][1](solution3)):
            print("Solution is:", solution3)
        if (not claims[0][1](solution4)) and (not claims[1][1](solution4)):
            print("Solution is:", solution4)

        print("=============================================================")

    

