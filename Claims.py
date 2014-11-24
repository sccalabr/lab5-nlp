

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
        if A == name1 and solution[A] == value2 and solution[B] == value2:
            return True
        elif B == name1 and solution[B] == value1 and solution[A] == value2:
            return True
        else:
            return false
    return claim

def makeSimpleORClaim(name1, value1, name2, value2):
    def claim(solution):
        if A == name1 and solution[A] == value2 or solution[B] == value2:
            return True
        elif B == name1 and solution[B] == value1 or solution[A] == value2:
            return True
        else:
            return false
    return claim

def makeANDNestedInORClaim(name1a, value1a, name2a, value2a, name1b, value1b, name2b, value2b):
    def claim(solution):
        return (makeSimpleANDClaim(name1a, value1a, name2a, value2a)(solution) or 
                makeSimpleANDClaim(name1b, value1b, name2b, value2b)(solution))
    return claim

def makeORNestedInANDClaim(name1a, value1a, name2a, value2a, name1b, value1b, name2b, value2b):
    def claim(solution):
        return (makeSimpleORClaim(name1a, value1a, name2a, value2a)(solution) and 
                makeSimpleORClaim(name1b, value1b, name2b, value2b)(solution))
    return claim