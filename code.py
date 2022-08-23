from pygame import *

init()
back = (200, 255, 255)
win_widht = 700
win_height = 500
GREEN = (0, 255, 0)
mw=display.set_mode((win_widht, win_height))
mw.fill(back)
display.set_caption('Лабиринт')
picture = transform.scale(image.load('background.jpg'), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, filename, widht, height, x, y):
        super().__init__()
        self.image = transform.scale(image.load(filename), (widht, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, filename, widht, height, x, y, x_speed, y_speed):
        super().__init__(filename, widht, height, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
        
    def fire(self):
        bullet = Bullet('bullet.png', 30,30, self.rect.right, self.rect.centery-15,20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, filename, widht, height, x, y, speed):
        super().__init__(filename, widht, height, x, y)
        self.speed = speed

    def update(self):
        if self.rect.x <= 500:
            self.direction = 'right'
        if self.rect.x >= 600:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
    
class Bullet(GameSprite):
    def __init__(self, filename, widht, height, x, y, speed):
        super().__init__(filename, widht, height, x, y)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x>670:
            self.kill()

player = Player('hedgehog.png', 60, 60, 100, 400, 0, 0)
wall1 = GameSprite('wall.png', 250, 40, 200, 200)
wall2 = GameSprite('wall.png', 40, 360, 450, 120)
wall3 = GameSprite('wall.png', 200, 40, 20, 350)
final = GameSprite('apple.png', 50, 50, 580, 400)
enemy = Enemy('wolf.png', 50, 50, 500, 200, 5)
win = GameSprite('win.png', 700, 500, 0, 0)
lose = GameSprite('lose.png', 700, 500, 0, 0)
bullets = sprite.Group()
barriers = sprite.Group()
barriers.add(wall1)
barriers.add(wall2)
barriers.add(wall3)
enemies = sprite.Group()
enemies.add(enemy)

run = True
finish = False
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_RIGHT:
                player.x_speed=5
            if e.key == K_LEFT:
                player.x_speed=-5
            if e.key == K_UP:
                player.y_speed=-10
            if e.key == K_DOWN:
                player.y_speed=10
            if e.key == K_SPACE:
                player.fire()
        if e.type == KEYUP:
            if e.key == K_RIGHT:
                player.x_speed=0
            if e.key == K_LEFT:
                player.x_speed=0
            if e.key == K_UP:
                player.y_speed=0
            if e.key == K_DOWN:
                player.y_speed=0
        
    mw.blit(picture, (0,0))
    if sprite.collide_rect(player, final):
        finish = True
        win.reset()
    if sprite.collide_rect(player, enemy):
        finish = True
        lose.reset()
    
    if not(finish):
        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets, enemies, True, True)

        barriers.draw(mw)
        bullets.update()
        bullets.draw(mw)
        enemies.draw(mw)
        player.reset()
        enemies.update()
        final.reset()
        player.update()
    display.update()
