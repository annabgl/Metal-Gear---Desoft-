# Importando as bibliotecas desnecessárias
import pygame
import random
from os import path

# carregando nossas pastas de imagens e sons
img_dir = path.join(path.dirname(__file__), 'imagens')
snd_dir = path.join(path.dirname(__file__), 'sons')

# Declarando variáveis necessárias
WIN = pygame.display.set_mode((500,480))
WIDTH = 1344
HEIGHT = 704 
FPS = 60
HEALTH = 100
HEALTH_ENEMY = 100
WAVE_NUMBER = 1

# Setando as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Guardando posições das Sprites
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

# listas de sprites
X = [RIGHT, LEFT]
Y = [FWD,BKD]
X_G = [GUN_RIGHT, GUN_LEFT]
Y_G = [GUN_FWD, GUN_BKD]
UNARMED = [IDLE_RIGHT, IDLE_LEFT, IDLE_FWD, IDLE_BKD]
ARMED = [GUN_RIGHT, GUN_LEFT, GUN_FWD, GUN_BKD]
MARCH= [MARCH_BKD, MARCH_FWD, MARCH_LEFT, MARCH_RIGHT]


life_bar = None

ITEM = 0

# Desenhando Mapa
o = 0
l = 1 
mapa = [
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,l,l,l,l,l,l,l],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,l],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,l],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,l],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,l],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,l],
       [o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,o,l]]

# Funcão que desenha a barra de vida
def draw_lifebar(surf, x_b, y_l , pct):
    global life_bar
    if(life_bar is None):    
        life_bar = pygame.image.load(path.join(img_dir,"lifebar.png")).convert_alpha()
    if pct < 0:
        pct = 0
    bar_length = 238
    bar_height = 10 
    fill = pct * bar_length
    fill_rect = pygame.Rect(x_b+40, y_l+28, fill, bar_height)
    if pct > 0.6:
        color = GREEN
    elif pct > 0.3:
        color = YELLOW
    else:
        color = RED
    pygame.draw.rect(surf, color, fill_rect)
    surf.blit(life_bar,(x_b,y_l))

# Função que troca a imagem da barra de vida
def draw_weapon(surf,x,y,img):
    weapon = img
    weapon=pygame.transform.scale(weapon, (38, 37))
    surf.blit(weapon,(x,y))
    

# Classe do nosso jogador   
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        
        # Guardando nossas imagens em uma lista 
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
        
        # Carrega Animação de acordo com as Sprites
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
        
        #Declarando Variáveis do Player
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
        self.health = HEALTH
        
        
        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 100
    
    # Função que atualiza o movimento do Jogador    
    def update(self):
        
        if self.state == AIR and self.rect.bottom == HEIGHT - 20:
            land_sound.play()
            self.state = IDLE_RIGHT
            self.speedx = 0
            self.speedy = 0
        
        now = pygame.time.get_ticks()
        elapsed_ticks = now - self.last_update
        if elapsed_ticks > self.frame_ticks:
            self.last_update = now
            self.frame += 1
            self.animation = self.animations[self.state]
            if self.frame >= len(self.animation):
                self.frame = 0
                if self.state == HIT_FWD:
                    self.state = IDLE_FWD
                if self.state == HIT_LEFT:
                    self.state = IDLE_LEFT
                if self.state == HIT_BKD:
                    self.state = IDLE_BKD
                if self.state == HIT_RIGHT:
                    self.state = IDLE_RIGHT
            center = self.rect.center
            self.image = self.animation[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
        

        if self.fire == True:
            if self.state == IDLE_FWD:
                self.state = HIT_FWD
                self.fire = False
            if self.state == IDLE_BKD:
                self.state = HIT_BKD
                self.fire = False
            if self.state == IDLE_RIGHT:
                self.state = HIT_RIGHT
                self.fire = False
            if self.state == IDLE_LEFT:
                self.state = HIT_LEFT
                self.fire = False
            else:
                pass
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
    
    # Função que Desenha a vida a medida que ele vai perdendo    
    def lifebar(self):
        if self.life > 60:
            color = GREEN
        elif self.life > 30:
            color = YELLOW
        else:
            color = RED
        width = int(self.rect.width * self.health / 100)
        self.health = pygame.Rect(0, 0, width, 7)
        if self.life < 100:
            pygame.draw.rect(self.image, color, self.health)

# Função que Desenha a areia         
class Tile(pygame.sprite.Sprite):
    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        tile_img = pygame.image.load(path.join(img_dir, "sand.jpg")).convert()
        tile_img = pygame.transform.scale(tile_img, (TILESIZE, TILESIZE))
        self.image = tile_img
        self.rect = self.image.get_rect()
        self.rect.x = TILESIZE * column
        self.rect.y = TILESIZE * row

# Função que desenha a árvore        
class Tree(pygame.sprite.Sprite):
    def __init__(self, row, column):
        pygame.sprite.Sprite.__init__(self)
        tile_img = pygame.image.load(path.join(img_dir, "tree.png")).convert()
        tile_img = pygame.transform.scale(tile_img, (TILESIZE, TILESIZE))
        self.image = tile_img
        self.rect = self.image.get_rect()
        self.rect.x = TILESIZE * column
        self.rect.y = TILESIZE * row

# Função que define uma parede imaginária        
class Wall():
    def __init__(self, x, y, WIDTH, HEIGHT):  
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)

# Função que Carrega a imagem da nossa arma 
class Gun(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        door = pygame.image.load(path.join(img_dir, "gun.png")).convert()
        self.image = pygame.transform.scale(door, (50,50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH/2
        self.rect.y = HEIGHT/2

# Função que desenha a Bala        
class Bullet(pygame.sprite.Sprite):
    def __init__(self,player_rect,player_state):
        global bullet_img
        pygame.sprite.Sprite.__init__(self)
        bullet = bullet_img
        self.image= pygame.transform.scale(bullet,(8,8))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = player_rect.x
        self.rect.y = player_rect.y
        if player_state in X:
            self.speedy = 0
            if player_state == RIGHT:      
                self.speedx = 20
            else:
                self.speedx = -20
        elif player_state in Y:
            self.speedx = 0
            if player_state == FWD:
                self.speedy = -20
            else:
                self.speedy = 20
        elif player_state == IDLE_FWD:
            self.speedx = 0
            self.speedy = -20
        elif player_state == IDLE_BKD:
            self.speedx = 0
            self.speedy = 20
        elif player_state == IDLE_RIGHT:
            self.speedx = 20
            self.speedy = 0           
        elif player_state == IDLE_LEFT:
            self.speedx = -20
            self.speedy = 0
        else:
            self.speedx = 0
            self.speedy = 0


                   
    def update(self): 
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.x > WIDTH or self.rect.x<0 or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()
            
# Função que Carrega as imagens do inimigo e declara suas váriaveis principais            
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,player):
        self.last_time_shot = 0
        self.player=player
        pygame.sprite.Sprite.__init__(self)
        
        enemy_spritesheet =   [pygame.image.load(path.join(img_dir, "enemy_fwd.png")).convert_alpha(),
                        pygame.image.load(path.join(img_dir, "enemy_right.png")).convert_alpha(),
                        pygame.image.load(path.join(img_dir, "enemy_bkd.png")).convert_alpha(),
                        pygame.image.load(path.join(img_dir, "enemy_left.png")).convert_alpha(),
                        pygame.image.load(path.join(img_dir, "enemy_fwd0.png")).convert_alpha(),
                        pygame.image.load(path.join(img_dir, "enemy_fwd1.png")).convert_alpha(),
                        pygame.image.load(path.join(img_dir, "enemy_right0.png")).convert_alpha(),
                        pygame.image.load(path.join(img_dir, "enemy_right1.png")).convert_alpha(),
                        pygame.image.load(path.join(img_dir, "enemy_bkd0.png")).convert_alpha(),
                        pygame.image.load(path.join(img_dir, "enemy_bkd1.png")).convert_alpha(),
                        pygame.image.load(path.join(img_dir, "enemy_left0.png")).convert_alpha(),
                        pygame.image.load(path.join(img_dir, "enemy_left1.png")).convert_alpha(),
                        pygame.image.load(path.join(img_dir, "enemy_hit_fwd.png")).convert_alpha(),
                        pygame.image.load(path.join(img_dir, "enemy_hit_right.png")).convert_alpha(),
                        pygame.image.load(path.join(img_dir, "enemy_hit_bkd.png")).convert_alpha(),
                        pygame.image.load(path.join(img_dir, "enemy_hit_left.png")).convert_alpha()] 
        
        i = 0
        while i < len(enemy_spritesheet):
            if i < len(enemy_spritesheet):
                enemy_spritesheet[i] = pygame.transform.scale(enemy_spritesheet[i],(30,60))
                self.image = enemy_spritesheet[i]
                self.image.set_colorkey(WHITE)
            i += 1
        
        # Animações do Inimigo
        self.animations = {IDLE_FWD:enemy_spritesheet[0:1], 
                           IDLE_RIGHT:enemy_spritesheet[1:2], 
                           IDLE_BKD:enemy_spritesheet[2:3], 
                           IDLE_LEFT:enemy_spritesheet[3:4], 
                           FWD:enemy_spritesheet[4:6],
                           RIGHT:enemy_spritesheet[6:8],
                           BKD:enemy_spritesheet[8:10],
                           LEFT:enemy_spritesheet[10:12],
                           MARCH_FWD:enemy_spritesheet[12:14],
                           MARCH_RIGHT:enemy_spritesheet[14:16],
                           MARCH_BKD:enemy_spritesheet[16:18],
                           MARCH_LEFT:enemy_spritesheet[18:20],
                           HIT_FWD:enemy_spritesheet[20:21],
                           HIT_RIGHT:enemy_spritesheet[21:22],
                           HIT_BKD:enemy_spritesheet[22:23],
                           HIT_LEFT:enemy_spritesheet[23:24]}
        
        self.state = RIGHT
        self.animation = self.animations[self.state]
        self.frame = 0
        self.got = False
        self.fire = False
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.speedx = 2
        self.speedy = 0
        self.last_position = [300,100]
        self.health_enemy = HEALTH_ENEMY
        self.last_update = pygame.time.get_ticks()
        self.frame_ticks = 100
        self.ready_to_shoot = False
        
    def update(self):
        
        now = pygame.time.get_ticks()
        time_between_shots = now - self.last_time_shot
        if time_between_shots > 5000 +random.randint(-2000,2000):
            self.last_time_shot = now
            self.ready_to_shoot = True 
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
            
            
        if self.rect.x - self.last_position[0] > 100:
            self.speedx = 0
            self.speedy = 2
            self.state = BKD
            self.last_position = [self.rect.x,self.rect.y]
        elif self.rect.y - self.last_position[1] > 100:
            self.speedx = -2
            self.speedy = 0
            self.state = LEFT
            self.last_position = [self.rect.x,self.rect.y]
        elif self.rect.x - self.last_position[0] < -100:
            self.speedx = 0
            self.speedy = -2
            self.state = FWD
            self.last_position = [self.rect.x,self.rect.y]
        elif self.rect.y - self.last_position[1] < -100:
            self.speedx = 2
            self.speedy = 0
            self.state = RIGHT
            self.last_position = [self.rect.x,self.rect.y]
        
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy  
       # print(self.rect.x - self.last_position[0])    

# Carrega Sons e Imagens            
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.display.set_caption("MG")
steps_sound = pygame.mixer.Sound(path.join(snd_dir, 'steps.wav'))
spotted_sound = pygame.mixer.Sound(path.join(snd_dir, 'spotted.ogg'))
land_sound = pygame.mixer.Sound(path.join(snd_dir, 'land.wav'))
cock_sound = pygame.mixer.Sound(path.join(snd_dir, 'cock.wav'))

gun_img = pygame.image.load(path.join(img_dir,"gun.png")).convert_alpha()
fist_img = pygame.image.load(path.join(img_dir,"fist.png")).convert_alpha()
bullet_img = pygame.image.load(path.join(img_dir, "bullet.png")).convert_alpha()

# Função que Carrega a tela Principal, onde ocorre o jogo
def field_screen(screen):
    global    WAVE_NUMBER
    running = True  
    pygame.mixer.music.load(path.join(snd_dir, 'Evasion.mp3'))
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(loops=-1)
    row = len(mapa)
    column = len(mapa[0])
    tiles = pygame.sprite.Group()
    trees = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    walls = [Wall(-10, 0, 10, HEIGHT), Wall(0, -10, WIDTH, 10), Wall(1330, 0, 10, HEIGHT),Wall(0, 690, WIDTH, 10)]
    player = Player()
    gun = Gun()
    wall = Wall(-10, 0, 10, HEIGHT)
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
    walls.append(wall)
    while running:
        
        clock.tick(FPS)
        
        if len(enemies) == 0:
            for wave in range(WAVE_NUMBER):
                inimigo = Enemy(random.randint(300,600),random.randint(100,300), player)
                all_sprites.add(inimigo)
                enemies.add(inimigo)
            WAVE_NUMBER += 1
        for event in pygame.event.get():      
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:       
                if event.key == pygame.K_q:
                    running = False
                # loop que só ocorre quando o jogador chega no chão e está desarmado
                if player.state != AIR:
                    if player.state in UNARMED:
                        #print(event.key)
                        if event.key == pygame.K_e:
                            if player.got:
                                bullet = Bullet(player.rect,player.state)
                                all_sprites.add(bullet)
                                bullets.add(bullet)     
                           
                            #spotted_sound.play()
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
        
        # Colisão do jogador com a tela e colisão das balas do inimigo e jogador 
        if player.state != AIR:
            collisions = pygame.sprite.spritecollide(player, enemy_bullets, True)
            for collition in collisions:
                player.health -= 10
            collisions = pygame.sprite.spritecollide(player, trees, False)
            for wall in walls:
                if(pygame.sprite.collide_rect(player, wall)):
                    collisions.append(wall)  
            for collision in collisions:
                if player.speedx > 0:
                    player.rect.right = collision.rect.left
                elif player.speedx < 0:
                    player.rect.left = collision.rect.right
                if player.speedy > 0:
                    player.rect.bottom = collision.rect.top
                elif player.speedy < 0:
                    player.rect.top = collision.rect.bottomq
            loot = pygame.sprite.collide_mask(player, gun)
            for inimigo in enemies:
                if(inimigo.ready_to_shoot):
                    bullet = Bullet(inimigo.rect,inimigo.state)
                    all_sprites.add(bullet)
                    enemy_bullets.add(bullet) 
                    inimigo.ready_to_shoot= False
                collisions = pygame.sprite.spritecollide(inimigo,trees,False)
                for collision in collisions:
                    if inimigo.speedx > 0:
                        inimigo.rect.right = collision.rect.left
                    elif inimigo.speedx < 0:
                        inimigo.rect.left = collision.rect.right
                    if inimigo.speedy > 0:
                        inimigo.rect.bottom = collision.rect.top
                    elif inimigo.speedy < 0:
                        inimigo.rect.top = collision.rect.bottom
                collisions = pygame.sprite.spritecollide(inimigo, bullets, True)
                if len(collisions) > 0:
                    inimigo.kill()

            if loot != None and player.got == False:
                cock_sound.play()
                gun.kill()
                player.got = True
#                item.gun = True
            
            collisions = pygame.sprite.spritecollide(player, enemies, False)
        
        # Carregando Fundo de Tela e Sprites
        all_sprites.update()
        screen.fill(BLACK)
        all_sprites.draw(screen) 
        draw_lifebar(screen, 10, 10, player.health / HEALTH)
        if(not player.got):
            draw_weapon(screen, 37,11,fist_img)
        else:
            draw_weapon(screen, 37,11,gun_img)
        pygame.display.flip()
        
# Tela Principal do Jogo        
try:
    field_screen(screen)
finally:
    pygame.quit()