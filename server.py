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
from threading import Thread, Lock
from snake_types import *
import random
import struct
import os
import sys
import time
import pygame

logging.basicConfig()
_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)

USAGE = 'Usage: python server.py [SHOW]\n\t' \
        'SHOW: shows a graphical illustration of the server\'s view of the game\n\t' \
        '--help: shows this message (and quits)\n'


class SnakeServer:
  def __init__(self, port=SERVER_PORT, show_ui=False):
    self.port = port
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind(('0.0.0.0', self.port))
    self.nextPlayer = 0
    self.lock = Lock()
    self.connections = {}
    self.terminated = set()
    self.show_ui = show_ui
    self.game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, self)

  def _handle_conn(self, conn):
    # Initialize new player
    player_id = -1
    with self.lock:
      player_id = self.nextPlayer
      self.nextPlayer += 1

    _log.debug('Accepted connection for new player: %d' % player_id)

    player = ServerPlayer(player_id, self.game)
    self.game.players.append(player)
    self.connections[player_id] = conn

    self.send_events([PlayerJoinedEvent(player_id, player.snake_head, player.snake_body, player.direction, player.score)],
                     [player.id for player in self.game.players if player.id != player_id])

    evts_for_new_player = [PlayerJoinedEvent(player_id, player.snake_head, player.snake_body, player.direction, player.score, my_join=True),
                           FoodPositionChangeEvent(self.game.food_pos)] + \
                      [PlayerJoinedEvent(player.id, player.snake_head, player.snake_body, player.direction, player.score) \
                       for player in self.game.players if player.id != player_id]
    self.send_events(evts_for_new_player, [player_id])

    # This thread only reads from the socket. The gameloop thread writes updates to all sockets
    while player_id not in self.terminated:
      try:
        data = conn.recv(4)
        key, = struct.unpack('!I', data)
        if key == SIGTERM:
          _log.debug('Received TERM signal from player %d (voluntary termination)', player_id)
          raise Exception()
        _log.debug('Player %d pressed %s', player_id, keycode2text(key))
        self.game.keypressed(player_id, key)
      except Exception as e:
        # Dropped connection
        _log.debug('Player %d left the game', player_id)
        try:
          self.game.players.remove(player)
          self.send_events([PlayerTerminatedEvent(player_id)])
        except:
          pass
        break

  def send_events(self, events, player_ids=None):
    if player_ids is None:
      player_ids = [player.id for player in self.game.players]
    update = cPickle.dumps(events, cPickle.HIGHEST_PROTOCOL)
    length = len(update)
    data = struct.pack('!H', length) + update
    for pid in player_ids:
      conn = self.connections[pid]
      conn.send(data)

  def run(self):
    self.socket.listen(5)
    _log.debug('Server is running on port %d' % self.port)
    while True:
      try:
        conn, _ = self.socket.accept()
        t = Thread(target=self._handle_conn, kwargs={'conn': conn})
        t.setDaemon(True)
        t.start()
      except:
        break
    _log.debug('Server is stopped.')

  def start(self):
    self.thread = Thread(target=self.run)
    self.thread.setDaemon(True)
    self.thread.start()
    self.game.start()

  def join(self):
    self.thread.join()

  def stop(self):
    for pid in self.connections:
      try:
        self.connections[pid].close()
      except:
        pass
    try:
      self.socket.shutdown(socket.SHUT_RDWR)
      self.socket.close()
    except:
      pass
    _log.debug('Closed all sockets')


class ServerPlayer(Player):
  def __init__(self, id, board):
    super(ServerPlayer, self).__init__(id, 10)
    if id % 2 == 0:
      initX = random.randrange(100, (board.width - 50)) // POINT_SIZE * POINT_SIZE
      initY = random.randrange(50, board.height // 2) // POINT_SIZE * POINT_SIZE
      self.init_head = [initX, initY]
      self.init_body = [[initX, initY], [initX - 10, initY], [initX - 20, initY]]
      self.init_direction = RIGHT
    else:
      initX = random.randrange(50, (board.width - 100)) // POINT_SIZE * POINT_SIZE
      initY = random.randrange(board.height // 2, board.height - 50) // POINT_SIZE * POINT_SIZE
      self.init_head = [initX, initY]
      self.init_body = [[initX, initY], [initX + 10, initY], [initX + 20, initY]]
      self.init_direction = LEFT
    self.snake_head = self.init_head[:]
    self.snake_body = self.init_body[:]
    self.direction = self.init_direction
    self.color = COLOR_GREEN


class Game:
  def __init__(self, width, height, server):
    self.width, self.height = width, height
    self.food_pos = [(random.randint(50, self.width - 50) // POINT_SIZE) * POINT_SIZE,
                    (random.randint(50, self.height - 50) // POINT_SIZE) * POINT_SIZE]
    self.foodSpawn = True
    self.players = []
    self.active = True
    self.server = server
    pygame.init()
    self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
    if server.show_ui:
      self.screen = pygame.display.set_mode((self.width, self.height))
      pygame.display.set_caption("Snake Server")
    self.clock = pygame.time.Clock()

  def keypressed(self, player_id, key):
    player = self.players[player_id]
    direction = player.key(key)
    if direction is not None:
      self.server.send_events([PlayerDirectionChangeEvent(player_id, direction), PlayerDimensionsEvent(player_id, player.snake_head, player.snake_body)])

  def kill_player(self, player):
    evt = PlayerTerminatedEvent(player.id)
    self.server.send_events([evt], [p.id for p in self.players])
    self.players.remove(player)

  def die(self):
    self.active = False

  def show_text(self):
    font = pygame.font.SysFont('Helvetica', 14)
    score_text = '%d players connected. Hold ESC key for 3 seconds to quit.' % len(self.players)
    text = font.render(score_text, True, COLOR_BLACK)
    score_text = '  '.join([('Player %d: %d  ' % (player.id, player.score)) for player in self.players])
    text2 = font.render(score_text, True, COLOR_BLACK)
    rect = text.get_rect()
    rect.topleft = (10, 10)
    self.screen.blit(text, rect)
    rect2 = text2.get_rect()
    rect2.topleft = (10, 40)
    self.screen.blit(text2, rect2)

  def gameloop(self):
    esc_time = 0
    quit_now = False

    while self.active:
      events = []

      for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
          esc_time = time.time()
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
          if esc_time != 0 and time.time() - esc_time >= 3:
            _log.debug('Stopping server...')
            self.active = False
            self.server.stop()
            quit_now = True

      if quit_now:
        break

      if self.server.show_ui:
        self.screen.fill(COLOR_WHITE)

      for player in self.players:
        should_pop = True
        p2p_hit_checks = set()
        if player.direction == RIGHT:
          player.snake_head[0] += POINT_SIZE
        elif player.direction == LEFT:
          player.snake_head[0] -= POINT_SIZE
        elif player.direction == DOWN:
          player.snake_head[1] += POINT_SIZE
        elif player.direction == UP:
          player.snake_head[1] -= POINT_SIZE
        else:
          _log.error('Invalid snake direction: %s' % (keycode2text(player.direction) if player.direction is not None else 'None'))

        player.snake_body.insert(0, list(player.snake_head))
        if player.snake_head == self.food_pos:
          _log.debug('Player %d ate the food!' % player.id)
          self.foodSpawn = False
          player.score += 1
          _log.debug('Player %d score: %d' % (player.id, player.score))
          should_pop = False
          events.append(PlayerDimensionsEvent(player.id, player.snake_head, player.snake_body))
          events.append(PlayerScoreChangeEvent(player.id, player.score))

        if self.foodSpawn == False:
          self.food_pos = [(random.randint(50, self.width - 50) // POINT_SIZE) * POINT_SIZE,
                    (random.randint(50, self.height - 50) // POINT_SIZE) * POINT_SIZE]
          self.foodSpawn = True
          events.append(FoodPositionChangeEvent(self.food_pos))

        # Other-player hit
        for otherplayer in self.players:
          if otherplayer == player or (otherplayer, player) in p2p_hit_checks:
            continue
          p2p_hit_checks.add((player, otherplayer))
          for block in otherplayer.snake_body[1:]:
            if player.snake_head == block:
              _log.debug('Player %d ate player %d!' % (player.id, otherplayer.id))
              otherplayer.score -= 1
              _log.debug('Player %d score: %d' % (otherplayer.id, otherplayer.score))
              player.score += 1
              _log.debug('Player %d score: %d' % (player.id, player.score))
              should_pop = False
              if otherplayer.score < 0:
                self.kill_player(otherplayer)
                events.append(PlayerTerminatedEvent(otherplayer.id))
              else:
                otherplayer.reset()
                events.append(PlayerScoreChangeEvent(otherplayer.id, otherplayer.score))
                events.append(PlayerDimensionsEvent(otherplayer.id, otherplayer.snake_head, otherplayer.snake_body))
                events.append(PlayerDirectionChangeEvent(otherplayer.id, otherplayer.direction))
              events.append(PlayerDimensionsEvent(player.id, player.snake_head, player.snake_body))
              events.append(PlayerScoreChangeEvent(player.id, player.score))

        if should_pop:
          player.snake_body.pop()

        # Bounds
        if player.snake_head[0] >= self.width or player.snake_head[0] < 0 or player.snake_head[1] >= self.height or \
           player.snake_head[1] < 0:
          _log.debug('Player %d hit bounds!' % player.id)
          player.score -= 1
          _log.debug('Player %d score: %d' % (player.id, player.score))
          if player.score < 0:
            self.kill_player(player)
            events.append(PlayerTerminatedEvent(player.id))
          else:
            player.reset()
            events.append(PlayerScoreChangeEvent(player.id, player.score))
            events.append(PlayerDimensionsEvent(player.id, player.snake_head, player.snake_body))
            events.append(PlayerDirectionChangeEvent(player.id, player.direction))

        # Self hit
        for block in player.snake_body[1:]:
          if player.snake_head == block:
            _log.debug('Player %d hit itself! (head: %s, body: %s)' % (player.id, player.snake_head, player.snake_body))
            player.score -= 1
            _log.debug('Player %d score: %d' % (player.id, player.score))
            if player.score < 0:
              self.kill_player(player)
              events.append(PlayerTerminatedEvent(player.id))
            else:
              player.reset()
              events.append(PlayerScoreChangeEvent(player.id, player.score))
              events.append(PlayerDimensionsEvent(player.id, player.snake_head, player.snake_body))
              events.append(PlayerDirectionChangeEvent(player.id, player.direction))

        if self.server.show_ui:
          for player in self.players:
            for pos in player.snake_body:
              try:
                pygame.draw.rect(self.screen, player.color, pygame.Rect(pos[0], pos[1], POINT_SIZE, POINT_SIZE))
              except:
                print('Invalid position: body=%s, pos=%s' % (str(player.snake_body), str(pos)))

        if self.server.show_ui and self.food_pos is not None:
          pygame.draw.rect(self.screen, COLOR_BROWN, pygame.Rect(self.food_pos[0], self.food_pos[1], POINT_SIZE, POINT_SIZE))

      if self.server.show_ui:
        self.show_text()
        pygame.display.flip()

      if len(events) > 0:
        _log.debug('Sending %d events' % len(events))
        self.server.send_events(events)
      self.clock.tick(GAME_FPS)

    pygame.quit()
    sys.exit()

  def start(self):
    self.gameloop()

  def join(self):
    pass


if __name__ == '__main__':
  for arg in sys.argv:
    if arg == '--help':
      print USAGE
      sys.exit(0)

  show_ui = False
  if len(sys.argv) > 1 and sys.argv[1] == 'SHOW':
    os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
    show_ui = True
  server = SnakeServer(show_ui=show_ui)
  server.start()
