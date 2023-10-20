# content from kids can code: http://kidscancode.org/blog/

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
from random import randint
import os 
from settings import *

vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
snd_folder = os.path.join(game_folder, 'sounds')



def draw_text(text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    screen.blit(text_surface, text_rect)

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # self.image = pg.Surface((50, 50))
        # self.image.fill(GREEN)
        # use an image for player sprite...
        self.image = pg.image.load(os.path.join(img_folder, 'theBell.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        print(self.rect.center)
        self.hitpoints = 100
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_SPACE]:
            self.jump()
    def jump(self):
        hits = pg.sprite.spritecollide(self, all_platforms, False)
        if hits:
            print("i can jump")
            self.vel.y = -PLAYER_JUMP
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # if friction - apply here
        self.acc.x += self.vel.x * -0.2
        # this would only apply when doing a top down video game
        # self.acc.y += self.vel.y * -0.2
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

# platforms

class Platform(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        print(self.rect.center)
        self.category = category
        self.speed = 0
        if self.category == "moving":
            self.speed = 5
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x > WIDTH or self.rect.x < 0:
                self.speed = -self.speed
        if self.category == "lava":
            self.image.fill(ORANGE)

class Mob(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        print(self.rect.center)
        self.category = category
        self.speed = 0
        if self.category == "moving":
            self.speed = 20
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            # check to see if this thing is on one side of the screen or the other
            if self.rect.x > WIDTH or self.rect.x < 0:
                self.speed = -self.speed
                self.rect.y += self.rect.h
            if self.rect.x > WIDTH/2:
                self.image.fill(ORANGE)
            else:
                self.image.fill((randint(0,255), randint(0,255), randint(0,255)))



# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")

clock = pg.time.Clock()

# create a group for all sprites
all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
all_mobs = pg.sprite.Group()

# instantiate classes
player = Player()
plat = Platform(150, 300, 100, 30, " ")
plat1 = Platform(200, 200, 100, 30, "moving")
plat2 = Platform(250, 100, 100, 30, "moving")
plat3 = Platform(10, 50, 100, 30, "lava")

# add instances to groups
all_sprites.add(player)
all_sprites.add(plat)
all_sprites.add(plat1)
all_sprites.add(plat2)
all_sprites.add(plat3)
all_platforms.add(plat)
all_platforms.add(plat1)
all_platforms.add(plat2)
all_platforms.add(plat3)

# for i in range(0,10):
#     p = Platform(randint(0,WIDTH), randint(0,HEIGHT), 100, 30, "moving")
#     all_sprites.add(p)
#     all_platforms.add(p)

for i in range(0,10):
    m = Mob(randint(0,WIDTH), randint(0,HEIGHT), 25, 25, "moving")
    all_sprites.add(m)
    all_mobs.add(m)

for plat in PLATFORM_LIST:
    p = Platform(*plat)
    all_sprites.add(p)
    all_platforms.add(p)

# Game loop
running = True
while running:
    # keep the loop running using clock
    currentFPS = clock.tick(FPS)
        
    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
    
    ############ Update ##############
    # update all sprites
    all_sprites.update()
    if player.rect.y > HEIGHT:
        player.pos = vec(WIDTH/2, HEIGHT/2)
    # this is what prevents the player from falling through the platform when falling down...
    if player.vel.y > 0:
            hits = pg.sprite.spritecollide(player, all_platforms, False)
            if hits:
                player.pos.y = hits[0].rect.top
                player.vel.y = 0
                player.vel.x = hits[0].speed*1.5
                
    # this prevents the player from jumping up through a platform
    if player.vel.y < 0:
        hits = pg.sprite.spritecollide(player, all_platforms, False)
        if hits:
            print("ouch")
            SCORE -= 1
            if player.rect.bottom >= hits[0].rect.top - 5:
                player.rect.top = hits[0].rect.bottom
                player.acc.y = 5
                player.vel.y = 0

    mhits = pg.sprite.spritecollide(player, all_mobs, False)
    if mhits:
        player.hitpoints -= 10
    ############ Draw ################
    # draw the background screen
    screen.fill(BLACK)
    # draw all sprites
    all_sprites.draw(screen)
    draw_text("FPS: " + str(currentFPS), 22, WHITE, WIDTH/2, HEIGHT/10)
    draw_text("Hitpoints: " + str(player.hitpoints), 22, WHITE, WIDTH/2, HEIGHT/20)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()
