import random
import string

class Sentence:
    representation = []
    truth_dictionary = {}

    #function to generate a single random letter
    #@return the letter
    def get_random_letter(self):
        alphabet = string.ascii_uppercase
        letter = random.choice(alphabet)
        return letter

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
def is_negated(letter):
    return letter[0] == "~"


def get_unit_clauses(sentence):
    unit_clauses = []
    for clause in sentence.representation:
        if len(clause) == 1:
            unit_clauses.append(clause)
    return unit_clauses

def unit_propagate(sentence, unit_clauses):
    #remove all instances of letter from sentence

    for unit in unit_clauses:
        letter = unit
        if (not is_negated(letter)):
            sentence.truth_dictionary[letter[-1]] = True
        else:
            sentence.truth_dictionary[letter[-1]] = False
        # for clause in sentence.representation:
        #     if (evaluate_clause(clause) == True):
        #         sentence.representation.remove(clause)
    
    #return modified sentence


#def pure_literal_assign(letter, sentence
#):
    #assign pure literals to true
    #return modified sentence


def DPLL(sentence):
    if sentence.is_consistent():
        return True
    if sentence.contains_empty_clause(): 
        return False

    #while there are unit clauses, propagate them
    unit_clauses = get_unit_clauses(sentence)
    while(len(unit_clauses) != 0):
        unit_propagate(sentence, unit_clauses)
        unit_clauses = get_unit_clauses(sentence)
    
    #assign pure literals true
    #choose a literal and recursively call with its value assigned true then false

#gives the complement of a given variable
#@param letter a string representing a variable
#@return returns the opposite of the variable
def complement(letter):
    #if there's a ~ in the letter, just give the letter
    if (is_negated(letter)):
        return letter[1]
    #if the letter is not negated, return its negation
    else:
        return "~" + letter

def main():
    print('this working?')
    sentence = Sentence(5)
    sentence.print()
    print(get_unit_clauses(sentence))
    
    print(sentence.truth_dictionary)
    sentence.populate_true()
    print(sentence.truth_dictionary)
    sentence.print()
    print(evaluate_Expression(sentence))
    DPLL(sentence)

if __name__ == "__main__":
    main()
