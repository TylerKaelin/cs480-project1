import random
import string

class Sentence:
    representation = []
    truth_dictionary = {}

    #function to generate a single random letter
    #@return the random generated letter
    def get_random_letter(self):
        alphabet = string.ascii_uppercase
        letter = random.choice(alphabet)
        return letter

    #@param num_clauses is the total number of clauses that will be in the sentence, the number of literals per clause is arbitarary
    def __init__(self, num_clauses):
       #   init empty list of list of tuples
        for i in range(num_clauses):
            clause_size = random.randint(1, 3)
            clause = []
            for j in range(clause_size):
              letter = self.get_random_letter()
              self.truth_dictionary[letter] = None
              negate = random.randint(0, 1)
              #we are negating
              if negate == 1:
                  letter = "~" + letter
              clause.append(letter)
            self.representation.append(clause)

    #function to print a CNF expression
    #@param sentence
    # the list of lists representing the expression
    def print(self):
        print_string = ""
        clause_index = 0
        for clause in self.representation:
            print_string += "("
            letter_index = 0
            for letter in clause:
                print_string += letter
                if letter_index < len(clause) - 1:
                    print_string += " | "
                letter_index += 1
            print_string += ")"
            if clause_index < len(self.representation) - 1:
                print_string += " & "
            clause_index += 1
        print(print_string)

    #Sets all truth values in the sentence
    # to true -- For testing
    def populate_true(self):
         for clause in self.representation:
            for letter in clause:
                self.truth_dictionary[letter[-1]] = True

    #changes the truth value of a letter tuple to a given value
    #@param letter a tuple consisting of a letter and its truth value
    #@param truth_value the truth value to set
    #@return a tuple with the given truth value
    def replace_truth_value(self, letter, truth_value):
        return (letter, truth_value)

    #determines if any clauses in the sentence are empty
    #NB: an empty clause means there is a contradiction!
    #@return whether an empty clause is in the sentence
    def contains_empty_clause(self):
        contains_empty = False
        for clause in self.representation:
            if len(clause) == 0:
                contains_empty = True
        return contains_empty

    def is_consistent(self):
        consistent = True
        checked_literals = []
        for clause in self.representation:
            for letter in clause:
                if (complement(letter) in checked_literals):
                    consistent = False
                else:
                    checked_literals.append(letter)
        return consistent


#evaluates an individual clause for its truth value
#@param clause a list of letters where the first is the letter
#@return the truth value of the clause
def evaluate_clause(clause, truth_dictionary):
    truth_value = False
    for letter in clause:
        if truth_dictionary[letter[-1]] == True:
            if not is_negated(letter):
                truth_value = True
                break
        elif truth_dictionary[letter[-1]] == False:
            if is_negated(letter):
                truth_value = True
                break
    return truth_value

#evaluates an entire CNF expression, stopping if one clause is false
#@return the truth value of the expression
def evaluate_Expression(sentence):
    truth_value = True
    for clause in sentence.representation:
        if evaluate_clause(clause, sentence.truth_dictionary) == False:
            truth_value = False
            break
    return truth_value

#says whether or not a letter is negated
#@param a string with the letter
#@return whether the letter is negated
def is_negated(letter):
    return letter[0] == "~"

#gets a list of all clauses with one element
#@param sentence a CNF sentence stored as list of lists
#@return a list of clauses with one element
def get_unit_clauses(sentence):
    unit_clauses = []
    for clause in sentence.representation:
        #if the length of the list within sentence is 1 then append that list to unit clauses
        if len(clause) == 1:
            if not (clause in unit_clauses):
                unit_clauses.append(clause)
    return unit_clauses

#gets the literals of a sentence
#NB: because our dictionary doesn't include negations, we need a function
#like this to catch negated literals
#@param sentence a sentence in CNF form
#@return the literals of a sentence (e.g. A, ~B, C)
def get_literals(sentence):
    literals = []
    for clause in sentence.representation:
        for literal in clause:
            if not (literal in literals):
                literals.append(literal)
    return literals

#finds all literals that only show up in one form 
#i.e. they only show up with negations or are never negated
#@param sentence a sentence in CNF form
#@return a list of all the pure literals
def get_pure_literals(sentence):
    pure_literals = []
    literals = get_literals(sentence)
    for literal in literals:
        is_pure = True
        for clause in sentence.representation:
            if (complement(literal) in clause):
                is_pure = False
        if is_pure:
            if not (literal in pure_literals):
                 pure_literals.append(literal)
    return pure_literals
        

#
def unit_propagate(sentence, unit_clauses):
    #remove all instances of letter from sentence

    for unit in unit_clauses:
        #get_unit_clauses is actually a list of lists, so we need to access it like this
        print("this is the length of unit clauses: " + str(len(unit_clauses)))
        letter = unit[0]
        print("each letter: " + str(letter))
        print(unit_clauses)
        if (not is_negated(letter)):
            sentence.truth_dictionary[letter[-1]] = True
        else:
            sentence.truth_dictionary[letter[-1]] = False
        for clause in sentence.representation:
            #remove any clauses that are satisfied
            if (evaluate_clause(clause, sentence.truth_dictionary) == True):
                sentence.representation.remove(clause)
            #remove the complement of the unit literal
            if (complement(letter) in clause):
                #two unit clauses conflict! unsatisfiable no matter what
                if len(clause) == 1:
                    print("the sentence is unsatisfiable")
                    quit()
                clause.remove(complement(letter))
    return sentence

    
    #return modified sentence


def pure_literal_assign(sentence):
    pure_literals = get_pure_literals(sentence)
    for literal in pure_literals:
        if (is_negated(literal)):
            #set the literal to false if it's always negated
            sentence.truth_dictionary[literal[-1]] = False
        else:
            #set it to true if it's never negated
            sentence.truth_dictionary[literal[-1]] = True
        #remove all the clauses we satisfied by this assignment
        for clause in sentence.representation:
            if (evaluate_clause(clause, sentence.truth_dictionary) == True):
                print("remove pure literal: " + str(clause))
                sentence.representation.remove(clause)
    return sentence


def DPLL(sentence):
    #im a little confused about the consistent function - sam
    if sentence.is_consistent():
        return True
    #since we remove all satisfied clauses, we can just check if 
    # the sentence is empty
    if (len(sentence) == 0):
        return True    
    #if we have made a clause empty, there's a contradiction (not satisfiable)
    if sentence.contains_empty_clause(): 
        return False

    #while there are unit clauses, propagate them
    unit_clauses = get_unit_clauses(sentence)
    while(len(unit_clauses) != 0):
        unit_propagate(sentence, unit_clauses)
        unit_clauses = get_unit_clauses(sentence)
    
    #assign pure literals true
    #choose a literal and recursively call with its value assigned true then false

    #store a copy of the sentence
    #while(sentence nonempty and other paths exist)
    #do random assignment, returning the sentence  

#gives the complement of a given variable
#@param letter a string representing a variable
#@return returns the opposite of the variable
def complement(letter):
    letter = str(letter)
    #if there's a ~ in the letter, just give the letter
    if (is_negated(letter)):
        return letter[1]
    #if the letter is not negated, return its negation
    else:
        return "~" + letter

def main():
    print('this working?')
    sentence = Sentence(100)
    sentence.print()
    print("")

    unit_clauses = get_unit_clauses(sentence)
    print(unit_clauses)
    sentence = unit_propagate(sentence, unit_clauses)
    print(sentence.truth_dictionary)
    sentence.print()

    print("get_pure_literals: " + str(get_pure_literals(sentence)))
    sentence = pure_literal_assign(sentence)
    sentence.print()

    #print("")


    
    #print(sentence.truth_dictionary)
   # print("")

    #sentence.populate_true()
   # print(sentence.truth_dictionary)
    #sentence.print()

    # print(evaluate_Expression(sentence))
    # DPLL(sentence)

if __name__ == "__main__":
    main()
