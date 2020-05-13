import pygame
import time
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'imagens')
snd_dir = path.join(path.dirname(__file__), 'sons')

WIDTH = 1344
HEIGHT = 704 
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

IDLE_FWD = 0
IDLE_RIGHT = 1
IDLE_BKD = 2
IDLE_LEFT = 3
FWD = 4
RIGHT = 5
BKD = 6
LEFT = 7
AIR = 8
GUN_FWD = 9
GUN_RIGHT = 10
GUN_BKD = 11
GUN_LEFT = 12
MARCH_FWD = 13
MARCH_RIGHT = 14
MARCH_BKD = 15
MARCH_LEFT = 16
HIT_FWD = 17
HIT_RIGHT = 18
HIT_BKD = 19
HIT_LEFT = 20
X = [RIGHT, LEFT]
Y = [FWD,BKD]
X_G = [GUN_RIGHT, GUN_LEFT]
Y_G = [GUN_FWD, GUN_BKD]
UNARMED = [IDLE_RIGHT, IDLE_LEFT, IDLE_FWD, IDLE_BKD]
ARMED = [GUN_RIGHT, GUN_LEFT, GUN_FWD, GUN_BKD]

ITEM = 0

o = 0
l = 1 
mapa = [
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,l,l,l,l,l,l],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,l],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,l],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,l],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,l],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,l],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,l]]

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        
        spritesheet =    [pygame.image.load(path.join(img_dir, "fwd.png")).convert(),
                          pygame.image.load(path.join(img_dir, "right.png")).convert(),
                          pygame.image.load(path.join(img_dir, "bkd.png")).convert(),
                          pygame.image.load(path.join(img_dir, "left.png")).convert(),
                          pygame.image.load(path.join(img_dir, "fwd0.png")).convert(),
                          pygame.image.load(path.join(img_dir, "fwd1.png")).convert(),
                          pygame.image.load(path.join(img_dir, "right0.png")).convert(),
                          pygame.image.load(path.join(img_dir, "right1.png")).convert(),
                          pygame.image.load(path.join(img_dir, "bkd0.png")).convert(),
                          pygame.image.load(path.join(img_dir, "bkd1.png")).convert(),
                          pygame.image.load(path.join(img_dir, "left0.png")).convert(),
                          pygame.image.load(path.join(img_dir, "left1.png")).convert(),
                          pygame.image.load(path.join(img_dir, "gun_fwd.png")).convert(),
                          pygame.image.load(path.join(img_dir, "gun_right.png")).convert(),
                          pygame.image.load(path.join(img_dir, "gun_bkd.png")).convert(),
                          pygame.image.load(path.join(img_dir, "gun_left.png")).convert(),
                          pygame.image.load(path.join(img_dir, "gun_fwd0.png")).convert(),
                          pygame.image.load(path.join(img_dir, "gun_fwd1.png")).convert(),
                          pygame.image.load(path.join(img_dir, "gun_right0.png")).convert(),
                          pygame.image.load(path.join(img_dir, "gun_right1.png")).convert(),
                          pygame.image.load(path.join(img_dir, "gun_bkd0.png")).convert(),
                          pygame.image.load(path.join(img_dir, "gun_bkd1.png")).convert(),
                          pygame.image.load(path.join(img_dir, "gun_left0.png")).convert(),
                          pygame.image.load(path.join(img_dir, "gun_left1.png")).convert(),
                          pygame.image.load(path.join(img_dir, "hit_fwd.png")).convert(),
                          pygame.image.load(path.join(img_dir, "hit_right.png")).convert(),
                          pygame.image.load(path.join(img_dir, "hit_bkd.png")).convert(),
                          pygame.image.load(path.join(img_dir, "hit_left.png")).convert(),
                          pygame.image.load(path.join(img_dir, "air.png")).convert()]         
        i = 0
        while i < len(spritesheet):
            if i < len(spritesheet) - 1:
                spritesheet[i] = pygame.transform.scale(spritesheet[i],(30,70))
                self.image = spritesheet[i]
                self.image.set_colorkey(WHITE)
            else:
                spritesheet[i] = pygame.transform.scale(spritesheet[i],(58,122))
                self.image = spritesheet[i]
                self.image.set_colorkey(WHITE)
            i += 1
        
        self.animations = {IDLE_FWD:spritesheet[0:1], 
                           IDLE_RIGHT:spritesheet[1:2], 
                           IDLE_BKD:spritesheet[2:3], 
                           IDLE_LEFT:spritesheet[3:4], 
                           FWD:spritesheet[4:6],
                           RIGHT:spritesheet[6:8],
                           BKD:spritesheet[8:10],
                           LEFT:spritesheet[10:12],
                           GUN_FWD:spritesheet[12:13],
                           GUN_RIGHT:spritesheet[13:14],
                           GUN_BKD:spritesheet[14:15],
                           GUN_LEFT:spritesheet[15:16],
                           MARCH_FWD:spritesheet[16:18],
                           MARCH_RIGHT:spritesheet[18:20],
                           MARCH_BKD:spritesheet[20:22],
                           MARCH_LEFT:spritesheet[22:24],
                           HIT_FWD:spritesheet[24:25],
                           HIT_RIGHT:spritesheet[25:26],
                           HIT_BKD:spritesheet[26:27],
                           HIT_LEFT:spritesheet[27:28],
                           AIR:spritesheet[28:29]}
        
        self.state = AIR
        self.animation = self.animations[self.state]
        self.frame = 0
        self.got = False
        self.fire = False
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 120
        self.rect.bottom = -20
        self.speedx = 0
        self.speedy = 2
        
        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 100
        
    def update(self):
        
        if self.state == AIR and self.rect.bottom == HEIGHT - 20:
            land_sound.play()
            self.state = IDLE_RIGHT
            self.speedy = 0
        
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_update
        if elapsed_ticks > self.frame_ticks:
            self.last_update = now
            self.frame += 1
            self.animation = self.animations[self.state]
            if self.frame >= len(self.animation):
                self.frame = 0
            center = self.rect.center
            self.image = self.animation[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
        
        if self.state == HIT_FWD and self.fire == False:
            if time.time() > self.time + .5:   
                print('IDLE_FWD')
                self.state = IDLE_FWD
        if self.fire == True:
            print('fire')
            if self.state == IDLE_FWD:
                self.time = time.time()
                print('IDLE_FWD')
                self.state = HIT_FWD
                self.fire = False
            else:
                print(self.state)
          
        keys = pygame.key.get_pressed() 
        if self.state == BKD:  
            if keys[pygame.K_s] == False:
                steps_sound.stop()
                self.speedy = 0
                self.speedx = 0
                self.state = IDLE_BKD
        if self.state == FWD:  
            if keys[pygame.K_w] == False:
                steps_sound.stop()
                self.speedy = 0
                self.speedx = 0
                self.state = IDLE_FWD
        if self.state == RIGHT:  
            if keys[pygame.K_d] == False:
                steps_sound.stop()
                self.speedy = 0
                self.speedx = 0
                self.state = IDLE_RIGHT
        if self.state == LEFT:  
            if keys[pygame.K_a] == False:
                steps_sound.stop()
                self.speedy = 0
                self.speedx = 0
                self.state = IDLE_LEFT
                
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
class Tile(pygame.sprite.Sprite):
    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        tile_img = pygame.image.load(path.join(img_dir, "sand.jpg")).convert()
        tile_img = pygame.transform.scale(tile_img, (TILESIZE, TILESIZE))
        self.image = tile_img
        self.rect = self.image.get_rect()
        self.rect.x = TILESIZE * column
        self.rect.y = TILESIZE * row
        
class Tree(pygame.sprite.Sprite):
    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        tile_img = pygame.image.load(path.join(img_dir, "tree.png")).convert()
        tile_img = pygame.transform.scale(tile_img, (TILESIZE, TILESIZE))
        self.image = tile_img
        self.rect = self.image.get_rect()
        self.rect.x = TILESIZE * column
        self.rect.y = TILESIZE * row

class Gun(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        door = pygame.image.load(path.join(img_dir, "gun.png")).convert()
        self.image = pygame.transform.scale(door, (50,50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH/2
        self.rect.y = HEIGHT/2
            
#class Item(pygame.sprite.Sprite):
#    def __init__(self):
#        pygame.sprite.Sprite.__init__(self)
#        itemsheet =    [pygame.image.load(path.join(img_dir, "fist.png")).convert(),
#                        pygame.image.load(path.join(img_dir, "gun.png")).convert()] 
#        i = 0
#        while i < len(itemsheet):
#            itemsheet[i] = pygame.transform.scale(itemsheet[i],(30,30))
#            self.image = itemsheet[i]
#            self.image.set_colorkey(WHITE)
#        
#        self.gun = False
#        self.image = itemsheet[0]
#        self.rect = self.image.get_rect()
#        self.rect.x = WIDTH/2
#        self.rect.y = HEIGHT/2
             
#    def update(self):
#        
#        if self.gun == True:
#            self.image = itemsheet[1]
            
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.display.set_caption("MG")
steps_sound = pygame.mixer.Sound(path.join(snd_dir, 'steps.wav'))
spotted_sound = pygame.mixer.Sound(path.join(snd_dir, 'spotted.ogg'))
land_sound = pygame.mixer.Sound(path.join(snd_dir, 'land.wav'))
cock_sound = pygame.mixer.Sound(path.join(snd_dir, 'cock.wav'))

def field_screen(screen):
    
    running = True  
    pygame.mixer.music.load(path.join(snd_dir, 'Evasion.mp3'))
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(loops=-1)
    row = len(mapa)
    column = len(mapa[0])
    tiles = pygame.sprite.Group()
    trees = pygame.sprite.Group()
    player = Player()
    gun = Gun()
#    item = Item()
    all_sprites = pygame.sprite.Group()
    for row in range(len(mapa)):
        for column in range(len(mapa[row])):
            tile_type = mapa[row][column]
            if tile_type == o:
                tile = Tile(row, column)
                all_sprites.add(tile)
                tiles.add(tile)
            elif tile_type == l:
                tree = Tree(row, column)
                all_sprites.add(tree)
                trees.add(tree)
    all_sprites.add(player)
    all_sprites.add(gun)
#    all_sprites.add(item)

    while running:
        
        clock.tick(FPS)
        for event in pygame.event.get():      
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:       
                if event.key == pygame.K_q:
                    running = False
                if player.state != AIR:
                    if player.state in UNARMED:
                        print(event.key)
                        if event.key == pygame.K_e and player.state not in X:
                            spotted_sound.play()
                            player.fire = True
                            
                        if event.key == pygame.K_s and player.state not in X:
                            steps_sound.play()
                            player.speedy = 5
                            player.state = BKD
                        if event.key == pygame.K_w and player.state not in X:
                            steps_sound.play()
                            player.speedy = -5
                            player.state = FWD
                        if event.key == pygame.K_d and player.state not in Y:
                            steps_sound.play()
                            player.speedx = 5
                            player.state = RIGHT
                        if event.key == pygame.K_a and player.state not in Y:
                            steps_sound.play()
                            player.speedx = -5
                            player.state = LEFT
                    elif player.state in ARMED:
                        if event.key == pygame.K_s and player.state not in X_G:
                            steps_sound.play()
                            player.speedy = 5
                            player.state = MARCH_BKD
                        if event.key == pygame.K_w and player.state not in X_G:
                            steps_sound.play()
                            player.speedy = -5
                            player.state = MARCH_FWD
                        if event.key == pygame.K_d and player.state not in Y_G:
                            steps_sound.play()
                            player.speedx = 5
                            player.state = MARCH_RIGHT
                        if event.key == pygame.K_a and player.state not in Y_G:
                            steps_sound.play()
                            player.speedx = -5
                            player.state = MARCH_LEFT
                    if event.key == pygame.K_p:
                        player.fire = True
        
        if player.state != AIR:
            collisions = pygame.sprite.spritecollide(player, trees, False)
            for collision in collisions:
                if player.speedx > 0:
                    player.rect.right = collision.rect.left
                elif player.speedx < 0:
                    player.rect.left = collision.rect.right
                if player.speedy > 0:
                    player.rect.bottom = collision.rect.top
                elif player.speedy < 0:
                    player.rect.top = collision.rect.bottom
            loot = pygame.sprite.collide_mask(player, gun)
            if loot != None and player.got == False:
                cock_sound.play()
                gun.kill()
                player.got = True
#                item.gun = True
                
        all_sprites.update()
        screen.fill(BLACK)
        all_sprites.draw(screen)       
        pygame.display.flip()
        
try:
    field_screen(screen)
finally:
    pygame.quit()