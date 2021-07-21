
import enum
import typing as t
from databind.core.api import Context, ConversionError, ConverterNotFound, Direction, IConverter, IConverterProvider
from databind.core.types import BaseType, ConcreteType


class EnumConverter(IConverter, IConverterProvider):
  """
  Converter for enum values.

  * #enum.IntEnum subclasses are serialized to integers.
  * #enum.Enum subclasses are serialized to strings (from the enum value name).
  """

  def get_converter(self, type_: BaseType, direction: Direction) -> IConverter:
    if isinstance(type_, ConcreteType) and issubclass(type_.type, enum.Enum):
      return self
    raise ConverterNotFound(type_, direction)

  def convert(self, ctx: Context) -> t.Any:
    assert isinstance(ctx.type, ConcreteType)
    assert issubclass(ctx.type.type, enum.Enum)

    if ctx.direction == Direction.serialize:
      if not isinstance(ctx.value, ctx.type.type):
        raise ctx.type_error(expected=ctx.type.type)
      if issubclass(ctx.type.type, enum.IntEnum):
        return ctx.value.value
      if issubclass(ctx.type.type, enum.Enum):
        return ctx.value.name

    elif ctx.direction == Direction.deserialize:
      if issubclass(ctx.type.type, enum.IntEnum):
        if not isinstance(ctx.value, int):
          raise ctx.type_error(expected=int)
        return ctx.type.type(ctx.value)
      if issubclass(ctx.type.type, enum.Enum):
        if not isinstance(ctx.value, str):
          raise ctx.type_error(expected=str)
        try:
          return ctx.type.type[ctx.value]
        except KeyError:
          raise ConversionError(f'{ctx.value!r} is not a member of enumeration {ctx.type}')

    assert False