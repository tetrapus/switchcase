"""
Usage:

from switchdef import Switch, DEFAULT

case = Switch(1+1)

@case(1)
def then():
    print("Not a match")

@case(2)
def then():
    print("First match!")

@case(3)
def then():
    print("Oh no, I fell through")
    return False

@case(4)
def then():
    print("Oops! Too far!")

@case(DEFAULT)
def then():
    print("Not triggered")
"""

class DEFAULT: pass


class BREAK: pass


class Switch():
    def __init__(value):
        self.value = value
        self.fallthrough = False

    def case(self, value):
        if self.fallthrough is not BREAK and (self.fallthrough or value == self.value or value is DEFAULT):
            def _(f):
                fallthrough = f()
                if fallthrough is BREAK:
                    self.fallthrough = BREAK
                else:
                    self.fallthrough = True
            return _

    def __call__(self, value):
        return self.case(value)
