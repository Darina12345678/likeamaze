# Разработай свою игру в этом файле!
# твой код здесь
from pygame import*
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self,picture,w,h,x,y):
        super().__init__()
        self.image=transform.scale(image.load(picture),(w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self,picture,w,h,x,y, x_speed,y_speed):
        super().__init__(picture,w,h,x,y)
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

    def shoot(self):
        bullet = Bullet('bullet.png', 30, 30, self.rect.right, self.rect.centery, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= 170:
            self.side = "right"
        if self.rect.x >= 390:
            self.side = "left"
        
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

                

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 710:
            self.kill()


window = display.set_mode((700,500))
display.set_caption('Моя первая игра')
background = transform.scale(image.load('fon.jpg'), (700,500))

wall_1 = GameSprite('wall.jpg', 20,150, 80, 0)
wall_2 = GameSprite('wall.jpg', 120,20,90,130)
wall_3 = GameSprite('wall.jpg', 20,150, 190, 0)
wall_4 = GameSprite('wall.jpg', 20,280, 80, 230)
wall_5 = GameSprite('wall.jpg', 220,20,80,230)
wall_6 = GameSprite('wall.jpg', 20,150,300,0)
wall_7 = GameSprite('wall.jpg', 20,280, 300, 230)
wall_8 = GameSprite('wall.jpg', 20,150, 450, 350)
wall_9 = GameSprite('wall.jpg', 150,20, 560, 350)
wall_10 = GameSprite('wall.jpg', 10,500, 701, 0)

goal = GameSprite('goal.png', 80, 80, 615, 400)

player = Player('hero.jpg', 60, 60, 0, 0, 0, 0)
enemy1 = Enemy('enemy.jpg', 70, 70, 120, 160, 5)
enemy2 = Enemy('enemy.jpg', 80, 80, 580, 250, 5)

walls = sprite.Group()
walls.add(wall_1)
walls.add(wall_2)
walls.add(wall_3)
walls.add(wall_4)
walls.add(wall_5)
walls.add(wall_6)
walls.add(wall_7)
walls.add(wall_8)
walls.add(wall_9)
walls.add(wall_10)

enemies = sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)

bullets = sprite.Group()

run = True
while run:
    time.delay(50)
    window.blit(background,(0,0))
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                player.x_speed -= 5
            elif e.key == K_RIGHT:
                player.x_speed += 5
            elif e.key == K_UP:
                player.y_speed -= 5
            elif e.key == K_DOWN:
                player.y_speed += 5
            elif e.key == K_SPACE:
                player.shoot()


        elif e.type == KEYUP:
            if e.key == K_LEFT:
                player.x_speed = 0
            elif e.key == K_RIGHT:
                player.x_speed = 0
            elif e.key == K_UP:
                player.y_speed = 0
            elif e.key == K_DOWN:
                player.y_speed = 0
    
    if sprite.spritecollide(player, enemies, False):
        player.rect.x = 0
        player.rect.y = 0

    if sprite.spritecollide(player, walls, False):
        player.x_speed *= -2
        player.y_speed *= -2

    if sprite.collide_rect(player, goal):
        goal.rect.x = randint(100,600)
        goal.rect.y = randint(100,400)

    if sprite.groupcollide(bullets, enemies, True, True):
        enemy3 = Enemy('enemy.jpg', 80, 80, randint(100, 600), randint(100,400), 5)
        enemies.add(enemy3)

    if sprite.groupcollide(enemies, walls, False, False):
        for enemy in enemies:
            if sprite.spritecollide(enemy, walls, False):
                enemy.speed *= -1
    



    player.update()
    player.reset()
    goal.reset()

    walls.update()
    walls.draw(window)
    enemies.update()
    enemies.draw(window)
    bullets.update()
    bullets.draw(window)
    display.update()
    