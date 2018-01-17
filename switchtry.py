class SwitchException(SyntaxError):
    pass


class UnusedException(BaseException):
    pass


def switch(value):
    globals()['__switch'] = value
    raise SwitchException("No default case given")


def case(value):
    if value == globals()['__switch']:
        del globals()['__switch']
        return SwitchException
    return UnusedException
