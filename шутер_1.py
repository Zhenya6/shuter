#Создай собственный Шутер!

from pygame import *
from random import randint
#mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()

class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, widht, height, player_speed_y, player_speed_x,):
        super().__init__()


        self.image = transform.scale(image.load(player_image), (widht, height))
        self.speed_x = player_speed_x
        self.speed_y = player_speed_y


        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.height = height
        self.widht = widht

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed_x
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed_x

    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx-26,self.rect.top,45,10,5,0)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y+=self.speed_x
        if self.rect.y > 500:
            self.rect.x= randint(50,650)
            self.rect.y=0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed_y
        self.rect.x -= self.speed_x
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"),(win_width,win_height))
game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font1 = font.SysFont('Arial',80)
win = font1.render("YOU WIN!", True, (255,255,255))
lose = font1.render("YOU LOSE!", True, (100,0,0))

font2 = font.SysFont('Arial', 36)


ship = Player("rocket.png",350,410,200,70,0,7)
monsters=sprite.Group()
for i in range(5):
    monster=Enemy("ufo.png",randint(50,650),0,80,50,0,randint(1,5))
    monsters.add(monster)
bullets = sprite.Group()
score = 0
lost = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type==KEYDOWN:
            if e.key==K_SPACE:
                ship.fire()

    if finish != True:
        window.blit(background,(0,0))
        text=font2.render("Счёт:"+str(score),True,(255,255,255))
        window.blit(text,(20,20))
        text1=font2.render("Пропущено:"+str(lost),True,(255,255,255))
        window.blit(text1,(20,50))
        ship.reset()
        ship.update()
        monsters.update()
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for monster in collides:
            monster=Enemy("ufo.png",randint(50,650),0,80,50,0,randint(1,5))
            monsters.add(monster)
            score = score + 1

        sprite_list=sprite.spritecollide(ship, monsters, False)
        if sprite_list or lost == 3:
            finish = True
            window.blit(lose,(200,200))
        if score == 100:
            finish = True
            window.blit(win,(200,200))

    display.update()
    clock.tick(FPS)