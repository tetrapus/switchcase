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

class MetaCase(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['__cases__'] = []

    def __setitem__(self, name, value):
        if name == 'case':
            self['__cases__'].append(value)
        else:
            super().__setitem__(name, value)

class MetaSwitch(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        return MetaCase()

    def __new__(cls, name, bases, clsdict):
        if '__annotations__' in clsdict and 'switch' in clsdict['__annotations__']:
            value = clsdict['__annotations__']['switch']
            fallthrough = False
            for case in clsdict['__cases__']:
                pattern = case.__annotations__["when"]
                if value == pattern or fallthrough:
                    signal = case(value)
                    if signal is not None:
                        break
                    fallthrough = True
            else:
                if 'default' in clsdict:
                    clsdict['default']()

        return super().__new__(cls, name, bases, dict(clsdict))

class Switch(metaclass=MetaSwitch):
    pass

