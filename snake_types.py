# Copyright 2018 Yotam Harchol
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided
# that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and
# the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
# the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import pygame
import logging
import cPickle
import snake_pb2
import snake_pb2_grpc
import grpc

RIGHT = snake_pb2.RIGHT
LEFT = snake_pb2.LEFT
UP = snake_pb2.UP
DOWN = snake_pb2.DOWN

SIGTERM = snake_pb2.QUIT

KEY_TEXT = ['RIGHT', 'LEFT', 'UP', 'DOWN']

POINT_SIZE = 5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GAME_FPS = 10

COLOR_RED = pygame.Color(255, 0, 0)
COLOR_GREEN = pygame.Color(0, 255, 0)
COLOR_BLUE = pygame.Color(0, 0, 255)
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_BROWN = pygame.Color(165, 42, 42)

SERVER_PORT = 8080


def keycode2text(kc):
  if kc == RIGHT:
    return 'RIGHT'
  if kc == LEFT:
    return 'LEFT'
  if kc == UP:
    return 'UP'
  if kc == DOWN:
    return 'DOWN'
  if kc == SIGTERM:
    return 'TERMINATE'
  return 'UNKNOWN'


def to_proto_pos(pos):
  if isinstance(pos[0], list):
    return [to_proto_pos(p) for p in pos]
  return snake_pb2.Pos(x=pos[0], y=pos[1])


def from_proto_pos(pos):
  if not isinstance(pos, snake_pb2.Pos):
    return [from_proto_pos(p) for p in pos]
  return [pos.x, pos.y]


def wrap_event(proto_evt):
  if isinstance(proto_evt, snake_pb2.KeyPressEvent):
    return snake_pb2.Event(key_press=proto_evt)
  if isinstance(proto_evt, snake_pb2.PlayerDirectionChangeEvent):
    return snake_pb2.Event(player_direction_change=proto_evt)
  if isinstance(proto_evt, snake_pb2.FoodPositionChangeEvent):
    return snake_pb2.Event(food_position_change=proto_evt)
  if isinstance(proto_evt, snake_pb2.PlayerScoreChangeEvent):
    return snake_pb2.Event(player_score_change=proto_evt)
  if isinstance(proto_evt, snake_pb2.PlayerDimensionsEvent):
    return snake_pb2.Event(player_dimensions=proto_evt)
  if isinstance(proto_evt, snake_pb2.PlayerJoinedEvent):
    return snake_pb2.Event(player_joined=proto_evt)
  if isinstance(proto_evt, snake_pb2.PlayerTerminatedEvent):
    return snake_pb2.Event(player_terminated=proto_evt)


def unwrap_event(evt):
  if evt.HasField('key_press'):
    return evt.key_press
  if evt.HasField('player_direction_change'):
    return evt.player_direction_change
  if evt.HasField('food_position_change'):
    return evt.food_position_change
  if evt.HasField('player_score_change'):
    return evt.player_score_change
  if evt.HasField('player_dimensions'):
    return evt.player_dimensions
  if evt.HasField('player_joined'):
    return evt.player_joined
  if evt.HasField('player_terminated'):
    return evt.player_terminated


class Player(object):
  def __init__(self, id, score, init_head=None, init_body=None, init_direction=None):
    self.id = id
    self.score = score
    self.init_head = init_head
    self.init_body = init_body
    self.init_direction = init_direction
    self.snake_head = init_head
    self.snake_body = init_body
    self.direction = init_direction

  def key(self, key):
    if key == RIGHT and self.direction != LEFT:
      self.direction = key
    elif key == LEFT and self.direction != RIGHT:
      self.direction = key
    elif key == UP and self.direction != DOWN:
      self.direction = key
    elif key == DOWN and self.direction != UP:
      self.direction = key
    else:
      return None

    return key

  def reset(self):
    self.snake_head = self.init_head[:]
    self.snake_body = self.init_body[:]
    self.direction = self.init_direction


# Events

"""
class Event(object):
  def __init__(self):
    pass


class KeyPressEvent(Event):
  def __init__(self, key):
    super(KeyPressEvent, self).__init__()
    self.key = key


class PlayerDirectionChangeEvent(Event):
  def __init__(self, player_id, direction):
    super(PlayerDirectionChangeEvent, self).__init__()
    self.player_id = player_id
    self.direction = direction


class FoodPositionChangeEvent(Event):
  def __init__(self, food_pos):
    super(FoodPositionChangeEvent, self).__init__()
    self.food_pos = food_pos


class PlayerScoreChangeEvent(Event):
  def __init__(self, player_id, score):
    super(PlayerScoreChangeEvent, self).__init__()
    self.player_id = player_id
    self.score = score


class PlayerDimensionsEvent(Event):
  def __init__(self, player_id, player_pos, player_body):
    super(PlayerDimensionsEvent, self).__init__()
    self.player_id = player_id
    self.player_pos = player_pos
    self.player_body = player_body


class PlayerJoinedEvent(Event):
  def __init__(self, player_id, player_pos, player_body, direction, score, my_join=False):
    super(PlayerJoinedEvent, self).__init__()
    self.player_id = player_id
    self.player_pos = player_pos
    self.player_body = player_body
    self.direction = direction
    self.score = score
    self.my_join = my_join


class PlayerTerminatedEvent(Event):
  def __init__(self, player_id):
    super(PlayerTerminatedEvent, self).__init__()
    self.player_id = player_id
"""
