# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: snake.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='snake.proto',
  package='snake',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\x0bsnake.proto\x12\x05snake\"\x1b\n\x03Pos\x12\t\n\x01x\x18\x01 \x02(\r\x12\t\n\x01y\x18\x02 \x02(\r\";\n\rKeyPressEvent\x12\x11\n\tsignature\x18\x01 \x02(\t\x12\x17\n\x03key\x18\x02 \x02(\x0e\x32\n.snake.Key\"N\n\x1aPlayerDirectionChangeEvent\x12\x11\n\tplayer_id\x18\x01 \x02(\r\x12\x1d\n\tdirection\x18\x02 \x02(\x0e\x32\n.snake.Key\"7\n\x17\x46oodPositionChangeEvent\x12\x1c\n\x08\x66ood_pos\x18\x01 \x02(\x0b\x32\n.snake.Pos\":\n\x16PlayerScoreChangeEvent\x12\x11\n\tplayer_id\x18\x01 \x02(\r\x12\r\n\x05score\x18\x02 \x02(\r\"k\n\x15PlayerDimensionsEvent\x12\x11\n\tplayer_id\x18\x01 \x02(\r\x12\x1e\n\nplayer_pos\x18\x02 \x02(\x0b\x32\n.snake.Pos\x12\x1f\n\x0bplayer_body\x18\x03 \x03(\x0b\x32\n.snake.Pos\"\xa6\x01\n\x11PlayerJoinedEvent\x12\x11\n\tplayer_id\x18\x01 \x02(\r\x12\x1e\n\nplayer_pos\x18\x02 \x02(\x0b\x32\n.snake.Pos\x12\x1f\n\x0bplayer_body\x18\x03 \x03(\x0b\x32\n.snake.Pos\x12\x1d\n\tdirection\x18\x04 \x02(\x0e\x32\n.snake.Key\x12\r\n\x05score\x18\x05 \x02(\r\x12\x0f\n\x07my_join\x18\x06 \x02(\x08\"*\n\x15PlayerTerminatedEvent\x12\x11\n\tplayer_id\x18\x01 \x02(\r\"\xaa\x03\n\x05\x45vent\x12)\n\tkey_press\x18\x01 \x01(\x0b\x32\x14.snake.KeyPressEventH\x00\x12\x44\n\x17player_direction_change\x18\x02 \x01(\x0b\x32!.snake.PlayerDirectionChangeEventH\x00\x12>\n\x14\x66ood_position_change\x18\x03 \x01(\x0b\x32\x1e.snake.FoodPositionChangeEventH\x00\x12<\n\x13player_score_change\x18\x04 \x01(\x0b\x32\x1d.snake.PlayerScoreChangeEventH\x00\x12\x39\n\x11player_dimensions\x18\x05 \x01(\x0b\x32\x1c.snake.PlayerDimensionsEventH\x00\x12\x31\n\rplayer_joined\x18\x06 \x01(\x0b\x32\x18.snake.PlayerJoinedEventH\x00\x12\x39\n\x11player_terminated\x18\x07 \x01(\x0b\x32\x1c.snake.PlayerTerminatedEventH\x00\x42\t\n\x07\x65vt_msg\"9\n\x06\x45vents\x12\x1c\n\x06\x65vents\x18\x01 \x03(\x0b\x32\x0c.snake.Event\x12\x11\n\tsignature\x18\x02 \x01(\t\"\x16\n\x03\x41\x63k\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x1a\n\nClientInfo\x12\x0c\n\x04name\x18\x01 \x02(\t\" \n\x0bPollRequest\x12\x11\n\tsignature\x18\x01 \x02(\t*6\n\x03Key\x12\x08\n\x04LEFT\x10\x00\x12\t\n\x05RIGHT\x10\x01\x12\x06\n\x02UP\x10\x02\x12\x08\n\x04\x44OWN\x10\x03\x12\x08\n\x04QUIT\x10\x04\x32\x9d\x01\n\x0bSnakeServer\x12.\n\x08JoinGame\x12\x11.snake.ClientInfo\x1a\r.snake.Events\"\x00\x12\x31\n\x08KeyPress\x12\x14.snake.KeyPressEvent\x1a\r.snake.Events\"\x00\x12+\n\x04Poll\x12\x12.snake.PollRequest\x1a\r.snake.Events\"\x00\x32:\n\x0bSnakeClient\x12+\n\x0c\x45ventHandler\x12\r.snake.Events\x1a\n.snake.Ack\"\x00')
)

_KEY = _descriptor.EnumDescriptor(
  name='Key',
  full_name='snake.Key',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='LEFT', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RIGHT', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UP', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DOWN', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='QUIT', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1205,
  serialized_end=1259,
)
_sym_db.RegisterEnumDescriptor(_KEY)

Key = enum_type_wrapper.EnumTypeWrapper(_KEY)
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
QUIT = 4



_POS = _descriptor.Descriptor(
  name='Pos',
  full_name='snake.Pos',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='snake.Pos.x', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='y', full_name='snake.Pos.y', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=22,
  serialized_end=49,
)


_KEYPRESSEVENT = _descriptor.Descriptor(
  name='KeyPressEvent',
  full_name='snake.KeyPressEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='signature', full_name='snake.KeyPressEvent.signature', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='key', full_name='snake.KeyPressEvent.key', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=51,
  serialized_end=110,
)


_PLAYERDIRECTIONCHANGEEVENT = _descriptor.Descriptor(
  name='PlayerDirectionChangeEvent',
  full_name='snake.PlayerDirectionChangeEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_id', full_name='snake.PlayerDirectionChangeEvent.player_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='direction', full_name='snake.PlayerDirectionChangeEvent.direction', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=112,
  serialized_end=190,
)


_FOODPOSITIONCHANGEEVENT = _descriptor.Descriptor(
  name='FoodPositionChangeEvent',
  full_name='snake.FoodPositionChangeEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='food_pos', full_name='snake.FoodPositionChangeEvent.food_pos', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=192,
  serialized_end=247,
)


_PLAYERSCORECHANGEEVENT = _descriptor.Descriptor(
  name='PlayerScoreChangeEvent',
  full_name='snake.PlayerScoreChangeEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_id', full_name='snake.PlayerScoreChangeEvent.player_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='score', full_name='snake.PlayerScoreChangeEvent.score', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=249,
  serialized_end=307,
)


_PLAYERDIMENSIONSEVENT = _descriptor.Descriptor(
  name='PlayerDimensionsEvent',
  full_name='snake.PlayerDimensionsEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_id', full_name='snake.PlayerDimensionsEvent.player_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='player_pos', full_name='snake.PlayerDimensionsEvent.player_pos', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='player_body', full_name='snake.PlayerDimensionsEvent.player_body', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=309,
  serialized_end=416,
)


_PLAYERJOINEDEVENT = _descriptor.Descriptor(
  name='PlayerJoinedEvent',
  full_name='snake.PlayerJoinedEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_id', full_name='snake.PlayerJoinedEvent.player_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='player_pos', full_name='snake.PlayerJoinedEvent.player_pos', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='player_body', full_name='snake.PlayerJoinedEvent.player_body', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='direction', full_name='snake.PlayerJoinedEvent.direction', index=3,
      number=4, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='score', full_name='snake.PlayerJoinedEvent.score', index=4,
      number=5, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='my_join', full_name='snake.PlayerJoinedEvent.my_join', index=5,
      number=6, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=419,
  serialized_end=585,
)


_PLAYERTERMINATEDEVENT = _descriptor.Descriptor(
  name='PlayerTerminatedEvent',
  full_name='snake.PlayerTerminatedEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_id', full_name='snake.PlayerTerminatedEvent.player_id', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=587,
  serialized_end=629,
)


_EVENT = _descriptor.Descriptor(
  name='Event',
  full_name='snake.Event',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key_press', full_name='snake.Event.key_press', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='player_direction_change', full_name='snake.Event.player_direction_change', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='food_position_change', full_name='snake.Event.food_position_change', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='player_score_change', full_name='snake.Event.player_score_change', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='player_dimensions', full_name='snake.Event.player_dimensions', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='player_joined', full_name='snake.Event.player_joined', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='player_terminated', full_name='snake.Event.player_terminated', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='evt_msg', full_name='snake.Event.evt_msg',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=632,
  serialized_end=1058,
)


_EVENTS = _descriptor.Descriptor(
  name='Events',
  full_name='snake.Events',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='events', full_name='snake.Events.events', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='signature', full_name='snake.Events.signature', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1060,
  serialized_end=1117,
)


_ACK = _descriptor.Descriptor(
  name='Ack',
  full_name='snake.Ack',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='snake.Ack.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1119,
  serialized_end=1141,
)


_CLIENTINFO = _descriptor.Descriptor(
  name='ClientInfo',
  full_name='snake.ClientInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='snake.ClientInfo.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1143,
  serialized_end=1169,
)


_POLLREQUEST = _descriptor.Descriptor(
  name='PollRequest',
  full_name='snake.PollRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='signature', full_name='snake.PollRequest.signature', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1171,
  serialized_end=1203,
)

_KEYPRESSEVENT.fields_by_name['key'].enum_type = _KEY
_PLAYERDIRECTIONCHANGEEVENT.fields_by_name['direction'].enum_type = _KEY
_FOODPOSITIONCHANGEEVENT.fields_by_name['food_pos'].message_type = _POS
_PLAYERDIMENSIONSEVENT.fields_by_name['player_pos'].message_type = _POS
_PLAYERDIMENSIONSEVENT.fields_by_name['player_body'].message_type = _POS
_PLAYERJOINEDEVENT.fields_by_name['player_pos'].message_type = _POS
_PLAYERJOINEDEVENT.fields_by_name['player_body'].message_type = _POS
_PLAYERJOINEDEVENT.fields_by_name['direction'].enum_type = _KEY
_EVENT.fields_by_name['key_press'].message_type = _KEYPRESSEVENT
_EVENT.fields_by_name['player_direction_change'].message_type = _PLAYERDIRECTIONCHANGEEVENT
_EVENT.fields_by_name['food_position_change'].message_type = _FOODPOSITIONCHANGEEVENT
_EVENT.fields_by_name['player_score_change'].message_type = _PLAYERSCORECHANGEEVENT
_EVENT.fields_by_name['player_dimensions'].message_type = _PLAYERDIMENSIONSEVENT
_EVENT.fields_by_name['player_joined'].message_type = _PLAYERJOINEDEVENT
_EVENT.fields_by_name['player_terminated'].message_type = _PLAYERTERMINATEDEVENT
_EVENT.oneofs_by_name['evt_msg'].fields.append(
  _EVENT.fields_by_name['key_press'])
_EVENT.fields_by_name['key_press'].containing_oneof = _EVENT.oneofs_by_name['evt_msg']
_EVENT.oneofs_by_name['evt_msg'].fields.append(
  _EVENT.fields_by_name['player_direction_change'])
_EVENT.fields_by_name['player_direction_change'].containing_oneof = _EVENT.oneofs_by_name['evt_msg']
_EVENT.oneofs_by_name['evt_msg'].fields.append(
  _EVENT.fields_by_name['food_position_change'])
_EVENT.fields_by_name['food_position_change'].containing_oneof = _EVENT.oneofs_by_name['evt_msg']
_EVENT.oneofs_by_name['evt_msg'].fields.append(
  _EVENT.fields_by_name['player_score_change'])
_EVENT.fields_by_name['player_score_change'].containing_oneof = _EVENT.oneofs_by_name['evt_msg']
_EVENT.oneofs_by_name['evt_msg'].fields.append(
  _EVENT.fields_by_name['player_dimensions'])
_EVENT.fields_by_name['player_dimensions'].containing_oneof = _EVENT.oneofs_by_name['evt_msg']
_EVENT.oneofs_by_name['evt_msg'].fields.append(
  _EVENT.fields_by_name['player_joined'])
_EVENT.fields_by_name['player_joined'].containing_oneof = _EVENT.oneofs_by_name['evt_msg']
_EVENT.oneofs_by_name['evt_msg'].fields.append(
  _EVENT.fields_by_name['player_terminated'])
_EVENT.fields_by_name['player_terminated'].containing_oneof = _EVENT.oneofs_by_name['evt_msg']
_EVENTS.fields_by_name['events'].message_type = _EVENT
DESCRIPTOR.message_types_by_name['Pos'] = _POS
DESCRIPTOR.message_types_by_name['KeyPressEvent'] = _KEYPRESSEVENT
DESCRIPTOR.message_types_by_name['PlayerDirectionChangeEvent'] = _PLAYERDIRECTIONCHANGEEVENT
DESCRIPTOR.message_types_by_name['FoodPositionChangeEvent'] = _FOODPOSITIONCHANGEEVENT
DESCRIPTOR.message_types_by_name['PlayerScoreChangeEvent'] = _PLAYERSCORECHANGEEVENT
DESCRIPTOR.message_types_by_name['PlayerDimensionsEvent'] = _PLAYERDIMENSIONSEVENT
DESCRIPTOR.message_types_by_name['PlayerJoinedEvent'] = _PLAYERJOINEDEVENT
DESCRIPTOR.message_types_by_name['PlayerTerminatedEvent'] = _PLAYERTERMINATEDEVENT
DESCRIPTOR.message_types_by_name['Event'] = _EVENT
DESCRIPTOR.message_types_by_name['Events'] = _EVENTS
DESCRIPTOR.message_types_by_name['Ack'] = _ACK
DESCRIPTOR.message_types_by_name['ClientInfo'] = _CLIENTINFO
DESCRIPTOR.message_types_by_name['PollRequest'] = _POLLREQUEST
DESCRIPTOR.enum_types_by_name['Key'] = _KEY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Pos = _reflection.GeneratedProtocolMessageType('Pos', (_message.Message,), dict(
  DESCRIPTOR = _POS,
  __module__ = 'snake_pb2'
  # @@protoc_insertion_point(class_scope:snake.Pos)
  ))
_sym_db.RegisterMessage(Pos)

KeyPressEvent = _reflection.GeneratedProtocolMessageType('KeyPressEvent', (_message.Message,), dict(
  DESCRIPTOR = _KEYPRESSEVENT,
  __module__ = 'snake_pb2'
  # @@protoc_insertion_point(class_scope:snake.KeyPressEvent)
  ))
_sym_db.RegisterMessage(KeyPressEvent)

PlayerDirectionChangeEvent = _reflection.GeneratedProtocolMessageType('PlayerDirectionChangeEvent', (_message.Message,), dict(
  DESCRIPTOR = _PLAYERDIRECTIONCHANGEEVENT,
  __module__ = 'snake_pb2'
  # @@protoc_insertion_point(class_scope:snake.PlayerDirectionChangeEvent)
  ))
_sym_db.RegisterMessage(PlayerDirectionChangeEvent)

FoodPositionChangeEvent = _reflection.GeneratedProtocolMessageType('FoodPositionChangeEvent', (_message.Message,), dict(
  DESCRIPTOR = _FOODPOSITIONCHANGEEVENT,
  __module__ = 'snake_pb2'
  # @@protoc_insertion_point(class_scope:snake.FoodPositionChangeEvent)
  ))
_sym_db.RegisterMessage(FoodPositionChangeEvent)

PlayerScoreChangeEvent = _reflection.GeneratedProtocolMessageType('PlayerScoreChangeEvent', (_message.Message,), dict(
  DESCRIPTOR = _PLAYERSCORECHANGEEVENT,
  __module__ = 'snake_pb2'
  # @@protoc_insertion_point(class_scope:snake.PlayerScoreChangeEvent)
  ))
_sym_db.RegisterMessage(PlayerScoreChangeEvent)

PlayerDimensionsEvent = _reflection.GeneratedProtocolMessageType('PlayerDimensionsEvent', (_message.Message,), dict(
  DESCRIPTOR = _PLAYERDIMENSIONSEVENT,
  __module__ = 'snake_pb2'
  # @@protoc_insertion_point(class_scope:snake.PlayerDimensionsEvent)
  ))
_sym_db.RegisterMessage(PlayerDimensionsEvent)

PlayerJoinedEvent = _reflection.GeneratedProtocolMessageType('PlayerJoinedEvent', (_message.Message,), dict(
  DESCRIPTOR = _PLAYERJOINEDEVENT,
  __module__ = 'snake_pb2'
  # @@protoc_insertion_point(class_scope:snake.PlayerJoinedEvent)
  ))
_sym_db.RegisterMessage(PlayerJoinedEvent)

PlayerTerminatedEvent = _reflection.GeneratedProtocolMessageType('PlayerTerminatedEvent', (_message.Message,), dict(
  DESCRIPTOR = _PLAYERTERMINATEDEVENT,
  __module__ = 'snake_pb2'
  # @@protoc_insertion_point(class_scope:snake.PlayerTerminatedEvent)
  ))
_sym_db.RegisterMessage(PlayerTerminatedEvent)

Event = _reflection.GeneratedProtocolMessageType('Event', (_message.Message,), dict(
  DESCRIPTOR = _EVENT,
  __module__ = 'snake_pb2'
  # @@protoc_insertion_point(class_scope:snake.Event)
  ))
_sym_db.RegisterMessage(Event)

Events = _reflection.GeneratedProtocolMessageType('Events', (_message.Message,), dict(
  DESCRIPTOR = _EVENTS,
  __module__ = 'snake_pb2'
  # @@protoc_insertion_point(class_scope:snake.Events)
  ))
_sym_db.RegisterMessage(Events)

Ack = _reflection.GeneratedProtocolMessageType('Ack', (_message.Message,), dict(
  DESCRIPTOR = _ACK,
  __module__ = 'snake_pb2'
  # @@protoc_insertion_point(class_scope:snake.Ack)
  ))
_sym_db.RegisterMessage(Ack)

ClientInfo = _reflection.GeneratedProtocolMessageType('ClientInfo', (_message.Message,), dict(
  DESCRIPTOR = _CLIENTINFO,
  __module__ = 'snake_pb2'
  # @@protoc_insertion_point(class_scope:snake.ClientInfo)
  ))
_sym_db.RegisterMessage(ClientInfo)

PollRequest = _reflection.GeneratedProtocolMessageType('PollRequest', (_message.Message,), dict(
  DESCRIPTOR = _POLLREQUEST,
  __module__ = 'snake_pb2'
  # @@protoc_insertion_point(class_scope:snake.PollRequest)
  ))
_sym_db.RegisterMessage(PollRequest)



_SNAKESERVER = _descriptor.ServiceDescriptor(
  name='SnakeServer',
  full_name='snake.SnakeServer',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1262,
  serialized_end=1419,
  methods=[
  _descriptor.MethodDescriptor(
    name='JoinGame',
    full_name='snake.SnakeServer.JoinGame',
    index=0,
    containing_service=None,
    input_type=_CLIENTINFO,
    output_type=_EVENTS,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='KeyPress',
    full_name='snake.SnakeServer.KeyPress',
    index=1,
    containing_service=None,
    input_type=_KEYPRESSEVENT,
    output_type=_EVENTS,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Poll',
    full_name='snake.SnakeServer.Poll',
    index=2,
    containing_service=None,
    input_type=_POLLREQUEST,
    output_type=_EVENTS,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SNAKESERVER)

DESCRIPTOR.services_by_name['SnakeServer'] = _SNAKESERVER


_SNAKECLIENT = _descriptor.ServiceDescriptor(
  name='SnakeClient',
  full_name='snake.SnakeClient',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  serialized_start=1421,
  serialized_end=1479,
  methods=[
  _descriptor.MethodDescriptor(
    name='EventHandler',
    full_name='snake.SnakeClient.EventHandler',
    index=0,
    containing_service=None,
    input_type=_EVENTS,
    output_type=_ACK,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SNAKECLIENT)

DESCRIPTOR.services_by_name['SnakeClient'] = _SNAKECLIENT

# @@protoc_insertion_point(module_scope)
