import AST
from Memory import *
from Exceptions import *
from visit import *
import sys
import operator

ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.div,
       "%": operator.mod, "|": operator.or_, "&": operator.and_, "^": operator.xor,
       "&&": operator.and_, "||": operator.or_, "<<": operator.lshift, ">>": operator.rshift,
       "==": operator.eq, "!=": operator.ne, ">": operator.gt, "<": operator.lt,
       "<=": operator.le, ">=": operator.ge}

sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.variableStack = MemoryStack()
        self.functionStack = MemoryStack()

    @on('node')  #
    def visit(self, node):
        pass

    @when(AST.Integer)
    def visit(self, node):
        return int(node.value)

    @when(AST.Float)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.Variable)
    def visit(self, node):
        return self.variableStack.get(node.name)

    @when(AST.Blocks)
    def visit(self, node):
        for child in node.children:
            child.accept(self)

    @when(AST.DeclarationList)
    def visit(self, node):
        for child in node.children:
            child.accept(self)

    @when(AST.Declaration)
    def visit(self, node):
        node.inits.accept(self)

    @when(AST.InitList)
    def visit(self, node):
        for child in node.children:
            child.accept(self)

    @when(AST.Init)
    def visit(self, node):
        expression = node.expression.accept(self)
        self.variableStack.insert(node.name, expression)
        return expression

    @when(AST.FunctionExpression)
    def visit(self, node):
        self.functionStack.insert(node.name, node)

    @when(AST.ArgumentList)
    def visit(self, node):
        arg_list = []
        for child in node.children:
            arg_list.append(child.accept(self))
        return arg_list

    @when(AST.Argument)
    def visit(self, node):
        return node.name

    @when(AST.InstructionList)
    def visit(self, node):
        for child in node.children:
            child.accept(self)

    @when(AST.AssignmentInstruction)
    def visit(self, node):
        expression = node.expr.accept(self)
        self.variableStack.set(node.id, expression)
        return expression

    @when(AST.PrintInstruction)
    def visit(self, node):
        string = ""
        for expr in node.expr.accept(self):
            string += str(expr)
        print string

    @when(AST.ChoiceInstruction)
    def visit(self, node):
        if node.condition.accept(self):
            node.action.accept(self)
        elif node.alternateAction is not None:
            node.alternateAction.accept(self)

    @when(AST.WhileInstruction)
    def visit(self, node):
        while node.condition.accept(self):
            try:
                node.instruction.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.RepeatInstruction)
    def visit(self, node):
        while True:
            try:
                node.instructions.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass
            if node.condition.accept(self):
                    break

    @when(AST.ReturnInstruction)
    def visit(self, node):
        value = node.expression.accept(self)
        raise ReturnValueException(value)

    @when(AST.ContinueInstruction)
    def visit(self, node):
        raise ContinueException()

    @when(AST.BreakInstruction)
    def visit(self, node):
        raise BreakException()

    @when(AST.CompoundInstruction)
    def visit(self, node):
        compound_memory = Memory("compoundScope")
        self.variableStack.push(compound_memory)
        node.declarations.accept(self)
        try:
            node.instructions.accept(self)
        finally:
            self.variableStack.pop()

    @when(AST.ExpressionList)
    def visit(self, node):
        expr_list = []
        for child in node.children:
            expr_list.append(child.accept(self))
        return expr_list

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return ops[node.op](r1, r2)

    @when(AST.InvocationExpression)
    def visit(self, node):
        fun = self.functionStack.get(node.name)
        function_memory = Memory(node.name)
        for actualArg, argExpr in zip(fun.args.accept(self), node.args.accept(self)):
            function_memory.put(actualArg, argExpr)
        self.variableStack.push(function_memory)
        try:
            fun.body.accept(self)
        except ReturnValueException as e:
            return e.value
        finally:
            self.variableStack.pop()
