import random
import string
import copy

class Sentence:
    representation = []
    truth_dictionary = {}

    #function to generate a single random letter
    #@return the random generated letter
    def get_random_letter(self):
        alphabet = string.ascii_uppercase + string.ascii_lowercase
        letter = random.choice(alphabet)
        return letter

    #@param num_clauses is the total number of clauses that will be in the sentence, the number of literals per clause is arbitrary
    def __init__(self, num_clauses):
       #   init empty list of list of tuples
        for i in range(num_clauses):
            clause_size = random.randint(2, 3)
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
    
    def manually_set(self, representation):
        self.representation = representation
        self.truth_dictionary = {}
        for clause in representation:
            for letter in clause:
                if not (letter[-1] in self.truth_dictionary):
                    self.truth_dictionary[letter[-1]] = None


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


    #determines if any clauses in the sentence are empty
    #NB: an empty clause means there is a contradiction!
    #@return whether an empty clause is in the sentence
    def contains_empty_clause(self):
        contains_empty = False
        for clause in self.representation:
            if len(clause) == 0:
                contains_empty = True
        return contains_empty
    
    def copy(self):
        the_copy = copy.deepcopy(self)
        the_copy.representation = copy.deepcopy(self.representation)
        the_copy.truth_dictionary = copy.deepcopy(self.truth_dictionary)
        return the_copy



#evaluates an individual clause for its truth value
#@param clause a list of letters where the first is the letter
#@param truth_dictionary an assignment of truth values to be used to evaluate the clause
#@return the truth value of the clause
def evaluate_clause(clause, truth_dictionary):
    truth_value = False
    for letter in clause:
        if len(clause) != 0:
            if truth_dictionary[letter[-1]] == True:
                if not is_negated(letter):
                    truth_value = True
                    break
            elif truth_dictionary[letter[-1]] == False:
                if is_negated(letter):
                    truth_value = True
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
        

#performs unit propagation, i.e.
#it takes all clauses with one element, assigns them the proper value,
#and them removes all clauses that it satisfies and removes the element's complement from the others
#@param sentence a CNF sentence
#@param unit_clauses a list of the sentence's unit clauses

def unit_propagate(sentence, unit_clauses):
    #remove all instances of letter from sentence
    #print("we unit propagating out here")
    #print("the sentence is:")
    #sentence.print()
    #print("our unit clauses are:")
    #print(unit_clauses)
    for unit in unit_clauses:
        #get_unit_clauses is actually a list of lists, so we need to access it like this
        letter = unit[0]
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
                    return False
                else:
                    clause.remove(complement(letter))
    return True

    
    #return modified sentence


def pure_literal_assign(sentence):
    #print("we pure literal assigning out here")
    #print("the sentence is:")
    #sentence.print()
    pure_literals = get_pure_literals(sentence)
    if (len(pure_literals) != 0):
        literal = pure_literals[0]
        if (is_negated(literal)):
            sentence.truth_dictionary[literal[-1]] = False
        else:
            sentence.truth_dictionary[literal[-1]] = True
        for clause in sentence.representation:
            if (evaluate_clause(clause, sentence.truth_dictionary) == True):
                sentence.representation.remove(clause)
    #for literal in pure_literals:
       # if (is_negated(literal)):
            #set the literal to false if it's always negated
           # sentence.truth_dictionary[literal[-1]] = False
        #else:
            #set it to true if it's never negated
           # sentence.truth_dictionary[literal[-1]] = True
        #remove all the clauses we satisfied by this assignment
       # for clause in sentence.representation:
            #if (evaluate_clause(clause, sentence.truth_dictionary) == True):
               # sentence.representation.remove(clause)
    return sentence
    
#get the list of variables that have no truth value assigned
#@param the current sentence object
#@return a list of unnasigned literals
def get_unassigned_variables(sentence):
    unassigned_variables = []
    for letter in sentence.truth_dictionary:
        if sentence.truth_dictionary[letter] == None:
            unassigned_variables.append(letter)
    return unassigned_variables

def remove_satisfied(sentence):
    anything_satisfied = False
    for clause in sentence.representation:
        if (evaluate_clause(clause, sentence.truth_dictionary) == True):
            sentence.representation.remove(clause)
            anything_satisfied = True
    return anything_satisfied
def remove_complements(sentence, letter):
    for i in range(3):
        for clause in sentence.representation:
            if (complement(letter) in clause):
                clause.remove(complement(letter))
#the main recursive algorithm, takes a sentence and figures out if its satisfiable
def DPLL(sentence):

    #since we remove all satisfied clauses, we can just check if 
    # the sentence is empty
    if (len(sentence.representation) == 0):
        print("we have satisfied the sentence! the assignment is:")
        assigned_dictionary = {}
        unassigned_dictionary = []
        for letter in sentence.truth_dictionary:
            if sentence.truth_dictionary[letter] != None:
                assigned_dictionary[letter] = sentence.truth_dictionary[letter]
            else:
                unassigned_dictionary.append(letter)
        print(assigned_dictionary)
        print("the letters which have no bearing on the truth value are:")
        print(unassigned_dictionary)
        quit()
        return True  
    else:
        print("the sentence is:")
        sentence.print()
    #if we have made a clause empty, there's a contradiction (not satisfiable)
    if sentence.contains_empty_clause(): 
        print("the sentence is unsatisfiable")
        return False

    #while there are unit clauses, propagate them
    unit_clauses = get_unit_clauses(sentence)
    while(len(unit_clauses) != 0 or len(get_pure_literals(sentence)) != 0):
        if unit_propagate(sentence, unit_clauses) == False:
            print("Two unit clauses conflict. The current branch is unsatisfiable no matter what.")
            return False
        unit_clauses = get_unit_clauses(sentence)
        pure_literal_assign(sentence)
    
    #now we try backtracking
    if(len(sentence.representation) != 0):
        print("WE ARE BACKTRACKING!!!")
        print("our sentence:")
        sentence.print()
        print("our dictionary:")
        print(sentence.truth_dictionary)
        unassigned_variables = get_unassigned_variables(sentence)
        print("unassigned variables:")
        print(unassigned_variables)
        if (len(unassigned_variables) != 0):
            for letter in unassigned_variables:
                try_true = None
                try_false = None
                print("the letter we are trying: " + letter)
                sentence_copy_true = sentence.copy()
                sentence_copy_false = sentence.copy()
                sentence_copy_true.truth_dictionary[letter] = True
                did_satisfy_true = remove_satisfied(sentence_copy_true)
                if (did_satisfy_true):
                    remove_complements(sentence_copy_true, letter)
                    try_true = DPLL(sentence_copy_true)
                sentence_copy_false.truth_dictionary[letter] = False
                print("dictionary for true:")
                print(sentence_copy_true.truth_dictionary)
                print("dictionary for false:")
                print(sentence_copy_false.truth_dictionary)
                did_satisfy_false = remove_satisfied(sentence_copy_false)
                if (did_satisfy_false):
                    remove_complements(sentence_copy_false, "~" + letter)
                    try_false = DPLL(sentence_copy_false)
                if (try_true or try_false) == True:
                    quit()
                if (try_true or try_false) == False:
                    print("all paths attempted, unsatisfiable.")
                    quit()
        
        
    DPLL(sentence)

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
    sentence = Sentence(150)
    DPLL(sentence)  

if __name__ == "__main__":
    main()
