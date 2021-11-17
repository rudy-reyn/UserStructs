from collections.abc import Iterable

def UserStruct(name_, **params) -> type:
    """Class factory for creating user defined dataclasses that allow for static type checking."""

        if not isinstance(attr, str) or not attr.isidentifier():
            raise TypeError(f"Invalid attribute name for '{attr}'")
        if isinstance(dtype, Iterable):
            for d in dtype:
                if not isinstance(d, type):
                    raise TypeError(f"Invalid type specified for attribute '{attr}', got '{d}'")
        else:
            if not isinstance(dtype, type):
                raise TypeError(f"Invalid type specified for attribute '{attr}', got '{dtype}'")

    class UserStruct_:
        name: str = name_
        indexes: dict = dict(enumerate(params.keys()))
        nparams: int = len(params)
        dtypes: dict = params.copy()

        def __init__(self, *args, **kwargs):
            self.data = {}
            if (nargs := len(args) + len(kwargs)) > self.nparams:
                raise ValueError(f"Too many values, expected: {self.nparams}, got: {nargs}")

            for i, v in enumerate(args):
                attr = self.indexes[i]
                dtype = self.dtypes[attr]
                if not isinstance(v, dtype):
                    raise TypeError(f"Invalid dtype for attribute '{attr}'.\n"
                    f"expected '{dtype}', got {type(v)}")
                self.data[attr] = v

            for attr, v in kwargs.items():
                dtype = self.dtypes[attr]
                if not isinstance(v, dtype):
                    raise TypeError(f"Invalid dtype for attribute '{attr}'.\n"
                    f"expected '{dtype}', got {type(v)}")
                self.data[attr] = v

            self._singleton = True

        def __setattr__(self, attr, value):
            if hasattr(self, "_singleton"):
                if attr in self.dtypes:
                    dtype = self.dtypes[attr]
                    if not isinstance(value, dtype):
                        raise TypeError(f"Invalid dtype for attribute '{attr}'.\n"
                        f"expected '{dtype}', got {type(value)}")
                    self.data[attr] = value
                else:
                    raise AttributeError(f"Attribute '{attr}' does not exist")
            else:
                object.__setattr__(self, attr, value)

        @staticmethod
        def datatypes() -> dict:
            return UserStruct_.dtypes.copy()

        def __iter__(self):
            yield from self.data.values()

        def items(self):
            yield from self.data.items()

        def asdict(self):
            return self.data.copy()

        def __len__(self):
            return self.nparams

        def __repr__(self):
            return f"{self.name}(" + ", ".join(f"{k}={v!r}" for k, v in
                    self.data.items()) + ")"

    return type(name_, (UserStruct_, ), {})