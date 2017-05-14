import math

from value import NumberValue


class Variables():
    ZERO = NumberValue(0)
    variables = {}
    variables.update({'PI': NumberValue(math.pi)})
    variables.update({'E': NumberValue(math.e)})

    def set_var(self, key, value):
        self.variables[key] = value

    def get_var(self, key):
        if self.variables.has_key(key):
            return self.variables.get(key)
        else:
            return self.ZERO
