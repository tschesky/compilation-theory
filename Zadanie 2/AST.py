# Here we map all tokens defined in Cparser to process them

class Node(object):
    # toString(), so when calling print() the Node is properly displayed
    def __str__(self):
        return self.printTree()

# For const we only need their value
class Const(Node):
    def __init__(self, value):
        self.value = value


class Integer(Const):
    pass


class Float(Const):
    pass


class String(Const):
    pass
#--------------------------------------

class Variable(Node):
    pass


# left op right
class BinExpr(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

# List of expressions, initially empty, with a defined function to add expressions to the list
class ExpressionList(Node):
    def __init__(self):
        self.expressionList = []

    def addExpression(self, expr):
        self.expressionList.append(expr)

# A classic function call, arguments return and the function body
class FunctionExpression(Node):
    def __init__(self, retType, name, args, body):
        self.retType = retType
        self.name = name
        self.args = args
        self.body = body

# A list of function definitions. Initially empty, we add to it later
class FunctionExpressionList(Node):
    def __init__(self):
        self.fundefs = []

    def addFunction(self, fundef):
        self.fundefs.append(fundef)

# Declaration list, same as above
class DeclarationList(Node):
    def __init__(self):
        self.declarations = []

    def addDeclaration(self, declaration):
        self.declarations.append(declaration)

# A sigle declaration, we get type and value
class Declaration(Node):
    def __init__(self, type, inits):
        self.type = type
        self.inits = inits

# A call to a function - the name and args we use
class InvocationExpression(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

# Function argument, same as declaration, but we need to differentiate
class Argument(Node):
    def __init__(self, type, name):
        self.type = type
        self.name = name

# List of arguments to collect - again empty
class ArgumentList(Node):
    def __init__(self):
        self.argList = []
        
    def addArgument(self, arg):
        self.argList.append(arg)

# List of initializations
class InitList(Node):
    def __init__(self):
        self.inits = []
        
    def addInit(self, init):
        self.inits.append(init)

# Single initialization
class Init(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

# Listof instrunction
class InstructionList(Node):
    def __init__(self):
        self.instructions = []
    
    def addInstruction(self, instr):
        self.instructions.append(instr)

# Pretty obvious
class PrintInstruction(Node):
    def __init__(self, expr):
        self.expr = expr


class LabeledInstruction(Node):
    def __init__(self, id, instr):
        self.id = id
        self.instr = instr


class AssignmentInstruction(Node):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr
#---------------

# 
class CompoundInstruction(Node):
    def __init__(self, declarations, instructions):
        self.declarations = declarations
        self.instructions = instructions

# A classic if-else
class ChoiceInstruction(Node):
    def __init__(self, condition, action, alternateAction=None):
        self.condition = condition
        self.action = action
        self.alternateAction = alternateAction

# A classic while
class WhileInstruction(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction

# A classic do-while
class RepeatInstruction(Node):
    def __init__(self, instructions, condition):
        self.instructions = instructions
        self.condition = condition

# A return for funcs()
class ReturnInstruction(Node):
    def __init__(self, expression):
        self.expression = expression

# We pass on breaks and continues
class BreakInstruction(Node):
    pass


class ContinueInstruction(Node):
    pass
#-------------------------------

# We define a program as something following that structure:
# 1) Declarations (eg. int a = 10)
# 2) Consecutive function declaration
# 3) Instructions
# If anything is declared outside of that orded - the program will not be properly parsed
class Program(Node):
    def __init__(self, declarations, fundefs, instructions):
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions
