class CaseMeta(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['__cases__'] = []

    def __setitem__(self, name, value):
        if name == 'case':
            self['__cases__'].append(value)
        else:
            super().__setitem__(name, value)


class SwitchMeta(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        return CaseMeta()

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


class Switch(metaclass=SwitchMeta):
    pass
