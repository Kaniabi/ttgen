from dataclasses import dataclass, field
from typing import Dict, List

from ttgen.dataclass_ import dataclass_from_dict


def test_simple_value():

    @dataclass
    class MyObject:
        value: int = 5

    o = dataclass_from_dict(MyObject, value=5)
    assert o.value == 5


def test_simple_list():

    @dataclass
    class Alpha:
        items: List[str] = field(default=list)

    a = dataclass_from_dict(Alpha, items=['alpha'])
    assert a.items == ['alpha']


def test_simple_dict():

    @dataclass
    class Alpha:
        items: Dict[str, str] = field(default=dict)

    a = dataclass_from_dict(Alpha, items={'a': 'alpha'})
    assert a.items == {'a': 'alpha'}


def test_object_dict():

    @dataclass
    class MyObject:
        value: int = 5

    @dataclass
    class Alpha:
        objects: Dict[str, MyObject] = field(default=dict)

    a = dataclass_from_dict(Alpha, objects=dict(a=dict(value=5)))
    assert a.objects == {'a': MyObject(value=5)}


def test_object_list():

    @dataclass
    class MyObject:
        value: int = 5

    @dataclass
    class Alpha:
        objects: List[MyObject] = field(default=list)

    a = dataclass_from_dict(Alpha, objects=[dict(value=5)])
    assert a.objects == [MyObject(value=5)]


def test_dataclass_list():

    @dataclass
    class MyObject:
        value: int = 5

    @dataclass
    class Alpha:
        objects: List[MyObject] = field(default=list)

    a = dataclass_from_dict(Alpha, objects=[MyObject(value=5)])
    assert a.objects == [MyObject(value=5)]

