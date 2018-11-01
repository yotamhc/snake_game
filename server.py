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
import hashlib
import concurrent.futures

logging.basicConfig()
_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)

USAGE = 'Usage: python server.py [SHOW]\n\t' \
        'SHOW: shows a graphical illustration of the server\'s view of the game\n\t' \
        '--help: shows this message (and quits)\n'


class SnakeServer(snake_pb2_grpc.SnakeServerServicer):
  def __init__(self, show_ui=False):
    self.nextPlayer = 0
    self.lock = Lock()
    self.sig_to_id = {}
    self.connections = {}
    self.terminated = set()
    self.show_ui = show_ui
    self.game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, self)
    self.events_awaiting = {}

  def JoinGame(self, request, context):
    return self._handle_conn(request)

  def KeyPress(self, request, context):
    player_id = self.sig_to_id.get(request.signature)
    if player_id is not None and player_id not in self.terminated:
      key = request.key
      if key == SIGTERM:
        _log.debug('Received TERM signal from player %d (voluntary termination)', player_id)
        _log.debug('Player %d left the game', player_id)
        player = [player for player in self.game.players if player.id == player_id][0]
        return self.game.kill_player(player)
      else:
        _log.debug('Player %d pressed %s', player_id, keycode2text(key))
        return self.game.keypressed(player_id, key)
    else:
      return snake_pb2.Events()

  def Poll(self, request, context):
    player_id = self.sig_to_id[request.signature]
    res = snake_pb2.Events()
    events = list(self.events_awaiting[player_id])
    for e in events:
      self.events_awaiting[player_id].remove(e)
    evts_proto = [wrap_event(evt) for evt in events]
    res.events.extend(evts_proto)
    return res

  def _handle_conn(self, conn):
    # Initialize new player
    player_id = -1
    with self.lock:
      player_id = self.nextPlayer
      self.nextPlayer += 1

    signature = hashlib.sha1(str(player_id)).hexdigest()
    self.sig_to_id[signature] = player_id
    self.events_awaiting[player_id] = []

    _log.debug('Accepted connection for new player: %d' % player_id)

    player = ServerPlayer(player_id, self.game)
    self.game.players.append(player)

    self.send_events([snake_pb2.PlayerJoinedEvent(player_id=player_id, player_pos=to_proto_pos(player.snake_head),
                                                  player_body=to_proto_pos(player.snake_body), direction=player.direction,
                                                  score=player.score, my_join=False)],
                     [player.id for player in self.game.players if player.id != player_id])

    evts_for_new_player = [snake_pb2.PlayerJoinedEvent(player_id=player_id, player_pos=to_proto_pos(player.snake_head),
                                                  player_body=to_proto_pos(player.snake_body), direction=player.direction,
                                                  score=player.score, my_join=True),
                           snake_pb2.FoodPositionChangeEvent(food_pos=to_proto_pos(self.game.food_pos))] + \
                        [snake_pb2.PlayerJoinedEvent(player_id=p.id, player_pos=to_proto_pos(p.snake_head),
                                                    player_body=to_proto_pos(p.snake_body), direction=p.direction,
                                                    score=p.score, my_join=False)
                         for p in self.game.players if p.id != player_id]
    res = snake_pb2.Events(signature=signature)
    res.events.extend([wrap_event(evt) for evt in evts_for_new_player])
    return res

  def send_events(self, events, player_ids=None):
    if player_ids is None:
      player_ids = [player.id for player in self.game.players]
    elif len(player_ids) == 0:
      return

    _log.debug('Sending %d events to %d players' % (len(events), len(player_ids)))

    for player_id in player_ids:
      self.events_awaiting[player_id].extend(events)

  def start(self):
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    snake_pb2_grpc.add_SnakeServerServicer_to_server(self, server)
    server.add_insecure_port('[::]:%d' % SERVER_PORT)
    server.start()
    self.game.start()

  def stop(self):
    _log.debug('Server is stopped.')
    pass

  # def run(self):
  #   self.socket.listen(5)
  #   _log.debug('Server is running on port %d' % self.port)
  #   while True:
  #     try:
  #       conn, _ = self.socket.accept()
  #       t = Thread(target=self._handle_conn, kwargs={'conn': conn})
  #       t.setDaemon(True)
  #       t.start()
  #     except:
  #       break
  #   _log.debug('Server is stopped.')

  # def start(self):
  #   self.thread = Thread(target=self.run)
  #   self.thread.setDaemon(True)
  #   self.thread.start()
  #   self.game.start()

  # def join(self):
  #   self.thread.join()

  # def stop(self):
  #   for pid in self.connections:
  #     try:
  #       self.connections[pid].close()
  #     except:
  #       pass
  #   try:
  #     self.socket.shutdown(socket.SHUT_RDWR)
  #     self.socket.close()
  #   except:
  #     pass
  #   _log.debug('Closed all sockets')


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
    self.food_ready = True
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
      evts = [snake_pb2.PlayerDirectionChangeEvent(player_id=player_id, direction=direction),
             snake_pb2.PlayerDimensionsEvent(player_id=player_id,
                                             player_pos=to_proto_pos(player.snake_head),
                                             player_body=to_proto_pos(player.snake_body))]
      self.server.send_events(evts, [player.id for player in self.players if player.id != player_id])
      res = snake_pb2.Events()
      res.events.extend([wrap_event(e) for e in evts])
      return res

  def kill_player(self, player):
    evt = snake_pb2.PlayerTerminatedEvent(player_id=player.id)
    self.server.send_events([evt], [p.id for p in self.players if p.id != player.id])
    self.players.remove(player)
    res = snake_pb2.Events()
    res.events.extend([wrap_event(evt)])
    return res

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
        if self.food_ready and player.snake_head == self.food_pos:
          _log.debug('Player %d ate the food!' % player.id)
          self.food_ready = False
          player.score += 1
          _log.debug('Player %d score: %d' % (player.id, player.score))
          should_pop = False
          events.append(snake_pb2.PlayerDimensionsEvent(player_id=player.id,
                                                        player_pos=to_proto_pos(player.snake_head),
                                                        player_body=to_proto_pos(player.snake_body)))
          events.append(snake_pb2.PlayerScoreChangeEvent(player_id=player.id, score=player.score))

        if not self.food_ready:
          self.food_pos = [(random.randint(50, self.width - 50) // POINT_SIZE) * POINT_SIZE,
                    (random.randint(50, self.height - 50) // POINT_SIZE) * POINT_SIZE]
          self.food_ready = True
          events.append(snake_pb2.FoodPositionChangeEvent(food_pos=to_proto_pos(self.food_pos)))

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
                events.append(snake_pb2.PlayerTerminatedEvent(player_id=otherplayer.id))
              else:
                otherplayer.reset()
                events.append(snake_pb2.PlayerScoreChangeEvent(player_id=otherplayer.id, score=otherplayer.score))
                events.append(snake_pb2.PlayerDimensionsEvent(player_id=otherplayer.id,
                                                              player_pos=to_proto_pos(otherplayer.snake_head),
                                                              player_body=to_proto_pos(otherplayer.snake_body)))
                events.append(snake_pb2.PlayerDirectionChangeEvent(player_id=otherplayer.id,
                                                                   direction=otherplayer.direction))
              events.append(snake_pb2.PlayerDimensionsEvent(player_id=player.id,
                                                            player_pos=to_proto_pos(player.snake_head),
                                                            player_body=to_proto_pos(player.snake_body)))
              events.append(snake_pb2.PlayerScoreChangeEvent(player_id=player.id, score=player.score))

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
            events.append(snake_pb2.PlayerTerminatedEvent(player_id=player.id))
          else:
            player.reset()
            events.append(snake_pb2.PlayerScoreChangeEvent(player_id=player.id, score=player.score))
            events.append(snake_pb2.PlayerDimensionsEvent(player_id=player.id,
                                                          player_pos=to_proto_pos(player.snake_head),
                                                          player_body=to_proto_pos(player.snake_body)))
            events.append(snake_pb2.PlayerDirectionChangeEvent(player_id=player.id, direction=player.direction))

        # Self hit
        for block in player.snake_body[1:]:
          if player.snake_head == block:
            _log.debug('Player %d hit itself! (head: %s, body: %s)' % (player.id, player.snake_head, player.snake_body))
            player.score -= 1
            _log.debug('Player %d score: %d' % (player.id, player.score))
            if player.score < 0:
              self.kill_player(player)
              events.append(snake_pb2.PlayerTerminatedEvent(player_id=player.id))
            else:
              player.reset()
              events.append(snake_pb2.PlayerScoreChangeEvent(player_id=player.id, score=player.score))
              events.append(snake_pb2.PlayerDimensionsEvent(player_id=player.id,
                                                            player_pos=to_proto_pos(player.snake_head),
                                                            player_body=to_proto_pos(player.snake_body)))
              events.append(snake_pb2.PlayerDirectionChangeEvent(player_id=player.id, direction=player.direction))

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
