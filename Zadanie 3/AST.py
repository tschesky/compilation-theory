# Not much changed here, added line to INITS

class Node(object):
    def __str__(self):
        return self.printTree(0)

    def accept(self, visitor):
        return visitor.visit(self)

    def __init__(self):
        self.children = ()

# For const we only need their value
class Const(Node):
    def __init__(self, line, value):
        self.value = value
        self.line = line


class Integer(Const):
    def __init__(self, line, value):
        Const.__init__(self, line, value)


class Float(Const):
    def __init__(self, line, value):
        Const.__init__(self, line, value)


class String(Const):
    def __init__(self, line, value):
        Const.__init__(self, line, value)
#--------------------------------------

class Variable(Node):
    def __init__(self, line, name):
        self.name = name
        self.line = line


# left op right
class BinExpr(Node):
    def __init__(self, line, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        self.line = line
        self.children = []
        self.children.append(left)
        self.children.append(right)

# List of expressions, initially empty, with a defined function to add expressions to the list
class ExpressionList(Node):
    def __init__(self):
        self.expressionList = []
        self.children = []

    def addExpression(self, expr):
        self.expressionList.append(expr)
        self.children.append(expr)

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
        self.children = []

    def addFunction(self, fundef):
        self.fundefs.append(fundef)
        self.children.append(fundef)

# Declaration list, same as above
class DeclarationList(Node):
    def __init__(self):
        self.declarations = []
        self.children = []

    def addDeclaration(self, declaration):
        self.declarations.append(declaration)
        self.children.append(declaration)

# A sigle declaration, we get type and value
class Declaration(Node):
    def __init__(self, type, inits):
        self.type = type
        self.inits = inits

# A call to a function - the name and args we use
class InvocationExpression(Node):
    def __init__(self, line, name, args):
        self.name = name
        self.args = args
        self.line = line

# Function argument, same as declaration, but we need to differentiate
class Argument(Node):
    def __init__(self, line, type, name):
        self.type = type
        self.name = name
        self.line = line

# List of arguments to collect - again empty
class ArgumentList(Node):
    def __init__(self):
        self.argList = []
        self.children = []
        
    def addArgument(self, arg):
        self.argList.append(arg)
        self.children.append(arg)

# List of initializations
class InitList(Node):
    def __init__(self):
        self.inits = []
        self.children = []
        
    def addInit(self, init):
        self.inits.append(init)
        self.children.append(init)

# Single initialization
class Init(Node):
    def __init__(self, line, name, expr):
        self.name = name
        self.expr = expr
        self.line = line

# Listof instrunction
class InstructionList(Node):
    def __init__(self):
        self.instructions = []
        self.children = []
    
    def addInstruction(self, instr):
        self.instructions.append(instr)
        self.children.append(instr)

# Pretty obvious
class PrintInstruction(Node):
    def __init__(self, line, expr):
        self.expr = expr
        self.line = line


class LabeledInstruction(Node):
    def __init__(self, id, instr):
        self.id = id
        self.instr = instr


class AssignmentInstruction(Node):
    def __init__(self, line, id, expr):
        self.id = id
        self.expr = expr
        self.line = line
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
    def __init__(self, line, expression):
        self.expression = expression
        self.line = line

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
