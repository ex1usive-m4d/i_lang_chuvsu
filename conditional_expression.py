import zope.interface

from expression import Expression
from value import NumberValue, StringValue


class ConditionalExpression(object):
    zope.interface.implements(Expression)
    value = 0.0
    expr1 = Expression
    expr2 = Expression
    operation = ''

    def __init__(self, expr1, expr2, operation):
        self.expr1 = expr1
        self.expr2 = expr2
        self.operation = operation

    def number_expression(self, value):
        self.value = value

    def eval(self):
        value1 = self.expr1.eval()
        value2 = self.expr2.eval()
        if isinstance(value1, StringValue) or isinstance(value2, StringValue):
            string1 = value1.as_string()
            string2 = value2.as_string()
            return self.case_expression(self.operation, string1, string2)
        elif isinstance(value1, NumberValue):
            number1 = float(value1.as_double())
            number2 = float(value2.as_double())
            return self.case_expression(self.operation, number1, number2)

    def __str__(self):
        return "{} {} {}".format(self.expr1, self.operation, self.expr2)

    def case_expression(self, operator, value1, value2):
        return {
            '=': NumberValue(value1 == value2 if True else False),
            '<': NumberValue(value1 < value2 if True else False),
            ">": NumberValue(value1 > value2 if True else False)
        }.get(operator, NumberValue(value1 == value2 if True else False))
