import zope.interface

from expression import Expression
from value import NumberValue


class UnaryExpression(object):
    zope.interface.implements(Expression)
    value = 0.0
    expr1 = Expression
    operation = ''

    def __init__(self, expr1, operation):
        self.expr1 = expr1
        self.operation = operation

    def eval(self):
        return self.case_expression(self.operation)

    def __str__(self):
        return self.operation, str(self.expr1)

    def case_expression(self, operator):
        return {
            '-': NumberValue(-self.expr1.as_number()),
        }.get(operator, self.expr1.eval())

    pass
