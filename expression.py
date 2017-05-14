import zope.interface

from value import Value


class Expression(zope.interface.Interface):
    def eval(self):
        return Value
