# Create visit functions for every class
# Check for errors, if there are any - print information with line number

from TType import TType
from AST import *
from SymbolTable import SymbolTable, FunctionSymbol, VariableSymbol

ttype = TType()

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        #print "node {} has visitor {}".format(str(node), str(visitor))
        return visitor(node)

    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        elif hasattr(node, "children"):
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, Node):
                            self.visit(item)
                elif isinstance(child, Node):
                    self.visit(child)

class TypeChecker(NodeVisitor):

    def __init__(self):
        self.table = SymbolTable(None, "root")
        self.currentType = ""
        self.currentFun = None
        self.isInLoop = False

    def visit_NoneType(self, node):
        return 'None'

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Variable(self, node):
        definition = self.table.getGlobal(node.name)
        if definition is None:
            raise MyException("Undefined symbol {} in line {}".format(node.name, node.line))
        else:
            return definition.type

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        result = ttype(op, type1, type2)
        if result is None:
            raise MyException("Error: Illegal operation, '{} {} {}': line {}".format(type1, op, type2, node.line))
        return result

    def visit_Assignment(self, node):
        declaration = self.table.getGlobal(node.id)
        exprType = self.visit(node.expression)
        if declaration is None:
            raise MyException("Error: Variable '{}' undefined in current scope: line {}".format(node.id, node.line))
        elif declaration.type == "int" and exprType == "float":
            print "Warning: Assignment of '{}' to '{}' may cause loss of precision: line {}".format(exprType, declaration.type, node.line)
        elif declaration.type == "float" and exprType == "int":
            pass
        elif exprType != declaration.type:
            raise MyException("Error: Assignment of '{}' to '{}': line {}". format(exprType, declaration.type, node.line))

    def visit_GroupedExpression(self, node):
        return self.visit(node.interior)

    def visit_FunctionExpression(self, node):
        if self.table.get(node.name) is not None:
            raise MyException("Error: Redefinition of function '{}': line {}".format(node.id, node.line))
        else:
            function = FunctionSymbol(node.retType, node.name, SymbolTable(self.table, node.name))
            self.table.put(node.name, function)
            self.table = function.symbolTable
            self.currentFun = function
            if node.args is not None:
                self.visit(node.args)
            function.extractParams()
            self.visit(node.body)
            self.table = self.table.getParentScope()
            self.currentFun = None

    def visit_CompoundInstruction(self, node):
        innerScope = SymbolTable(self.table, "innerScope")
        self.table = innerScope
        if node.declarations is not None:
            self.visit(node.declarations)
        self.visit(node.instructions)
        self.table = self.table.getParentScope()

    def visit_ArgumentList(self, node):
        for arg in node.children:
            self.visit(arg)
        self.currentFun.extractParams()

    def visit_Argument(self, node):
        if self.table.get(node.name) is not None:
            raise MyException("Argument {} already defined. Line: {}".format(node.name, node.line))
        else:
            self.table.put(node.name, VariableSymbol(node.name, node.type))

    def visit_InvocationExpression(self, node):
        funDef = self.table.getGlobal(node.name)
        if funDef is None or not isinstance(funDef, FunctionSymbol):
            print "Function {} not defined. Line: {}".format(node.name, node.line)
        else:
            if node.args is None and funDef.params != []:
                print "Invalid number of arguments in line {}. Expected {}".\
                    format(node.line, len(funDef.params))
            else:
                types = [self.visit(x) for x in node.args.children]
                expectedTypes = funDef.params
                for actual, expected in zip(types, expectedTypes):
                    if actual != expected and not (actual == "int" and expected == "float"):
                        print "Mismatching argument types in line {}. Expected {}, got {}".\
                            format(node.line, expected, actual)
            return funDef.type

    def visit_ChoiceInstruction(self, node):
        self.visit(node.condition)
        self.visit(node.action)
        if node.alternateAction is not None:
            self.visit(node.alternateAction)

    def visit_WhileInstruction(self, node):
        innerLoop = False
        if self.isInLoop:
            innerLoop = True
        self.visit(node.condition)
        self.isInLoop = True
        self.visit(node.instruction)
        if not innerLoop:
            self.isInLoop = False

    def visit_RepeatInstruction(self, node):
        innerLoop = False
        if self.isInLoop:
            innerLoop = True
        self.isInLoop = True
        self.visit(node.instructions)
        self.visit(node.condition)
        if not innerLoop:
            self.isInLoop = False

    def visit_ReturnInstruction(self, node):
        if self.currentFun is None:
            raise MyException("Error: return instruction outside a function: line {}".format(node.line))
        else:
            retType = self.visit(node.expression)
            if retType != self.currentFun.type and (self.currentFun.type != "float" or retType != "int"):
                raise MyException("Error: Improper returned type, expected {}, got {}: line {}".format(self.actFun.type, retType, node.line))

    def visit_ContinueInstruction(self, node):
        if not self.isInLoop:
            raise MyException("Error: continue instruction outside a loop: line {}".format(node.line))

    def visit_BreakInstruction(self, node):
        if not self.isInLoop:
            raise MyException("Error: break instruction outside a loop: line {}".format(node.line))

    def visit_Init(self, node):
        initType = self.visit(node.expression)
        if (initType == self.actType) or (initType == "int" and self.actType == "float") or (initType == "float" and self.actType == "int"):
            if self.table.get(node.name) is not None:
                raise MyException("Invalid definition of {} in line: {}. Entity redefined".format(node.name, node.line))
            else:
                self.table.put(node.name, VariableSymbol(node.name, self.actType))
        else:
            raise MyException("Bad assignment of {} to {} in line {}".format(initType, self.actType, node.line))

    def visit_Declaration(self,node):
        self.actType = node.type
        self.visit(node.inits)
        self.actType = ""

    def visit_PrintInstruction(self, node):
        self.visit(node.expr)

    def visit_LabeledInstruction(self, node):
        self.visit(node.instr)

    def visit_Expression(self):
        pass

class MyException(Exception):
    def __init__(self, error):
        self.error = error

0
