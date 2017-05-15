from binary_expression import BinaryExpression
from conditional_expression import ConditionalExpression
from functional_expression import FunctionalExpression
from statement import AssigmentStatement, WritecStatement, IfStatement, BlockStatement, WhileStatement, ForStatement, \
    BreakStatement, ContinueStatement, DoWhileStatement, FunctionStatement, FunctionDefineStatement
from token import Token
from token_type import TokenType
from unary_expression import UnaryExpression
from value_expression import ValueExpression
from variable_expression import VariableExpression


class Parser:
    tokens = []
    pos = 0
    size = 0
    EOF = Token(TokenType.EOF, "")

    def __init__(self, tokens):
        self.tokens = tokens
        self.size = len(self.tokens)

    def parse(self):
        result = BlockStatement()
        while not self.match(TokenType.EOF):
            result.add_statement(self.statement())
        return result

    def block(self):
        block = BlockStatement()
        self.consume(TokenType.LBRACE)
        while not self.match(TokenType.RBRACE):
            block.add_statement(self.statement())
        return block

    def statement_or_block(self):
        if self.get(0).get_type() == TokenType.LBRACE:
            return self.block()
        return self.statement()

    def statement(self):
        if self.match(TokenType.WRITEC):
            return WritecStatement(self.expression())
        if self.match(TokenType.IF):
            return self.if_else()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.DO):
            return self.do_while_statement()
        if self.match((TokenType.BREAK)):
            return BreakStatement()
        if self.match((TokenType.CONTINUE)):
            return ContinueStatement()
        if self.match(TokenType.FUNC):
            return self.function_define_statement();
        if self.get(0).get_type() == TokenType.WORD and self.get(1).get_type() == TokenType.LPAREN:
            return FunctionStatement(self.function())
        return self.assignment_statement()

    def assignment_statement(self):
        # WORD EQ
        current = self.get(0)
        if current.get_type() == TokenType.WORD and self.get(1).get_type() == TokenType.EQUAL:
            self.consume(TokenType.WORD)
            variable = current.get_text()
            self.consume(TokenType.EQUAL)
            return AssigmentStatement(variable, self.expression())
        else:
            print self.pos, current.get_type(), current.get_text()
            exit("Unknown statement")

    def if_else(self):
        condition = self.expression()
        if_statement = self.statement_or_block()
        if self.match(TokenType.ELSE):
            else_statement = self.statement_or_block()
            return IfStatement(condition, if_statement, else_statement)
        else:
            return IfStatement(condition, if_statement)

    def while_statement(self):
        condition = self.expression()
        statement = self.statement_or_block()
        return WhileStatement(condition, statement)

    def for_statement(self):
        initialization = self.assignment_statement()
        self.consume(TokenType.SEMIC)
        termination = self.expression()
        self.consume(TokenType.SEMIC)
        increment = self.assignment_statement()
        statement = self.statement_or_block()
        return ForStatement(initialization, termination, increment, statement)

    def do_while_statement(self):
        statement = self.statement_or_block()
        self.consume(TokenType.WHILE)
        condition = self.expression()
        return DoWhileStatement(condition, statement)

    def function_define_statement(self):
        name = self.consume(TokenType.WORD).get_text()
        self.consume(TokenType.LPAREN)
        arg_names = []
        while not self.match(TokenType.RPAREN):
            arg_names.append(self.consume(TokenType.WORD).get_text())
            self.match(TokenType.COMMA)
        body = self.statement_or_block()
        return FunctionDefineStatement(name, arg_names, body)

    def function(self):
        name = self.consume(TokenType.WORD).get_text()
        self.consume(TokenType.LPAREN)
        function = FunctionalExpression(name)
        while not self.match(TokenType.RPAREN):
            function.add_argument(self.expression())
            self.match(TokenType.COMMA)
        return function
    def expression(self):
        return self.logic_or()

    def logic_or(self):
        result = self.logic_and()
        while True:
            if (self.match(TokenType.BARBAR)):
                result = ConditionalExpression(result, self.logic_and(), ConditionalExpression.operator.get("OR"))
                continue
            else:
                break
        return result

    def logic_and(self):
        result = self.equaluty()
        while True:
            if (self.match(TokenType.AMPAMP)):
                result = ConditionalExpression(result, self.logic_and(), ConditionalExpression.operator.get("AND"))
            else:
                break
        return result

    def equaluty(self):
        expr = self.conditional()
        if self.match(TokenType.EQEQ):
            return ConditionalExpression(expr, self.conditional(), ConditionalExpression.operator.get("EQUALS"))
        if self.match(TokenType.EXCLEQ):
            return ConditionalExpression(expr, self.conditional(), ConditionalExpression.operator.get("NOT_EQUALS"))
        return expr

    def conditional(self):
        expr = self.additive()
        while True:
            if self.match(TokenType.LT):
                expr = ConditionalExpression(expr, self.additive(), ConditionalExpression.operator.get("LT"))
                continue
            if self.match(TokenType.GT):
                expr = ConditionalExpression(expr, self.additive(), ConditionalExpression.operator.get("GT"))
                continue
            if self.match(TokenType.GTEQ):
                expr = ConditionalExpression(expr, self.additive(), ConditionalExpression.operator.get("GTEQ"))
                continue
            if self.match(TokenType.LTEQ):
                expr = ConditionalExpression(expr, self.additive(), ConditionalExpression.operator.get("LTEQ"))
                continue
            break
        return expr

    def additive(self):
        expr = self.multiplicative()
        while True:
            if self.match(TokenType.PLUS):
                expr = BinaryExpression(expr, self.multiplicative(), "+")
                continue
            if self.match(TokenType.MINUS):
                expr = BinaryExpression(expr, self.multiplicative(), "-")
                continue
            break
        return expr

    def multiplicative(self):
        expr = self.unary()
        while True:
            if self.match(TokenType.STAR):
                expr = BinaryExpression(expr, self.unary(), "*")
                continue
            if self.match(TokenType.SLASH):
                expr = BinaryExpression(expr, self.unary(), "/")
                continue
            break
        return expr

    def unary(self):
        if self.match(TokenType.MINUS):
            return UnaryExpression(self.primary(), "-")
        if self.match(TokenType.PLUS):
            return self.primary()
        return self.primary()

    def primary(self):
        current = self.get(0)
        if self.match(TokenType.NUMBER):
            return ValueExpression(float(current.get_text()))
        if self.get(0).get_type() == TokenType.WORD and self.get(1).get_type() == TokenType.LPAREN:
            return self.function()
        if self.match(TokenType.WORD):
            return VariableExpression(current.get_text())
        if self.match(TokenType.TEXT):
            return ValueExpression(current.get_text())
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.match(TokenType.RPAREN)
            return expr

    def match(self, type):
        current = self.get(0)
        if type != current.get_type():
            return False
        else:
            self.pos += 1
            return True

    def consume(self, type=None):
        current = self.get(0)
        if type != current.get_type():
            return exit("Token {} doesn't match {}".format(current, type))
        else:
            self.pos += 1
            return current

    def get(self, relation_pos):
        position = self.pos + relation_pos
        if position >= self.size:
            return self.EOF
        return self.tokens[position]
