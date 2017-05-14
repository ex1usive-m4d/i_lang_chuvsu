from binary_expression import BinaryExpression
from conditional_expression import ConditionalExpression
from statement import AssigmentStatement, WritecStatement, IfStatement
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
        result = []
        while not self.match(TokenType.EOF):
            result.append(self.statement())
        return result

    def statement(self):
        if self.match(TokenType.WRITEC):
            return WritecStatement(self.expression())
        if self.match(TokenType.IF):
            return self.if_else()
        return self.assignment_statement()

    def assignment_statement(self):
        # WORD EQ
        current = self.get(0)
        if self.match(TokenType.WORD) and self.get(0).get_type() == TokenType.EQUAL:
            self.consume(TokenType.WORD)
            variable = current.get_text()
            self.consume(TokenType.EQUAL)
            return AssigmentStatement(variable, self.expression())
        else:
            exit("Unknown statement")

    def if_else(self):
        condition = self.expression()
        if_statement = self.statement()
        if self.match(TokenType.ELSE):
            else_statement = self.statement()
            return IfStatement(condition, if_statement, else_statement)
        else:
            return IfStatement(condition, if_statement)

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
        if self.match(TokenType.TEXT):
            return ValueExpression(current.get_text())
        if self.match(TokenType.WORD):
            return VariableExpression(current.get_text())
        if self.match(TokenType.NUMBER):
            return ValueExpression(float(current.get_text()))
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

    def consume(self, type):
        current = self.get(0)
        if type != current.get_type():
            return RuntimeError("Token", current, "doesn't match", type)
        else:
            self.pos += 1
            return current

    def get(self, relation_pos):
        position = self.pos + relation_pos
        if position >= self.size:
            return self.EOF
        return self.tokens[position]
