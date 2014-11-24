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
    return "I am a knight" in statement and "is a knight." in statement or "I am a knight" in statement and "is a knave." in statement or "I am a knave" in statement and "is a knight." in statement or "I am a knave" in statement and "is a knave." in statement

def classifyStatement(statement):
    map = {}
    print(statement)
    if "least one of the following is true" in statement.lower():
        if statement.split()[0] != names[0]:
            name = name[1]
            name[1] = name[0]
            name[0] = name

        if "I am a knight" in statement and "is a knight." in statement:
            map[statement.split()[0]] = "(" +names[0] +" == knight) or (" + names[1] + " == knight)"
        elif "I am a knight" in statement and "is a knave." in statement:
            map[statement.split()[0]] = "(" +names[0] +" == knight) or (" + names[1] + " == knave)"
        elif "I am a knave" in statement and "is a knight." in statement:
            map[statement.split()[0]] = "(" +names[0] +" == knave) or (" + names[1] + " == knight)"
        else :
            map[statement.split()[0]] = "(" +names[0] +" == knave) or (" + names[1] + " == knave)"
    
    elif knightKnaveCheck(statement):
        if statement.split()[0] != names[0]:
            name = name[1]
            name[1] = name[0]
            name[0] = name
            
        if "I am a knight" in statement and "is a knight." in statement:
            map[statement.split()[0]] = "(" +names[0] +" == knight) or (" + names[1] + "== knight)"
        elif "I am a knight" in statement and "is a knave." in statement:
            map[statement.split()[0]] = "(" +names[0] +" == knight) or (" + names[1] + "== knave)"
        elif "I am a knave" in statement and "is a knight." in statement:
            map[statement.split()[0]] = "(" +names[0] +" == knave) or (" + names[1] + "== knight)"
        else :
            map[statement.split()[0]] = "(" +names[0] +" == knave) or (" + names[1] + "== knave)"
    
    elif " not the case that" in statement and "is a knave" in statement:
        name = getName(statement)
        
        map[statement.split()[0]] = name +" == knight"
    
    elif "false that" in statement:
        type = ""
        if "knave" in statement:
            type = "knight"
        else:
            type = "knave"
        
        name = getName(statement)
        
        map[statement.split()[0]] = name +" == " + type
    
    elif " not the case that" in statement and "is a knight" in statement:
        name = getName(statement)
        
        map[statement.split()[0]] = name +" == knave"       
 
    elif " not the case that" in statement and "is a knave" in statement:
        name = getName(statement)
        
        map[statement.split()[0]] = name +" == knight"     
                
    elif "exactly one is a knight" in statement.lower() or "are not the same" in statement.lower() or "are different" in statement or "exactly one is a knave"  in statement.lower():
        map[statement.split()[0]] = "(" + names[0] + " == knight " + "and " + names[1] + " == knave) or (" + names[0] + " == knave " + "and " + names[1] + " == knight)"
    
    elif "both knights or both knaves" in statement or "are the same" in statement:
         map[statement.split()[0]] = "(" + names[0] + " == knight " + "and " + names[1] + " == knight) or (" + names[0] + " == knave " + "and " + names[1] + " == knave)"
    
    elif "neither" in statement.lower() : #MOEVD UP FROM BOTTOM
        if "knave" in statement.lower() :
            map[statement.split()[0]] = names[0] + " == knight and " + names[1] + " == knight"
        else:
           map[statement.split()[0]] = names[0] + " == knave and " + names[1] + " == knave"  
             
    elif "are knights" in statement.lower() or "are both knights" in statement.lower():
        map[statement.split()[0]] = names[1] + " == knight and " + names[0] + " == knight" 
        
    elif "are knaves" in statement.lower() or "are both knaves" in statement.lower():
        map[statement.split()[0]] = names[1] + " == knave and " + names[0] + " == knave" 
    #LOOK AT THIS ONE
    elif "only a knave would say that" in statement.lower():
        if statement.split()[0] == names[0]:
            map[statement.split()[0]] = names[1] + " == knave and " + names[0] + " == knave" 
        else: 
            map[statement.split()[0]] = names[0] + " == knave and " + names[1] + " == knave" 
    
    elif "could say that I am a knave" in statement or "could claim that I am a knave" in statement or "would tell you that I am a knave" in statement:
          map[statement.split()[0]] = statement.split()[0] + " == knave"
    
    elif "could say that I am a knight" in statement or "could claim that I am a knight" in statement or "would tell you that I am a knight" in statement:
          map[statement.split()[0]] = statement.split()[0] + " == knight"
          
    elif "Either" in statement:
        if "knight" in statement:
            map[statement.split()[0]] = "(" + names[0] +" == knight) or (" + names[1] + " == knight)"
        else:
            map[statement.split()[0]] = "(" + names[0] +" == knave) or (" + names[1] + " == knave)"
    elif "is a knave" in statement.lower():
        if statement.split()[0] == names[0]:
            map[statement.split()[0]] = names[1] + " == knave"
        else: 
            map[statement.split()[0]] = names[0] + " == knave"
    
    elif "is a knight" in statement.lower() :
        if statement.split()[0] == names[0]:
            map[statement.split()[0]] = names[1] + " == knight"
        else: 
            map[statement.split()[0]] = names[0] + " == knight"
    
     
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
        classifyKnightsAndKnaves(line)
        print("=============================================================")
