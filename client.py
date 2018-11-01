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


import socket
from snake_types import *
import pygame
import sys
import time
from threading import Timer
import struct
import concurrent.futures

POLL_TIMEOUT = 0.1

logging.basicConfig()
_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)

__next_colors = [COLOR_GREEN, COLOR_BLUE, COLOR_RED, COLOR_BLACK]

AUTO_MODE = False

USAGE = 'Usage: python client.py [AUTO] [server address]\n\tAUTO: client will play automatically: it will attempt ' + \
        'to not hit bounds,\n\t\tand to eat food.\n\tServer address: IP address or URL of the server.\n\t\tIf not ' + \
        'provided, localhost is used.\n\t--help: shows this message (and quits)\n'

def _next_color():
  res = __next_colors.pop(0)
  __next_colors.append(res)
  return res


KEY_DICT = {
  pygame.K_RIGHT: RIGHT,
  pygame.K_LEFT: LEFT,
  pygame.K_UP: UP,
  pygame.K_DOWN: DOWN
}


class SnakeClient:
  def __init__(self, server_address, name='Client'):
    self.server_address = server_address
    self.ui = None
    self.game = ClientGame()
    self.stub = snake_pb2_grpc.SnakeServerStub(grpc.insecure_channel('%s:%d' % (server_address, SERVER_PORT)))
    self.client_info = snake_pb2.ClientInfo(name=name)
    self.signature = None
    self.last_event_received = 0

  def handle_received_events(self, events_message):
    self.last_event_received = time.time()
    if len(events_message.events) > 0:
      _log.debug('Received %d events from server' % len(events_message.events))
      events = [unwrap_event(evt) for evt in events_message.events]
      for evt in events:
        self.game.handle_server_event(evt)
    if self.game.active:
      Timer(POLL_TIMEOUT, function=self.poll_timer).start()

  def poll_server(self):
    res = self.stub.Poll(snake_pb2.PollRequest(signature=self.signature))
    self.handle_received_events(res)

  def poll_timer(self):
    if time.time() - self.last_event_received > POLL_TIMEOUT:
      self.poll_server()

  def start(self):
    self.ui = UiBoard(self)
    self.ui.game = self.game
    events = self.stub.JoinGame(self.client_info)
    _log.debug('Received %d initial events. Signature: %s' % (len(events.events), events.signature))
    self.signature = events.signature
    self.handle_received_events(events)
    self.ui.start()

  def term(self):
    self.game.active = False
    res = self.stub.KeyPress(snake_pb2.KeyPressEvent(signature=self.signature, key=SIGTERM))
    self.handle_received_events(res)

  def keypress(self, key):
    _log.debug('Sending keypress: %d' % key)
    res = self.stub.KeyPress(snake_pb2.KeyPressEvent(signature=self.signature, key=key))
    self.handle_received_events(res)


class ClientPlayer(Player):
  def __init__(self, id, snake_head, snake_body, direction, score):
    super(ClientPlayer, self).__init__(id, score, snake_head, snake_body, direction)
    self.color = _next_color()


class ClientGame:
  def __init__(self):
    self.width = SCREEN_WIDTH
    self.height = SCREEN_HEIGHT
    self.players = {}
    self.active = True
    self.food_pos = None
    self.recently_set = set()
    self.player_id = None

  def handle_server_event(self, event):
    _log.debug('Received event of type %s' % (type(event)))

    if isinstance(event, snake_pb2.PlayerJoinedEvent):
      self.players[event.player_id] = ClientPlayer(event.player_id, from_proto_pos(event.player_pos),
                                                   from_proto_pos(event.player_body), event.direction, event.score)
      self.recently_set.add(event.player_id)
      if event.my_join:
        self.player_id = event.player_id
    elif isinstance(event, snake_pb2.FoodPositionChangeEvent):
        self.food_pos = from_proto_pos(event.food_pos)
    elif event.player_id not in self.players:
      _log.debug('No such player (yet?): %d' % event.player_id)
      return
    elif isinstance(event, snake_pb2.PlayerDirectionChangeEvent):
      self.players[event.player_id].direction = event.direction
    elif isinstance(event, snake_pb2.PlayerScoreChangeEvent):
      self.players[event.player_id].score = event.score
    elif isinstance(event, snake_pb2.PlayerDimensionsEvent):
      self.players[event.player_id].snake_head = from_proto_pos(event.player_pos)
      self.players[event.player_id].snake_body = from_proto_pos(event.player_body)
      self.recently_set.add(event.player_id)
    elif isinstance(event, snake_pb2.PlayerTerminatedEvent):
      del self.players[event.player_id]
      if event.player_id == self.player_id:
        self.active = False

  def get_recently_set(self):
    res = self.recently_set
    self.recently_set = set()
    return res


class UiBoard:
  def __init__(self, client):
    self.game = None
    _log.debug('Creating GUI')
    pygame.init()
    self.client = client
    self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
    self.board = pygame.display.set_mode((self.width, self.height))
    pygame.display.set_caption("Snake" if not AUTO_MODE else "Snake AUTO")
    self.clock = pygame.time.Clock()

  def gameOver(self):
    self.board.fill(COLOR_WHITE)
    myFont = pygame.font.SysFont('Helvetica', 72)
    GOsurf = myFont.render("Game Over", True, COLOR_RED)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (self.width // 2, 25)
    self.board.blit(GOsurf, GOrect)
    self.showScore(0)
    pygame.display.flip()

  def showScore(self, pos=1):
    font = pygame.font.SysFont('Helvetica', 18)
    score_text = ''
    for i in self.game.players:
      score_text += 'Player %d: %d  ' % (i, self.game.players[i].score)
    text = font.render(score_text, True, COLOR_BLACK)
    rect = text.get_rect()
    if pos == 1:
      rect.topleft = (10, 10)
    else:
      rect.midtop = (self.width // 2, 100)
    self.board.blit(text, rect)

  def uiloop(self):
    t = 0
    terminated = False
    while True:
      if self.game is not None and self.game.active:
        for event in pygame.event.get():
          if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]:
              key = KEY_DICT[event.key]
              self.client.keypress(key)
              self.game.players[self.game.player_id].key(key)

            elif event.key == pygame.K_ESCAPE:
              self.client.term()
              pygame.event.post(pygame.event.Event(pygame.QUIT, dict={}))
              terminated = True

        if terminated:
          continue

        if AUTO_MODE and self.game.player_id is not None:
          player = self.game.players.get(self.game.player_id)
          if player is None:
            continue
          key = -1
          if player.direction == RIGHT and player.snake_head[0] == self.game.food_pos[0] - (POINT_SIZE):
            key = DOWN if player.snake_head[1] < self.game.food_pos[1] else UP
          elif player.direction == LEFT and player.snake_head[0] == self.game.food_pos[0] + (POINT_SIZE):
            key = DOWN if player.snake_head[1] < self.game.food_pos[1] else UP
          elif player.direction == UP and player.snake_head[1] == self.game.food_pos[1] + (POINT_SIZE):
            key = LEFT if player.snake_head[0] > self.game.food_pos[0] else RIGHT
          elif player.direction == DOWN and player.snake_head[1] == self.game.food_pos[1] - (POINT_SIZE):
            key = LEFT if player.snake_head[0] > self.game.food_pos[0] else RIGHT
          elif player.direction == RIGHT and player.snake_head[0] >= self.width - 50:
            key = DOWN
          elif player.direction == LEFT and player.snake_head[0] <= 50:
            key = UP
          elif player.direction == DOWN and player.snake_head[1] >= self.height - 50:
            key = LEFT
          elif player.direction == UP and player.snake_head[1] <= 50:
            key = RIGHT

          if key != -1:
            self.client.keypress(key)
            self.game.players[self.game.player_id].key(key)

        recently_set = self.game.get_recently_set()
        for player_id in self.game.players:
          player = self.game.players[player_id]
          if player.id not in recently_set:
            if player.direction == RIGHT:
              player.snake_head[0] += POINT_SIZE
            elif player.direction == LEFT:
              player.snake_head[0] -= POINT_SIZE
            elif player.direction == DOWN:
              player.snake_head[1] += POINT_SIZE
            elif player.direction == UP:
              player.snake_head[1] -= POINT_SIZE

            player.snake_body.insert(0, list(player.snake_head))
            player.snake_body.pop()

        self.board.fill(COLOR_WHITE)
        for player_id in self.game.players:
          player = self.game.players[player_id]
          for pos in player.snake_body:
            try:
              pygame.draw.rect(self.board, player.color, pygame.Rect(pos[0], pos[1], POINT_SIZE, POINT_SIZE))
            except:
              print('Invalid position: body=%s, pos=%s (recently set: %s)' % (str(player.snake_body), str(pos), player_id in recently_set))

        if self.game.food_pos is not None:
          pygame.draw.rect(self.board, COLOR_BROWN, pygame.Rect(self.game.food_pos[0], self.game.food_pos[1], POINT_SIZE, POINT_SIZE))
        else:
          _log.debug('No food...')

        self.showScore()
        pygame.display.flip()
        t = time.time()

      elif self.game is not None: # not active
        if time.time() - t < 4:
          for event in pygame.event.get():
            pass
          self.gameOver()
        else:
          break

      self.clock.tick(GAME_FPS)

    pygame.quit()
    sys.exit()

  def start(self):
    self.uiloop()


if __name__ == '__main__':
  for arg in sys.argv:
    if arg == '--help':
      print USAGE
      sys.exit(0)

  server_ip = '127.0.0.1'
  self_ip = '127.0.0.1'
  if len(sys.argv) > 1 and sys.argv[1] == 'AUTO':
    AUTO_MODE = True
    if len(sys.argv) > 2:
      server_ip = sys.argv[2]
  elif len(sys.argv) > 1:
    server_ip = sys.argv[1]

  client = SnakeClient(self_ip, server_ip)
  client.start()
