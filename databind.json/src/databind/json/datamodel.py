
"""
Provides the #DatamodelModule that implements the de/serialization of JSON payloads for databind
schemas (see #databind.core.schema).
"""

import typing as t
from databind.core import annotations as A
from databind.core.annotations.unionclass import Style, unionclass
from databind.core.api import Context, ConversionError, ConverterNotFound, Direction, IConverter, Context
from databind.core.objectmapper import Module
from databind.core.typehint import Datamodel, TypeHint, from_typing
from nr import preconditions


class DatamodelModule(Module):

  def get_converter(self, type: TypeHint, direction: Direction) -> IConverter:
    if isinstance(type, Datamodel):
      if type.schema.unionclass is not None:
        return UnionclassConverter()
      return DatamodelConverter()
    raise ConverterNotFound(type, direction)


class DatamodelConverter(IConverter):

  def convert(self, ctx: Context) -> t.Any:
    print('--> datamodel', ctx)
    raise NotImplementedError  # TODO


class UnionclassConverter(IConverter):

  def convert(self, ctx: Context) -> t.Any:
    unionclass = preconditions.check_instance_of(ctx.type, Datamodel).schema.unionclass
    unionclass = preconditions.check_not_none(unionclass).with_fallback(
      ctx.mapper.get_global_annotation(A.unionclass))
    style = preconditions.check_not_none(unionclass.style)
    discriminator_key = preconditions.check_not_none(unionclass.discriminator_key)

    is_deserialize = ctx.direction == Direction.deserialize

    if is_deserialize:
      if not isinstance(ctx.value, t.Mapping):
        raise ctx.type_error(expected='Object')
      if discriminator_key not in ctx.value:
        raise ConversionError(f'missing discriminator key {discriminator_key!r}', ctx.location)
      member_name = ctx.value[discriminator_key]
      member_type = unionclass.subtypes.get_type_by_name(member_name)
    else:
      member_type = type(ctx.value)
      member_name = unionclass.subtypes.get_type_name(member_type)

    type_hint = ctx.mapper.adapt_type_hint(from_typing(member_type)).normalize()

    if is_deserialize:
      if style == A.unionclass.Style.nested:
        if member_name not in ctx.value:
          raise ConversionError(f'missing value key {member_name!r}', ctx.location)
        child_context = ctx.push(type_hint, ctx.value[member_name], member_name, ctx.field)
      elif style == A.unionclass.Style.flat:
        child_context = ctx.push(type_hint, dict(ctx.value), None, ctx.field)
        t.cast(t.Dict, child_context.value).pop(discriminator_key)
      else:
        raise RuntimeError(f'bad style: {style!r}')
    else:
      child_context = ctx.push(type_hint, ctx.value, None, ctx.field)

    result = child_context.convert()

    if is_deserialize:
      return result
    else:
      if style == A.unionclass.Style.nested:
        result = {discriminator_key: member_name, member_name: result}
      else:
        if not isinstance(result, t.MutableMapping):
          raise RuntimeError(f'unionclass.Style.flat is not supported for non-object member types')
        result[discriminator_key] = member_name

    print('@@@', repr(result))
    return result
