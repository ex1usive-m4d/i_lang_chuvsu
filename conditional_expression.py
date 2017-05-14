import zope.interface

from expression import Expression
from value import NumberValue, StringValue


class ConditionalExpression(object):
    zope.interface.implements(Expression)
    value = 0.0
    expr1 = Expression
    expr2 = Expression
    operation = ""
    operator = {
        'PLUS': '+',
        'MINUS': '-',
        'MULTIPLY': '*',
        'DIVIDE': '/',
        'EQUALS': "==",
        'NOT_EQUALS': '!=',
        'LT': '<',
        'LTEQ': '<=',
        'GT': '>',
        'GTEQ': '>=',
        'AND': '&&',
        'OR': '||',
    }

    def __init__(self, expr1, expr2, operation):
        self.expr1 = expr1
        self.expr2 = expr2
        self.operation = operation


    def eval(self):
        value1 = self.expr1.eval()
        value2 = self.expr2.eval()
        result = bool
        if isinstance(value1, StringValue) or isinstance(value2, StringValue):
            number1 = value1.as_string()
            number2 = value2.as_string()
            result = self.case_expression(self.operation, number1, number2)
        elif isinstance(value1, NumberValue):
            number1 = float(value1.as_double())
            number2 = float(value2.as_double())
            result = self.case_expression(self.operation, number1, number2)
        return NumberValue(result)
    def __str__(self):
        return "{} {} {}".format(self.expr1, self.operation, self.expr2)

    def case_expression(self, operator, value1, value2):
        return {
            '!=': value1 != value2 if True else False,
            '<': value1 < value2 if True else False,
            '>': value1 > value2 if True else False,
            '<=': value1 <= value2 if True else False,
            '>=': value1 >= value2 if True else False,
            '&&': bool(value1) and bool(value2) if True else False,
            '||': bool(value1) or bool(value2) if True else False
        }.get(operator, value1 == value2 if True else False)
