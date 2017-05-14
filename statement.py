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
        # Variables.set_var(self.variable, result)

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
