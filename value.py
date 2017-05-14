import zope.interface


class Value(zope.interface.Interface):
    def as_double(self):
        pass

    def as_string(self):
        pass


class NumberValue(object):
    zope.interface.implements(Value)
    value = 0.0

    def __init__(self, value):
        if type(value) is not isinstance(value, basestring):
            self.value = float(value)
        if type(value) is isinstance(value, bool):
            self.value = value if 1 else 0

    def as_double(self):
        return self.value

    def as_string(self):
        return "{}".format(self.value)

    def __str__(self):
        return self.as_string()


class StringValue(object):
    zope.interface.implements(Value)
    value = None

    def __init__(self, value):
        self.value = value

    def as_double(self):
        try:
            return float(self.value)
        except:
            exit("Error convert to double")
            return 0

    def as_string(self):
        return self.value

    def __str__(self):
        return self.as_string()
