import random
import string

#function to generate a single random letter
#@return the letter
def get_random_letter():
    alphabet = string.ascii_uppercase
    letter = random.choice(alphabet)
    return letter

#function to generate a CNF expression of length num_clauses
#@param num_clauses the number of clauses in the expression
#@return a list of lists of tuples representing the expression
def generate_sentence(num_clauses):
 #   init empty list of list of tuples
    sentence = []
    for i in range(num_clauses):
        clause_size = random.randint(1, 3)
        clause = []
        for j in range(clause_size):
          letter = get_random_letter()
          negate = random.randint(0, 1)
          #we are negating
          if negate == 1:
              letter = "~" + letter
          clause.append((letter, None))
        sentence.append(clause)
    return sentence

#function to print a CNF expression
#@param sentence the list of lists representing the expression
def print_sentence(sentence):
    print_string = ""
    clause_index = 0
    for clause in sentence:
        print_string += "("
        letter_index = 0
        for letter in clause:
            print_string += letter[0]
            if letter_index < len(clause) - 1:
                print_string += " | "
            letter_index += 1
        print_string += ")"
        if clause_index < len(sentence) - 1:
            print_string += " & "
        clause_index += 1
    print(print_string)

#evaluates an individual clause for its truth value
#@param clause a list of tuples where the first is the letter, second is its truth value
#@return the truth value of the clause
def evaluate_clause(clause):
    truth_value = False
    for letter in clause:
        if letter[1] == True:
            if not is_negated(letter):
                truth_value = True
                break
        elif letter[1] == False:
            if is_negated(letter):
                truth_value = True
                break
    return truth_value

#evaluates an entire CNF expression, stopping if one clause is false
#@return the truth value of the expression
def evaluate_sentence(sentence):
    truth_value = True
    for clause in sentence:
        if evaluate_clause(clause) == False:
            truth_value = False
            break
    return truth_value

#says whether or not a letter is negated
#@param a tuple with the letter in index 0
def is_negated(letter):
    return letter[0][0] == "~"

#Sets all truth values in the sentence to true -- For testing
def populate_true(sentence):
     for clause in sentence:
        for letter in clause:
            clause[clause.index(letter)] = replace_truth_value(letter, True)

#changes the truth value of a letter tuple to a given value
#@param letter a tuple consisting of a letter and its truth value
#@param truth_value the truth value to set 
#@return a tuple with the given truth value
def replace_truth_value(letter, truth_value):
    return (letter[0], truth_value)

def main():
    print('this working?')
    sentence = generate_sentence(5)
    print(sentence)
    populate_true(sentence)
    print(sentence)
    print_sentence(sentence)
    print(evaluate_sentence(sentence))
if __name__ == "__main__":
    main()
