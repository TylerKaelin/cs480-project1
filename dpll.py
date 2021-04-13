"""sat.py: a simple DPLL SAT solver in pure python.
The API is designed to be as simple as possible:
>>> x = Var('x')
>>> y = Var('y')
>>> z = Var('z')
>>> DPLL([(x, y, z),
...       (x, y, ~z),
...       (x, ~y, z),
...       (x, ~y, ~z),
...       (~x, y, z),
...       (~x, y, ~z),
...       (~x, ~y, z),
...       (~x, ~y, ~z)]))
None
>>> DPLL([(x, y, z),
...       (x, y, ~z),
...       (x, ~y, z),
...       (x, ~y, ~z),
...       (~x, y, z),
...       (~x, y, ~z),
...       (~x, ~y, z)])
{'y': True, 'x': True, 'z': True}
Variable objects are identical when their names are.
"""

"""
Whats in the parenthesis is or'ed together and on the outside of the parenthesis is anded
"""


class Var:
    """A simple variable class for expressing CNF formulae."""
    def __init__(self, name):
        """Initializes the variable."""
        self.name = name
        self.inverted = False

    def __invert__(self):
        """Inverts the variable."""
        inverse = self.__class__(self.name)
        inverse.inverted = not self.inverted
        return inverse

    def __str__(self):
        """Gives a short string representation of the variable."""
        return ('~' if self.inverted else '') + self.name

    def __repr__(self):
        """Gives a precise string representation of the variable."""
        return 'Var(name={}, inverted={})'.format(self.name, self.inverted)

    def __eq__(self, other):
        """Determines whether two variables are equal."""
        return self.name == other.name and self.inverted == other.inverted

    def __ne__(self, other):
        """Determines whether two variables aren't equal."""
        return not self.__eq__(other)


def assign_to_true(var, clauses):
    """Assigns a variable to true in an expression, then simplifies."""
    new_clauses = []
    for clause in clauses:
        if var in clause:
            continue
        new_clause = [clause_var for clause_var in clause
                      if clause_var != ~var]
        new_clauses.append(new_clause)
    return new_clauses


def find_pure_vars(clauses):
    """Finds all pure variables in a list of clauses."""
    seen_vars = [var for clause in clauses for var in clause]
    return [var for var in seen_vars if ~var not in seen_vars]


def DPLL(clauses):
    def DPLL_helper(clauses, values):
        """Determines if a list of CNF formulae is solvable."""
        # If all we have are literals, test if they're consistent
        if all([len(clause) == 1 for clause in clauses]):
            seen_vars = []
            for (var,) in clauses:
                for seen_var in seen_vars:
                    name_match = (seen_var.name == var.name)
                    is_opposite = (seen_var.inverted != var.inverted)
                    if name_match and is_opposite:
                        return None
                seen_vars.append(var)
                values[var.name] = not var.inverted
            return values

        # Perform unit propagation on every unit clause
        unit_clauses = [clause for clause in clauses if len(clause) == 1]
        for unit_clause in unit_clauses:
            (var,) = unit_clause
            clauses = assign_to_true(var, clauses)
            values[var.name] = not var.inverted

        # Find pure literals and assign them properly
        for var in find_pure_vars(clauses):
            clauses = assign_to_true(var, clauses)
            values[var.name] = not var.inverted

        # Check if we're done
        if len(clauses) == 0:
            return values

        # If we have any empty clauses, we can't satisfy those
        if any([len(clause) == 0 for clause in clauses]):
            return None

        # Explore by choosing a literal
        var = clauses[0][0]

        # Try assinging the variable to true
        values[var.name] = not var.inverted
        with_true = DPLL_helper(assign_to_true(var, clauses), values)
        if with_true is not None:
            return with_true

        # Try assigning the variable to false
        values[var.name] = var.inverted
        with_false = DPLL_helper(assign_to_true(var, clauses), values)
        return with_false
    return DPLL_helper(clauses, {})

def main():
 x = Var('x')
 y = Var('y')
 z = Var('z')
 q = Var('q')

 print(DPLL([(~x, ~y, ~z), (x, y, ~z), (x,y,z)]))

if __name__ == "__main__":
    main()