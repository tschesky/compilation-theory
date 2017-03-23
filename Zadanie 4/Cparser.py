#!/usr/bin/python

from scanner import Scanner
import AST
import re


class Cparser(object):


    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens


    precedence = (
       ("nonassoc", 'IFX'),
       ("nonassoc", 'ELSE'),
       ("right", '='),
       ("left", 'OR'),
       ("left", 'AND'),
       ("left", '|'),
       ("left", '^'),
       ("left", '&'),
       ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
       ("left", 'SHL', 'SHR'),
       ("left", '+', '-'),
       ("left", '*', '/', '%'),
    )


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print("Unexpected end of input")

    def p_program(self, p):
        """program : blocks"""
        p[0] = p[1]

    def p_blocks(self, p):
        """blocks : blocks block
                  | """
        if len(p) == 3:
            p[1].children.append(p[2])
            p[0] = p[1]
        else:
            p[0] = AST.Blocks()

    def p_block(self, p):
        """block : declaration
                 | fundef
                 | instruction"""
        p[0] = p[1]

    def p_declarations(self, p):
        """declarations : declarations declaration
                        | """
        if len(p) == 3:
            p[1].children.append(p[2])
            p[0] = p[1]
        else:
            p[0] = AST.DeclarationList()

    def p_declaration(self, p):
        """declaration : TYPE inits ';'
                       | error ';' """
        if len(p) == 4:
            p[0] = AST.Declaration(p[1], p[2])
        # else:
        #     p[0] = p[1]


    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        if len(p) == 4:
            p[1].children.append(p[3])
            p[0] = p[1]
        else:
            p[0] = AST.InitList()
            p[0].children.append(p[1])


    def p_init(self, p):
        """init : ID '=' expression """
        p[0] = AST.Init(p[1], p[3], p.lineno(1))


    def p_instructions_opt(self, p):
        """instructions_opt : instructions
                            | """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = AST.Instructions()


    def p_instructions(self, p):
        """instructions : instructions instruction
                        | instruction """
        if len(p) == 3:
            p[1].children.append(p[2])
            p[0] = p[1]
        else:
            p[0] = AST.InstructionList()
            p[0].children.append(p[1])


    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr
                       | repeat_instr
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr
                       | expression ';' """
        p[0] = p[1]


    def p_print_instr(self, p):
        """print_instr : PRINT expr_list ';'
                       | PRINT error ';' """
        if len(p) == 4:
            p[0] = AST.PrintInstruction(p.lineno(1), p[2])

    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """


    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        p[0] = AST.AssignmentInstruction(p.lineno(1), p[1], p[3])


    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
        if len(p) == 8:
            p[0] = AST.ChoiceInstruction(p[3], p[5], p[7])
        else:
            p[0] = AST.ChoiceInstruction(p[3], p[5], None)


    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        p[0] = AST.WhileInstruction(p[3], p[5])

    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT instructions UNTIL condition ';' """
        p[0] = AST.RepeatInstruction(p[2], p[4])

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        p[0] = AST.ReturnInstruction(p.lineno(1), p[2])

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = AST.ContinueInstruction(p.lineno(1))

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = AST.BreakInstruction(p.lineno(1))

    def p_compound_instr(self, p):
        """compound_instr : '{' declarations instructions_opt '}' """
        p[0] = AST.CompoundInstruction(p[2], p[3])


    def p_condition(self, p):
        """condition : expression"""
        p[0] = p[1]


    def p_const(self, p):
        """const : INTEGER
                 | FLOAT
                 | STRING"""

        if re.match(r"\d+(\.\d*)|\.\d+", p[1]):
            p[0] = AST.Float(p.lineno(1), p[1])
        elif re.match(r"\d+", p[1]):
            p[0] = AST.Integer(p.lineno(1), p[1])
        else:
            p[0] = AST.String(p.lineno(1), p[1][1:-1])

    def p_expression(self, p):
        """expression : const
                      | ID
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | '(' error ')'
                      | ID '(' expr_list_or_empty ')'
                      | ID '(' error ')' """
        if len(p) == 2:
            if isinstance(p[1], AST.Const):
                p[0] = p[1]
            else:
                p[0] = AST.Variable(p.lineno(1), p[1])

        elif p[1] == '(':
            p[0] = p[2]
        elif p[2] == '(':
            p[0] = AST.InvocationExpression(p.lineno(1), p[1], p[3])
        else:
            p[0] = AST.BinExpr(p[2], p[1], p[3], p.lineno(2))


    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = AST.ExpressionList()

    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        if len(p) == 4:
            p[1].children.append(p[3])
            p[0] = p[1]
        else:
            p[0] = AST.ExpressionList()
            p[0].children.append(p[1])


    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        p[0] = AST.FunctionExpression(p[1], p[2], p[4], p[6], p.lineno(1))


    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = AST.ArgumentList()

    def p_args_list(self, p):
        """args_list : args_list ',' arg
                     | arg """
        if len(p) == 4:
            p[1].children.append(p[3])
            p[0] = p[1]
        else:
            p[0] = AST.ArgumentList()
            p[0].children.append(p[1])

    def p_arg(self, p):
        """arg : TYPE ID """
        p[0] = AST.Argument(p.lineno(1), p[1], p[2])

