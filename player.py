class Player():
    def __init__(self, name, min, sec, ms):
        self.name = name
        self.min = min
        self.sec = sec
        self.ms = ms

    def name():
        doc = "The name property."
        def fget(self):
            return self._name
        def fset(self, value):
            self._name = value
        def fdel(self):
            del self._name
        return locals()
    name = property(**name())

    def min():
        doc = "The min property."
        def fget(self):
            return self._min
        def fset(self, value):
            self._min = value
        def fdel(self):
            del self._min
        return locals()
    min = property(**min())

    def sec():
        doc = "The sec property."
        def fget(self):
            return self._sec
        def fset(self, value):
            self._sec = value
        def fdel(self):
            del self._sec
        return locals()
    sec = property(**sec())

    def ms():
        doc = "The ms property."
        def fget(self):
            return self._ms
        def fset(self, value):
            self._ms = value
        def fdel(self):
            del self._ms
        return locals()
    ms = property(**ms())
