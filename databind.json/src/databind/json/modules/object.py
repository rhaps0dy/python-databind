
"""
Provides the #ObjectTypeModule that implements the de/serialization of JSON payloads for databind
schemas (see #databind.core.schema).
"""

import typing as t
from databind.core.api import Context, Direction, IConverter, Context
from databind.core.types import ObjectType


class ObjectTypeConverter(IConverter):

  def convert(self, ctx: Context) -> t.Any:
    assert isinstance(ctx.type, ObjectType)
    skip_default_values = True

    if ctx.direction == Direction.serialize:
      if not isinstance(ctx.value, ctx.type.schema.python_type):
        raise ctx.type_error(expected=ctx.type.schema.python_type)

      groups: t.Dict[str, t.Dict[str, t.Any]] = {}
      for field in ctx.type.schema.fields.values():
        if not field.flat:
          continue
        value = getattr(ctx.value, field.name)
        if skip_default_values and value == field.get_default():
          continue
        groups[field.name] = ctx.push(field.type, value, field.name, field).convert()

      result: t.Dict[str, t.Any] = {}
      for field in ctx.type.schema.flat_fields():
        alias = (field.field.aliases or [field.field.name])[0]
        if field.group == '$':
          value = getattr(ctx.value, field.field.name)
          if skip_default_values and value != field.field.get_default():
            result[alias] = ctx.push(field.field.type, value, field.field.name, field.field).convert()
        elif alias in groups[field.group]:
          # May not be contained if we skipped default values.
          result[alias] = groups[field.group][alias]

      # TODO (@NiklasRosenstein): Support flat MapType() field

      return result

    elif ctx.direction == Direction.deserialize:
      if not isinstance(ctx.value, t.Mapping):
        raise ctx.type_error(expected=t.Mapping)

      groups: t.Dict[str, t.Dict[str, t.Any]] = {'$': {}}
      used_keys: t.Set[str] = set()
      for field in ctx.type.schema.flat_fields():
        aliases = field.field.aliases or [field.field.name]
        for alias in aliases:
          if alias in ctx.value:
            value = ctx.value[field.field.name]
            groups.setdefault(field.group, {})[field.field.name] = \
              ctx.push(field.field.type, value, field.field.name, field.field).convert()
            used_keys.add(alias)

      for group, values in groups.items():
        if group == '$': continue
        field = ctx.type.schema.fields[group]
        groups['$'][group] = ctx.push(field.type, values, group, field).convert()

      # TODO (@NiklasRosenstein): Support flat MapType() field

      return ctx.type.schema.composer.compose(groups['$'])

    assert False
