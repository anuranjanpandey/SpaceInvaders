import pygame
import random
import math
from pygame import mixer


class Player:
    def __init__(self, image=None, x=0, y=0, xchange=0, ychange=0):
        self.img = pygame.image.load(image)
        self.X = x
        self.Y = y
        self.X_change = xchange
        self.Y_change = ychange

    def getPlayer(self):
        return self.img, self.X, self.Y, self.X_change, self.Y_change


class Bullet:
    def __init__(self, image=None, x=0, y=0, xchange=0, ychange=0, state="ready"):
        self.img = pygame.image.load(image)
        self.X = x
        self.Y = y
        self.X_change = xchange
        self.Y_change = ychange
        self.state = state


class SpaceInvader:
    score_value = 0

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Space Invader")
        icon = pygame.image.load('ufo.png')
        pygame.display.set_icon(icon)
        self.background = pygame.image.load('background.png')
        mixer.music.load("background.wav")
        mixer.music.play(-1)

        self.player = Player('player.png', 370, 480, 0, 0)
        self.bullet = Bullet('bullet.png', 0, 480, 0, 10, "ready")
        self.num_of_enemies = 6
        self.enemies = [Player('enemy.png', random.randint(0, 736), random.randint(50, 150), 4, 40) for _ in
                        range(self.num_of_enemies)]

    def show_score(self, x, y):
        font = pygame.font.Font('freesansbold.ttf', 32)
        score = font.render("Score : " + str(SpaceInvader.score_value), True, (255, 255, 255))
        self.screen.blit(score, (x, y))

    def game_over_text(self):
        over_font = pygame.font.Font('freesansbold.ttf', 64)
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(over_text, (200, 250))

    def showPlayer(self, image, x, y):
        self.screen.blit(image, (x, y))

    def fire(self, x, y):
        self.bullet.state = "fire"
        self.screen.blit(self.bullet.img, (x + 16, y + 10))

    @staticmethod
    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False

    def play(self):
        running = True
        while running:

            # RGB = Red, Green, Blue
            self.screen.fill((0, 0, 0))
            # Background Image
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # if keystroke is pressed check whether its right or left
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.X_change = -5
                    if event.key == pygame.K_RIGHT:
                        self.player.X_change = 5
                    if event.key == pygame.K_SPACE:
                        if self.bullet.state is "ready":
                            bulletSound = mixer.Sound("laser.wav")
                            bulletSound.play()
                            # Get the current x cordinate of the spaceship
                            self.bullet.X = self.player.X
                            self.fire(self.bullet.X, self.bullet.Y)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.X_change = 0

            self.player.X += self.player.X_change
            if self.player.X <= 0:
                self.player.X = 0
            elif self.player.X >= 736:
                self.player.X = 736

            # Enemy Movement
            for i in range(self.num_of_enemies):

                # Game Over
                if self.enemies[i].Y > 440:
                    for j in range(self.num_of_enemies):
                        self.enemies[j].Y = 2000
                    self.game_over_text()
                    break

                self.enemies[i].X += self.enemies[i].X_change
                if self.enemies[i].X <= 0:
                    self.enemies[i].X_change = 4
                    self.enemies[i].Y += self.enemies[i].Y_change
                elif self.enemies[i].X >= 736:
                    self.enemies[i].X_change = -4
                    self.enemies[i].Y += self.enemies[i].Y_change

                # Collision
                collision = self.isCollision(self.enemies[i].X, self.enemies[i].Y, self.bullet.X, self.bullet.Y)
                if collision:
                    explosionSound = mixer.Sound("explosion.wav")
                    explosionSound.play()
                    self.bullet.Y = 480
                    self.bullet.state = "ready"
                    type(self).score_value += 1
                    self.enemies[i].X = random.randint(0, 736)
                    self.enemies[i].Y = random.randint(50, 150)

                self.showPlayer(self.enemies[i].img, self.enemies[i].X, self.enemies[i].Y)

            # Bullet Movement
            if self.bullet.Y <= 0:
                self.bullet.Y = 480
                self.bullet.state = "ready"

            if self.bullet.state is "fire":
                self.fire(self.bullet.X, self.bullet.Y)
                self.bullet.Y -= self.bullet.Y_change

            self.showPlayer(self.player.img, self.player.X, self.player.Y)
            self.show_score(10, 10)
            pygame.display.update()


if __name__ == "__main__":
    game = SpaceInvader()
    game.play()
