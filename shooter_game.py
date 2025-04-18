from pygame import *
from random import *

'''mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
'''

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
image_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_meteor = 'asteroid.png'

score = 0
lost = 0
all = 10

font.init()
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 80)

lose = font1.render('ПРОИГРАЛ', True, (255, 0, 0))
win = font1.render('ПОБЕДИЛ', True, (0, 255, 0))
max_lost = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x <win_width-80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15 )
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        
        self.rect.y+=self.speed
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0


win_width = 700
win_height = 500

display.set_caption('ШУТЕР')

window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
ship = Player(img_hero, 5, win_height-100, 80, 100, 10)



finish = False
run = True

clock = time.Clock()
asteroids = sprite.Group()
for i in range(1,6):
    asteroid = Asteroid(img_meteor, randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
    asteroids.add(asteroid)
monsters = sprite.Group()

for i in range(1, 6):
    monster = Enemy(image_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
    monsters.add(monster)
    

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                '''fire_sound.play()'''
                ship.fire()
    keys = key.get_pressed()
    if keys[K_ESCAPE]:
        run = False

    if not finish:
        window.blit(background,(0,0))
        sprite_list = sprite.spritecollide(ship, asteroids, False)
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for m in sprite_list:
            asteroid = Asteroid(img_meteor, randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
            asteroids.add(asteroid)
        for a in sprites_list:
            monster = Enemy(image_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
            monsters.add(monster)
            score+=1

        if score == 10:
            finish = True
            window.blit(win, (180, 200))
        sprites_list = sprite.spritecollide(ship, monsters, False)
        
        if lost >= 3 or sprites_list:
            finish = True
            window.blit(lose, (180,200))
        
        text = font2.render('Счёт: '+str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_refresh = font2.render('Пули: '+str(all), 1, (255, 255, 255))
        window.blit(text_refresh, (10, 80))
        text_lose = font2.render("Пропущено: "+str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        monsters.update()
        bullets.update()
        asteroid.update()

        ship.reset()
        asteroid.reset()
        monsters.draw(window)
        bullets.draw(window)
        '''if bullets >= rect.top:
            all =-1'''
        display.update()
        
    clock.tick(60)