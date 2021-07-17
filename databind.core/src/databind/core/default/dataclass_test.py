
import typing as t
import typing_extensions as te
from dataclasses import dataclass

from databind.core.schema import Field, Schema
from databind.core.types import ConcreteType, OptionalType
from .dataclass import dataclass_to_schema
from databind.core.annotations import alias


def test_dataclass_to_schema_conversion():

  @dataclass
  class MyDataclass:
    a: int
    b: t.Optional[str] = None
    c: te.Annotated[str, alias('calias')] = 42

  schema = dataclass_to_schema(MyDataclass)
  assert schema == Schema(
    'MyDataclass',
    {
      'a': Field(ConcreteType(int), []),
      'b': Field(OptionalType(ConcreteType(str)), []),
      'c': Field(ConcreteType(str), (alias('calias'),)),
    },
    [],
    MyDataclass,
    schema.composer
  )
