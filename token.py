class Token:
    text = ""
    type = 0

    def __init__(self, type, text):
        self.type = type
        self.text = text

    def get_text(self):
        return self.text

    def get_type(self):
        return self.type

    def set_text(self, text):
        self.text = text

    def set_type(self, type):
        self.type = type

    def __str__(self):
        return "[{} : {}]".format(self.type, self.text)
