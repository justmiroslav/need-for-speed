import pgzrun
import pygame as pg
from pgzero.actor import Actor
import math
import time
# import of necessary components
background = pg.image.load("background.jpg")
WIDTH = background.get_width()/1.5
HEIGHT = background.get_height()/1.5
finish = pg.image.load("finish_line.png")
line = pg.transform.rotate(finish, 90)
finish_line = pg.transform.scale(line, (120, HEIGHT))
# loading + initialization of background and finish line
game_win = False
game_win_update = False
game_over = False
game_over_update = False
game_draw = False
# Boolean values that will be needed soon


class Car:
    def __init__(self):
        self.image = Actor("car")
        self.x = 55
        self.y = HEIGHT - 40
        self.angle = 0
        self.speed = 0
        # initialization of the car

    def update(self):
        global game_draw
        if keyboard.a:
            self.angle += 3
        if keyboard.s:
            self.speed = -5
            self.x -= math.sin(math.radians(self.angle)) * self.speed
            self.y -= math.cos(math.radians(self.angle)) * self.speed
        if keyboard.w:
            self.speed = 5
            self.x -= math.sin(math.radians(self.angle)) * self.speed
            self.y -= math.cos(math.radians(self.angle)) * self.speed
        if keyboard.d:
            self.angle -= 3
        self.image.angle = self.angle
        self.image.pos = (self.x, self.y)
        # changes of the angles and the speed based on the key pressed
        if self.x - 40 < 0:
            self.x = 40
        if self.y + 40 > HEIGHT:
            self.y = HEIGHT - 40
        elif self.y - 40 < 0:
            self.y = 40
        # checking that car doesn't move out of the screen
        if self.x > WIDTH - 50:
            global game_win
            game_win = True
            game_draw = True
        # collision between car and finish line, changing the values to true
        for wall in walls:
            if wall.collide(self.image):
                global game_over
                game_over = True
                game_draw = True
        # collision between car and rocks, also changing the values

    def draw(self):
        self.image.draw()
        # drawing a car


class Rock:
    def __init__(self, x, y):
        self.image = Actor("rock")
        self.x = x
        self.y = y
        self.image.pos = (self.x, self.y)
        # initialization of the rock, for this I also use Actor

    def draw(self):
        self.image.draw()
        # drawing a rock

# the next 2 class are about making a wall from the rocks, I loaded earlier
# class Wide make the horizontal walls and High - vertical


class Wide:
    def __init__(self, x, y, width):
        self.rocks = []
        for a in range(x, x + width, 50):
            self.rocks.append(Rock(a, y))
        # initializing the wall, using arguments from outer scope

    def draw(self):
        for rock in self.rocks:
            rock.draw()
        # drawing a wall

    def collide(self, rect):
        for rock in self.rocks:
            if rect.colliderect(rock.image):
                return True
        return False
        # condition for collision with car

# same logic for class High


class High:
    def __init__(self, x, y, height):
        self.rocks = []
        for o in range(y, y + height, 50):
            self.rocks.append(Rock(x, o))

    def draw(self):
        for rock in self.rocks:
            rock.draw()

    def collide(self, rect):
        for rock in self.rocks:
            if rect.colliderect(rock.image):
                return True
        return False


car = Car()
w1 = Wide(20, 20, 1250)  # for horizontal walls arguments are (x, y, width)
w2 = Wide(120, 700, 1150)
w3 = High(120, 200, 500)  # for vertical walls arguments are (x, y, width)
w4 = High(270, 250, 150)
w5 = Wide(270, 500, 300)
w6 = Wide(270, 300, 400)
w7 = High(570, 350, 250)
w8 = High(420, 70, 150)
w9 = Wide(570, 450, 150)
w10 = High(570, 250, 100)
w11 = High(770, 70, 450)
w12 = Wide(720, 120, 50)
w13 = Wide(720, 520, 150)
w14 = High(1020, 350, 400)
w15 = Wide(970, 400, 50)
w16 = Wide(1020, 170, 200)
w17 = High(1220, 70, 500)
# making examples of the class
walls = [w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17]
# also making a list of walls to operate them easily


def draw():
    # drawing and layering objects
    screen.blit(background, (0, 0))
    screen.blit(finish_line, (WIDTH-120, 0))
    if not game_draw:  # Boolean values with changed meaning
        for wall in walls:
            wall.draw()
        car.draw()
    if game_win:
        # text drawn if player wins
        screen.draw.text("YOU WON!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="white")
        global game_win_update
        game_win_update = True
    if game_over:
        # text drawn if player loses
        screen.draw.text("Game Over!", center=(WIDTH // 2, HEIGHT // 2), fontsize=60, color="white")
        global game_over_update
        game_over_update = True


def update():
    # updating car position
    car.update()
    if game_win_update or game_over_update:  # quiting the game after some time if we win or lose
        time.sleep(1.2)
        pg.quit()


pgzrun.go()
