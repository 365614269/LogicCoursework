MAX_CONSTANTS = 10

TOKENS = {
    'PROPS': ['p', 'q', 'r', 's'],                                  # Propositions
    'PREDS': ['P', 'Q', 'R', 'S'],                                  # Binary Predicates
    'CONSTS': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'],   # Constants
    'VARS': ['x', 'y', 'z', 'w'],                                   # Variables
    'COMMA': ',',                                                   # Comma
    'EXIST': 'E',                                                   # Existential quantifier
    'FORALL': 'A',                                                  # Universal quantifier
    'BINARY_CONNS': ['/\\', '\\/', '=>'],                           # Binary Connectives
    'NEG': '~',                                                     # Negation
    'LEFT_PARENS': '(',                                             # Left Parenthesis
    'RIGHT_PARENS': ')'                                             # Right Parenthesis
}

def negation(fmla):
    if fmla.startswith('~'):
        return fmla[1:]
    else:
        return '~' + fmla

class Node:
    """A node in a tableau tree."""

    def __init__(self, data):
        self.data = data      # The value stored in the node
        self.left = None      # Left child
        self.right = None     # Right child
        

class Tableau:
    def __init__(self, root):
        self.root = Node(root)
        self.used_constants = 0
        self.complete = False
        self.sat = -1

    def insert_alpha(self, start_node, fmla1, fmla2):   # Insert a new node from start_node using alpha rule.
        queue = [start_node]

        while queue:
            current = queue.pop(0)

            if (not current.left) and (not current.right):
                new_node1 = Node(fmla1)
                new_node2 = Node(fmla2)
                current.left = new_node1
                current.left.left = new_node2
            else:
                if current.left:
                    queue.append(current.left)
                if current.right:
                    queue.append(current.right)

    def insert_beta(self, start_node, fmla1, fmla2):    # Insert a new node from start_node using beta rule.
        queue = [start_node]

        while queue:
            current = queue.pop(0)
            if (not current.left) and (not current.right):
                new_node1 = Node(fmla1)
                new_node2 = Node(fmla2)
                current.left = new_node1
                current.right = new_node2
            else:
                if current.left:
                    queue.append(current.left)
                if current.right:
                    queue.append(current.right)


    def insert_delta(self, start_node, fmla):
        queue = [start_node]

        while queue:
            current = queue.pop(0)

            if (not current.left) and (not current.right):
                new_node = Node(fmla)
                current.left = new_node
            else:
                if current.left:
                    queue.append(current.left)
                if current.right:
                    queue.append(current.right)


    def _get_branches(self, node, path):
        """Recursively collects all branches (paths from root to leaves)."""
        if node is None:
            return []
        path = path + [node.data]
        if node.left is None and node.right is None:
            return [path]
        branches = []
        if node.left:
            branches.extend(self._get_branches(node.left, path))
        if node.right:
            branches.extend(self._get_branches(node.right, path))
        return branches
    
    def _is_branch_closed(self, path):   # Check if a branch is closed
        for node1 in path:
            for node2 in path:
                if node1 == negation(node2):
                    return True
        return False  # Return False if the branch is not closed
    
    def closed(self):
        """Determines if the tableau is closed (all branches are closed)."""
        branches = self._get_branches(self.root, [])
        for branch in branches:
            if not self._is_branch_closed(branch):
                return False
        return True
    

def parse(fmla):
    fmla = fmla.strip()
    if fmla == "":
        return 0

    if len(fmla) == 6:
        pred = fmla[0]
        left = fmla[1]
        var1 = fmla[2]
        comma = fmla[3]
        var2 = fmla[4]
        right = fmla[5]

        if ((pred in TOKENS['PREDS']) and
            (left == TOKENS['LEFT_PARENS']) and
            (comma == TOKENS['COMMA']) and
            (right == TOKENS['RIGHT_PARENS']) and
            (var1 in TOKENS['VARS'] + TOKENS['CONSTS']) and
            (var2 in TOKENS['VARS'] + TOKENS['CONSTS'])):

            return 1    # fmla is an atom

    if len(fmla) >= 3:  # range(a, b+1) = [a, a+1, ..., b]
        quantifier = fmla[0]
        var = fmla[1]
        if var in TOKENS['VARS']:
            fmlaparse = parse(fmla[2:])

            if fmlaparse in range(1, 6):
                if quantifier == TOKENS['FORALL']:
                    return 3    # fmla is a universally quantified formula
                elif quantifier == TOKENS['EXIST']:
                    return 4    # fmla is an existentially quantified formula

    if len(fmla) >= 1:
        if fmla in TOKENS['PROPS']:
            return 6  # fmla is a proposition

        if fmla[0] == TOKENS['NEG']:
            fmlaparse = parse(fmla[1:])

            if fmlaparse in range(1, 6):
                return 2    # fmla is the negation of a first order formula
            elif fmlaparse in range(6, 9):
                return 7    # fmla is the negation of a propositional formula

        if fmla[0] == TOKENS['LEFT_PARENS'] and fmla[-1] == TOKENS['RIGHT_PARENS']:
            left = lhs(fmla)
            connective = con(fmla)
            right = rhs(fmla)

            lparse = parse(left)
            rparse = parse(right)

            if lparse in range(1, 6) and rparse in range(1, 6) and connective in TOKENS['BINARY_CONNS']:
                return 5  # fmla is a binary connective first order formula
            elif lparse in range(6, 9) and rparse in range(6, 9) and connective in TOKENS['BINARY_CONNS']:
                return 8  # fmla is a binary connective propositional formula

    return 0  # Not a valid formula

def expand(fmla, var, const, bound_vars=None, quantifier_removed=False):
    """Eliminates the outermost quantifier over 'var' and replaces 'var' with 'const' in its scope, respecting variable binding."""
    if bound_vars is None:
        bound_vars = set()

    fmlaparse = parse(fmla)
    
    if fmlaparse == 1:  # Atom
        if not var in bound_vars:
            fmla = fmla.replace(var, const)
        return fmla
    
    elif fmlaparse in [2, 7]:  # Negation
        sub_fmla = fmla[1:]
        new_sub_fmla = expand(sub_fmla, var, const, bound_vars, quantifier_removed)
        return fmla[0] + new_sub_fmla
    
    elif fmlaparse in [3, 4]:  # Quantifier
        quantifier = fmla[0]
        bound_var = fmla[1]
        sub_fmla = fmla[2:]
        if bound_var == var and not quantifier_removed:
            # Remove this quantifier and replace 'var' with 'const' in its scope
            new_sub_fmla = expand(sub_fmla, var, const, bound_vars, quantifier_removed=True)
            return new_sub_fmla
        else:
            # Keep the quantifier and add its bound variable to bound_vars
            new_bound_vars = bound_vars.copy()
            new_bound_vars.add(bound_var)
            new_sub_fmla = expand(sub_fmla, var, const, new_bound_vars, quantifier_removed)
            return quantifier + bound_var + new_sub_fmla
            
    elif fmlaparse in [5, 8]:  # Binary connective
        left = lhs(fmla)
        connective = con(fmla)
        right = rhs(fmla)
        new_left = expand(left, var, const, bound_vars, quantifier_removed)
        new_right = expand(right, var, const, bound_vars, quantifier_removed)
        return '(' + new_left + connective + new_right + ')'
    
    else:
        return fmla  # Not a recognized formula type

def lhs(fmla):
    # Extract the left-hand side of the formula
    parens = 1     # We start after the first '('
    sub_fmla = ""
    i = 1  # Start after the first '('

    while i < len(fmla):
        token = fmla[i]
        if token == TOKENS['LEFT_PARENS']:
            parens += 1
        elif token == TOKENS['RIGHT_PARENS']:
            parens -= 1

        # Check for binary connective at top level
        if parens == 1:
            for conn in TOKENS['BINARY_CONNS']:
                conn_len = len(conn)
                if fmla[i:i + conn_len] == conn:
                    return sub_fmla.strip()
        sub_fmla += token
        i += 1

    return ""  # No valid LHS found

def con(fmla):
    # Extract the binary connective from the formula
    parens = 1
    i = 1  # Start after the first '('

    while i < len(fmla):
        if fmla[i] == TOKENS['LEFT_PARENS']:
            parens += 1
        elif fmla[i] == TOKENS['RIGHT_PARENS']:
            parens -= 1

        if parens == 1:
            for conn in TOKENS['BINARY_CONNS']:
                conn_len = len(conn)
                if fmla[i:i + conn_len] == conn:
                    return conn
        i += 1

    return ""  # No valid connective found

def rhs(fmla):
    # Extract the right-hand side of the formula
    parens = 1
    i = 1  # Start after the first '('

    # Find the position where the connective ends
    while i < len(fmla):
        if fmla[i] == TOKENS['LEFT_PARENS']:
            parens += 1
        elif fmla[i] == TOKENS['RIGHT_PARENS']:
            parens -= 1

        if parens == 1:
            for conn in TOKENS['BINARY_CONNS']:
                conn_len = len(conn)
                if fmla[i:i + conn_len] == conn:
                    # RHS starts after the connective
                    rhs_start = i + conn_len
                    rhs_end = len(fmla) - 1  # Exclude the last ')'
                    return fmla[rhs_start:rhs_end].strip()
        i += 1

    return ""  # No valid RHS found

def theory(fmla):  # initialise a theory with a single formula in it
    general_queue = []
    gamma_queue = []

    tableau = Tableau(fmla)

    general_queue.append(tableau.root)

    while general_queue or gamma_queue:
        front = general_queue.pop(0)
        fmla = front.data

        while fmla.startswith("~~"):     # Eliminate double negations
            fmla = fmla[2:]

        front.data = fmla

        fmlaparse = parse(fmla)

        if fmlaparse == 3:      # Universally quantified fmla
            var = fmla[1]

            for const in TOKENS['CONSTS']:
                new_fmla = expand(fmla, var, const)
                tableau.insert_delta(front, new_fmla)        

        elif fmlaparse == 4:    # Existentially quantified fmla
            if tableau.used_constants == MAX_CONSTANTS:
                tableau.sat = 2
                return tableau
            
            new_const = TOKENS['CONSTS'][tableau.used_constants]
            tableau.used_constants += 1

            var = fmla[1]
            new_fmla = expand(fmla, var, new_const)

            tableau.insert_delta(front, new_fmla)

        elif fmlaparse in [2, 7]:        # Dealing with negations
            sub_fmla = fmla[1:]        # Consume the negation sign

            sub_fmlaparse = parse(sub_fmla)

            if sub_fmlaparse in [5, 8]:         # sub formula is a binary connective formula

                left = lhs(sub_fmla)
                conn = con(sub_fmla)
                right = rhs(sub_fmla)

                if conn == '/\\':
                    tableau.insert_beta(front, negation(left), negation(right))
                elif conn == '\\/':
                    tableau.insert_alpha(front, negation(left), negation(right))
                elif conn == '=>':
                    tableau.insert_alpha(front, left, negation(right))

            elif sub_fmlaparse == 3:    # Negation of Universally quantified fmla
                if tableau.used_constants == MAX_CONSTANTS:
                    tableau.sat = 2
                    return tableau
                
                new_const = TOKENS['CONSTS'][tableau.used_constants]
                tableau.used_constants += 1

                var = sub_fmla[1]
                new_fmla = expand(fmla, var, new_const)

                tableau.insert_delta(front, new_fmla)

            elif sub_fmlaparse == 4:    # Negation of Existentially quantified fmla
                var = fmla[1]

                for const in TOKENS['CONSTS']:
                    new_fmla = expand(fmla, var, const)
                    tableau.insert_delta(front, negation(new_fmla))

        elif fmlaparse in [5, 8]:        # Dealing with binary connectives
            left = lhs(fmla)
            conn = con(fmla)
            right = rhs(fmla)

            if conn == '/\\':
                tableau.insert_alpha(front, left, right)
            elif conn == '\\/':
                tableau.insert_beta(front, left, right)
            elif conn == '=>':
                tableau.insert_beta(front, negation(left), right)

        if front.left:
            general_queue.append(front.left)
        if front.right:
            general_queue.append(front.right)

    return tableau

# check for satisfiability
def sat(tableau):
    if tableau.sat != 2:
        if tableau.closed():
            return 0
        else:
            return 1
    else:
        return 2



#------------------------------------------------------------------------------------------------------------------------------:
#                   DO NOT MODIFY THE CODE BELOW. MODIFICATION OF THE CODE BELOW WILL RESULT IN A MARK OF 0!                   :
#------------------------------------------------------------------------------------------------------------------------------:

f = open('input.txt')

parseOutputs = ['not a formula',
                'an atom',
                'a negation of a first order logic formula',
                'a universally quantified formula',
                'an existentially quantified formula',
                'a binary connective first order formula',
                'a proposition',
                'a negation of a propositional formula',
                'a binary connective propositional formula']

satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']



firstline = f.readline()

PARSE = False
if 'PARSE' in firstline:
    PARSE = True

SAT = False
if 'SAT' in firstline:
    SAT = True

for line in f:
    line = line.strip()
    if not line:
        continue  # Skip empty lines
    parsed = parse(line)

    if PARSE:
        output = "%s is %s." % (line, parseOutputs[parsed])
        if parsed in [5, 8]:
            output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (lhs(line), con(line), rhs(line))
        print(output)

    if SAT:
        if parsed:
            tableau = theory(line)
            print('%s %s.' % (line, satOutput[sat(tableau)]))
        else:
            print('%s is not a formula.' % line)
