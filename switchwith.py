class SwitchException(SyntaxError):
    pass


class UnusedException(BaseException):
    pass


class Select(object):
    def __enter__(self):
        class SwitchCase:
            def switch(self, value):
                self.value = value
                raise SwitchException

            def case(self, value):
                if value == self.value:
                    return SwitchException
                return UnusedException
        sc = SwitchCase()
        return sc.switch, sc.case

    def __exit__(self, type, value, traceback):
        return isinstance(value, SwitchException)

select = Select()
