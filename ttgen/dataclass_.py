from dataclasses import fields, is_dataclass, dataclass
from dataclasses_json import DataClassJsonMixin


def dataclass_from_dict(class_, **d):

    def _dataclass_from_dict(klass, d):

        if is_dataclass(d):
            return d

        try:
            fields_ = fields(klass)
        except TypeError:
            origin = getattr(klass, '__origin__', None)

            if origin is list:
                value_klass = klass.__args__[0]
                return [
                    _dataclass_from_dict(value_klass, i)
                    for i in d
                ]

            if origin is dict:
                value_klass = klass.__args__[1]
                return {
                    i: _dataclass_from_dict(value_klass, j)
                    for i, j in d.items()
                }

            return d  # Not a dataclass field
        else:
            fieldtypes = {f.name: f.type for f in fields_}
            return klass(
                **{i: _dataclass_from_dict(fieldtypes[i], j) for i, j in d.items()}
            )

    return _dataclass_from_dict(class_, d)


@dataclass
class Point3D(DataClassJsonMixin):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


@dataclass
class Point2D(DataClassJsonMixin):
    x: float = 0.0
    y: float = 0.0


@dataclass
class RgbType(DataClassJsonMixin):
    r: float = 0.0
    g: float = 0.0
    b: float = 0.0
