from token import Token
from token_type import *


class Lexer(object):
    strinput = ""
    tokens = []
    pos = 0
    length = 0
    OPERATOR_CHARS = "+-*/()=<>!&|"

    OPERATORS = {}
    OPERATORS.update({"+": TokenType.PLUS})
    OPERATORS.update({"-": TokenType.MINUS})
    OPERATORS.update({"*": TokenType.STAR})
    OPERATORS.update({"/": TokenType.SLASH})
    OPERATORS.update({"(": TokenType.LPAREN})
    OPERATORS.update({")": TokenType.RPAREN})
    OPERATORS.update({"[": TokenType.LBRACKET})
    OPERATORS.update({"]": TokenType.RBRACKET})
    OPERATORS.update({"{": TokenType.LBRACE})
    OPERATORS.update({"}": TokenType.RBRACE})
    OPERATORS.update({"=": TokenType.EQUAL})
    OPERATORS.update({"<": TokenType.LT})
    OPERATORS.update({">": TokenType.GT})
    OPERATORS.update({":": TokenType.COMMA})
    OPERATORS.update({"!": TokenType.EXCL})
    OPERATORS.update({"&": TokenType.AMP})
    OPERATORS.update({"|": TokenType.BAR})
    OPERATORS.update({"==": TokenType.EQEQ})
    OPERATORS.update({"!=": TokenType.EXCLEQ})
    OPERATORS.update({"<=": TokenType.LTEQ})
    OPERATORS.update({">=": TokenType.GTEQ})
    OPERATORS.update({"&&": TokenType.AMPAMP})
    OPERATORS.update({"||": TokenType.BARBAR})

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
        current = self.peek(0)
        if current == '/':
            if self.peek(1) == '*':
                self.next()
                self.next()
                self.tokenize_multi_line_comment()
                return
            elif self.peek(1) == '/':
                self.next()
                self.next()
                self.tokenize_comment()
                return

        buff = ""
        while True:
            text = buff
            if not self.OPERATORS.has_key(text + current) and text:
                self.add_token(self.OPERATORS.get(text))
                return
            buff += current
            current = self.next()

    def tokenize_comment(self):
        current = self.peek(0)
        while '\r\n\0'.find(current) == -1:
            current = self.next()

    def tokenize_multi_line_comment(self):
        current = self.peek(0)
        while True:
            if current == '\0':
                exit("Missing close tag")
            if current == '*' and self.peek(1) == '/':
                break
            current = self.next()
        self.next()
        self.next()


    def tokenize_number(self):
        buff = ""
        current = self.peek(0)
        while True:
            if current == '.':
                if buff.find('.') != -1:
                    exit('Invalid float number')
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
        elif buff == "if":
            self.add_token(TokenType.IF, buff)
        elif buff == "else":
            self.add_token(TokenType.ELSE, buff)
        else:
            self.add_token(TokenType.WORD, buff)
        return None

    def next(self):
        self.pos += 1
        return self.peek(0)

    def peek(self, relation_pos):
        position = self.pos + relation_pos
        if position >= self.length:
            return '\0'
        return self.strinput[position]

    def add_token(self, type, text=""):
        temp = Token(type, text)
        self.tokens.append(temp)
