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

RIGHT = 0x010001
LEFT = 0x010002
UP = 0x010003
DOWN = 0x010004

SIGTERM = 0x099999

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
  if kc not in [RIGHT, LEFT, UP, DOWN]:
    return 'UNKNOWN'
  return KEY_TEXT[kc - 0x010000 - 1]


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
