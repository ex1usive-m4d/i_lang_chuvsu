from token import Token
from token_type import *


class Lexer(object):
    strinput = ""
    tokens = []
    pos = 0
    length = 0
    OPERATOR_CHARS = "+-*/()="
    OPERATOR_TOKENS = [
        TokenType.PLUS, TokenType.MINUS,
        TokenType.STAR, TokenType.SLASH,
        TokenType.LPAREN, TokenType.RPAREN,
        TokenType.EQUAL
    ]

    def Lexer(self, strinput):
        self.strinput = strinput
        self.length = len(self.strinput)
        self.tokens = []

    def tokenize(self):
        while (self.pos < self.length):
            current = self.peek(0)
            if current.isdigit():
                self.tokenize_number()
            elif current.isalpha():
                self.tokenize_word()
            elif current == '"':
                self.tokenize_text()
            elif self.OPERATOR_CHARS.find(current) != -1:
                self.tokenize_operator()
            else:
                self.next()
        return self.tokens

    def tokenize_operator(self):
        position = self.OPERATOR_CHARS.index(self.peek(0))
        self.add_token_type(self.OPERATOR_TOKENS[position])
        self.next()
        return

    def tokenize_number(self):
        buff = ""
        current = self.peek(0)
        while True:
            if current == '.':
                if buff.find('.') != -1:
                    Exception('Invalid float number')
            elif not current.isdigit():
                break
            buff += current
            current = self.next()
        self.add_token(TokenType.NUMBER, buff)
        return None

    def tokenize_text(self):
        self.next()
        buff = ""
        current = self.peek(0)
        while True:
            if current == '\\':
                current = self.next()
                if current == '"':
                    current = self.next()
                    buff += '"'
                    continue
                elif current == 'n':
                    current = self.next()
                    buff += '\n'
                    continue
                elif current == 't':
                    current = self.next()
                    buff += '\t'
                    continue
                buff += '\\'
                continue
            if current == '"':
                break
            buff += current
            current = self.next()
        self.next()
        self.add_token(TokenType.TEXT, buff)

    def tokenize_word(self):
        buff = ""
        current = self.peek(0)
        while True:
            if not (current.isdigit() or current.isalpha()) and (current != '_' and current != '$'):
                break
            buff += current
            current = self.next()
        if buff == "writec":
            self.add_token(TokenType.WRITEC, buff)
        else:
            self.add_token(TokenType.WORD, buff)
        return None

    def add_token_type(self, type):
        self.add_token(type, "")

    def next(self):
        self.pos += 1
        return self.peek(0)

    def peek(self, relation_pos):
        position = self.pos + relation_pos
        if position >= self.length:
            return '\0'
        return self.strinput[position]

    def add_token(self, type, text):
        temp = Token(type, text)
        self.tokens.append(temp)
