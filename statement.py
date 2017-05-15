import zope.interface

from expression import Expression
from variables import Variables


class Statement(zope.interface.Interface):
    def execute(self):
        pass


class AssigmentStatement(object):
    zope.interface.implements(Statement)
    variable = ""
    expression = Expression

    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def execute(self):
        result = self.expression.eval()
        Variables.variables[self.variable] = result

    def __str__(self):
        return '{} = {}'.format(self.variable, self.expression.eval())


class WritecStatement(object):
    zope.interface.implements(Statement)
    expression = Expression

    def __init__(self, expression):
        self.expression = expression

    def execute(self):
        print self.expression.eval()

    def __str__(self):
        return "writec {}".format(self.expression)


class IfStatement(object):
    zope.interface.implements(Statement)
    if_statement = Statement
    else_statement = Statement
    expression = Expression

    def __init__(self, expression, if_statement, else_statement=None):
        self.expression = expression
        self.else_statement = else_statement
        self.if_statement = if_statement

    def execute(self):
        result = self.expression.eval().as_double()
        if result != 0:
            self.if_statement.execute()
        elif self.else_statement != None:
            self.else_statement.execute()

    def __str__(self):
        result = 'if {} {}'.format(self.expression, str(self.if_statement))
        if self.else_statement != None:
            result += " \nelse {}".format(self.else_statement)
        return str(result)


class BlockStatement(object):
    zope.interface.implements(Statement)
    statements = None

    def __init__(self):
        self.statements = list()

    def add_statement(self, statement):
        self.statements.append(statement)

    def execute(self):
        for statement in self.statements:
            statement.execute()

    def __str__(self):
        result = ''
        for statement in self.statements:
            result += str(statement) + "\n"
        return str(result)
