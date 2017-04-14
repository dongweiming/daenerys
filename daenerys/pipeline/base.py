import abc


class _Missing(object):
    def __repr__(self):
        return 'no value'
    def __reduce__(self):
        return '_missing'


_missing = _Missing()


class PipelineProperty:
    __metaclass__ = abc.ABCMeta
    __counter = 0
    required_attrs = set()

    def __init__(self, **options):
        cls = self.__class__
        self.options = options
        prefix = cls.__name__
        index = cls.__counter
        self.name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

        assigned_attrs = set()
        for name, value in options.items():
            assigned_attrs.add(name)

            # required attrs
            if name in self.required_attrs:
                setattr(self, name, value)
        missing_attrs = self.required_attrs - assigned_attrs
        if missing_attrs:
            raise TypeError("missing %r" % ", ".join(missing_attrs))

        self.prepare()

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.name, _missing)
        if value is _missing:
            value = self.provide_value(obj)
            obj.__dict__[self.name] = value
        return value

    def prepare(self):
        """This method will be called after instance ininialized. The
        subclasses could override the implementation."""

    @abc.abstractmethod
    def provide_value(self, obj):
        pass
