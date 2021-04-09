import random
import string

expression = {}
readable_expression = []

#function to generate a single random letter
#@return the letter
def get_random_letter():
    alphabet = string.ascii_uppercase
    letter = random.choice(alphabet)
    return letter

#function indicates if negation applies
#@return true or false if it negates
def randomly_negate():
    negate = random.randint(0, 1)
    if negate == 1:
        return True
    else: 
        return False

def build_expression():
    number_of_total_variables = random.randint(3, 10)
    for number_of_clauses in range(number_of_total_variables):
        if(randomly_negate()):
            expression["~" + get_random_letter()] = "None"
        else:
            expression[get_random_letter()] = "None"
    # print(expression)
    return expression

def print_human_readable_expression(express):
    total_number_of_expressions_used = 0
    total_number_of_expressions = len(express)
    all_expression_items = express.items()

    print("length of express")
    print(express)

    for each_expression_set in range(3):
        number_of_expressions_per_set = random.randint(1, 3)
        while total_number_of_expressions_used != total_number_of_expressions:
            print()
            print()
            if(total_number_of_expressions_used <= total_number_of_expressions):
                readable_expression.append(list(all_expression_items)[total_number_of_expressions_used:number_of_expressions_per_set])
                total_number_of_expressions_used += number_of_expressions_per_set
            else:
                total_number_of_expressions_used -= number_of_expressions_per_set
                number_of_expressions_per_set = random.randint(1, 3)

    print(readable_expression)


    

# def main():
#     print_human_readable_expression(build_expression())
# if __name__ == "__main__":
#     main()