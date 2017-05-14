from binary_expression import BinaryExpression
from statement import AssigmentStatement, WritecStatement
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
            RuntimeError("Unknown statement")

    def expression(self):
        return self.additive()

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
