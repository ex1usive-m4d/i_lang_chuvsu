import zope.interface

from expression import Expression
from value import NumberValue, StringValue, Value


class ValueExpression(object):
    zope.interface.implements(Expression)
    value = Value

    def __init__(self, value):
        if isinstance(value, basestring) or isinstance(value, StringValue):
            self.value = StringValue(value)
        elif isinstance(value, float) or isinstance(value, NumberValue):
            self.value = NumberValue(value)

    def eval(self):
        return self.value

    def __str__(self):
        return "{}".format(self.eval())
