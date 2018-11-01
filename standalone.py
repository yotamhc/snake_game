import pygame
import sys
import time
import random
from threading import Thread

COLOR_RED = pygame.Color(255, 0, 0)
COLOR_GREEN = pygame.Color(0, 255, 0)
COLOR_BLUE = pygame.Color(0, 0, 255)
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_BROWN = pygame.Color(165, 42, 42)

POINT_SIZE = 10


class UiBoard:
  def __init__(self, width, height, game):
    pygame.init()
    self.width, self.height = width, height
    self.board = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake")

    self.clock = pygame.time.Clock()

    self.game = game

  def gameOver(self):
    self.board.fill(COLOR_WHITE)
    myFont = pygame.font.SysFont('Helvetica', 72)
    GOsurf = myFont.render("Game Over", True, COLOR_RED)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (320, 25)
    self.board.blit(GOsurf, GOrect)
    self.showScore(0)
    pygame.display.flip()

  def showScore(self, pos=1):
    font = pygame.font.SysFont('Helvetica', 24)
    text = font.render("Player 1: {0}  Player 2: {1}".format(self.game.players[0].score, self.game.players[1].score), True, COLOR_BLACK)
    rect = text.get_rect()
    if pos == 1:
      rect.midtop = (150, 10)
    else:
      rect.midtop = (320, 100)
    self.board.blit(text, rect)

  def uiloop(self):
    t = 0
    while True:
      if self.game.active:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
          elif event.type == pygame.KEYDOWN:
            p = -1
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]:
              p = 0
            elif event.key in [pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s]:
              p = 1
            if p in [0, 1]:
              self.game.keypressed(p, event)

            if event.key == pygame.K_ESCAPE:
              self.game.die()
              pygame.event.post(pygame.event.Event(pygame.QUIT))

        self.board.fill(COLOR_WHITE)
        for player in self.game.players:
          for pos in player.snakeBody:
            pygame.draw.rect(self.board, player.color, pygame.Rect(pos[0], pos[1], POINT_SIZE, POINT_SIZE))

        pygame.draw.rect(self.board, COLOR_BROWN, pygame.Rect(self.game.foodPos[0], self.game.foodPos[1], POINT_SIZE, POINT_SIZE))

        self.showScore()
        pygame.display.flip()
        t = time.time()

      else: # not active
        if time.time() - t < 4:
          for event in pygame.event.get():
            pass
          self.gameOver()
        else:
          break

      self.clock.tick(self.game.fps)

    pygame.quit()
    sys.exit()

  def start(self):
    self.uiloop()


class Game:
  def __init__(self, width, height):
    self.players = [Player(), Player(False)]
    self.active = True
    self.width, self.height = width, height
    self.foodPos = [(random.randint(100, self.width - 100) // POINT_SIZE) * POINT_SIZE,
               (random.randint(100, self.height - 100) // POINT_SIZE) * POINT_SIZE]
    self.foodSpawn = True
    self.fps = 10

  def keypressed(self, player, key):
    self.players[player].key(key)

  def die(self):
    self.active = False

  def gameloop(self):
    while self.active:
      for player in self.players:
        should_pop = True
        if player.direction == 'RIGHT':
          player.snakePos[0] += POINT_SIZE
        if player.direction == 'LEFT':
          player.snakePos[0] -= POINT_SIZE
        if player.direction == 'DOWN':
          player.snakePos[1] += POINT_SIZE
        if player.direction == 'UP':
          player.snakePos[1] -= POINT_SIZE

        player.snakeBody.insert(0, list(player.snakePos))
        if player.snakePos == self.foodPos:
          self.foodSpawn = False
          player.score += 1
          should_pop = False

        if self.foodSpawn == False:
          self.foodPos = [random.randrange(1, self.width // POINT_SIZE) * POINT_SIZE, random.randrange(1, self.height // POINT_SIZE) * POINT_SIZE]
          self.foodSpawn = True

        # Other-player hit
        otherplayer = self.players[0] if self.players[0] == player else self.players[1]
        for block in otherplayer.snakeBody[1:]:
          if player.snakePos == block:
            otherplayer.score -= 1
            player.score += 1
            should_pop = False
            if otherplayer.score < 0:
              self.active = False
              break
            else:
              otherplayer.reset()

        if should_pop:
          player.snakeBody.pop()

        # Bounds
        if player.snakePos[0] >= self.width or player.snakePos[0] < 0 or player.snakePos[1] >= self.height or player.snakePos[1] < 0:
          player.score -= 1
          if player.score < 0:
            self.active = False
            break
          else:
            player.reset()

        # Self hit
        for block in player.snakeBody[1:]:
          if player.snakePos == block:
            player.score -= 1
            if player.score < 0:
              self.active = False
              break
            else:
              player.reset()
      time.sleep(1.0 / self.fps)

  def start(self):
    self.thread = Thread(target=self.gameloop)
    self.thread.start()
    ui = UiBoard(self.width, self.height, self)
    ui.start()

  def join(self):
    self.thread.join()


if __name__ == "__main__":
  game = Game(640, 480)
  game.start()


class Player:
  def __init__(self, uses_arrows=True):
    self.score = 3
    if uses_arrows:
      self.color = COLOR_GREEN
      self.initPos = [100, 50]
      self.initBody = [[100, 50], [90, 50], [80, 50]]
      self.initDirection = 'RIGHT'
      self.right_key = pygame.K_RIGHT
      self.left_key = pygame.K_LEFT
      self.up_key = pygame.K_UP
      self.down_key = pygame.K_DOWN
    else:
      self.color = COLOR_BLUE
      self.initPos = [300, 400]
      self.initBody = [[300, 400], [290, 400], [280, 400]]
      self.initDirection = 'LEFT'
      self.right_key = pygame.K_d
      self.left_key = pygame.K_a
      self.up_key = pygame.K_w
      self.down_key = pygame.K_s
    self.snakePos = self.initPos[:]
    self.snakeBody = self.initBody[:]
    self.direction = self.initDirection
    self.uses_arrows = uses_arrows

  def key(self, event):
    changeto = None
    if event.key == self.right_key:
      changeto = 'RIGHT'
    if event.key == self.left_key:
      changeto = 'LEFT'
    if event.key == self.up_key:
      changeto = 'UP'
    if event.key == self.down_key:
      changeto = 'DOWN'

    if changeto == 'RIGHT' and self.direction != 'LEFT':
      self.direction = changeto
    if changeto == 'LEFT' and self.direction != 'RIGHT':
      self.direction = changeto
    if changeto == 'UP' and self.direction != 'DOWN':
      self.direction = changeto
    if changeto == 'DOWN' and self.direction != 'UP':
      self.direction = changeto

  def reset(self):
    self.snakePos = self.initPos[:]
    self.snakeBody = self.initBody[:]
    self.direction = self.initDirection
