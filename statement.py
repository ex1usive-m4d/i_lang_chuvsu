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
        print self.expression.eval(),

    def __str__(self):
        return "writec {}".format(self.expression).rstrip()


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


class WhileStatement(object):
    zope.interface.implements(Statement)
    condition = Expression
    statement = Statement

    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement

    def execute(self):
        while self.condition.eval().as_double() != 0:
            try:
                self.statement.execute()
            except BreakStatement as er:
                break
            except ContinueStatement as c:
                continue

    def __str__(self):
        return "while {} {}".format(self.condition, self.statement)


class DoWhileStatement(object):
    zope.interface.implements(Statement)
    condition = Expression
    statement = Statement

    def __init__(self, condition, statement):
        self.condition = condition
        self.statement = statement

    def execute(self):
        while True:
            try:
                self.statement.execute()
            except BreakStatement as er:
                break
            except ContinueStatement as c:
                continue
            if self.condition.eval().as_double() == 0:
                break

    def __str__(self):
        return "do {} while {}".format(self.statement, self.condition, )


class ForStatement(object):
    zope.interface.implements(Statement)
    initialziation = Statement  # variable to init
    termination = Expression  # condition to termitate
    increment = Statement  # increment var
    block = Statement

    def __init__(self, initialziation, termination, increment, block):
        self.initialziation = initialziation
        self.termination = termination
        self.increment = increment
        print increment
        self.block = block

    def execute(self):
        self.initialziation.execute()
        while self.termination.eval().as_double() != 0:
            try:
                self.block.execute()
                self.increment.execute()
            except BreakStatement as er:
                break
            except ContinueStatement as c:
                continue

    def __str__(self):
        return "for {} {} {} {}".format(self.initialziation, self.termination, self.increment, self.block)


class BreakStatement(RuntimeError):
    zope.interface.implements(Statement)

    def execute(self):
        raise BreakStatement()

    def __str__(self):
        return "break"


class ContinueStatement(RuntimeError):
    zope.interface.implements(Statement)

    def execute(self):
        raise ContinueStatement()

    def __str__(self):
        return "continue"
