import pygame, math, random

width, height = 1280, 600
window = pygame.display.set_mode((width, height))

lose_screen = pygame.image.load('lose_screen.jpg')
pygame.init()


class meteor_class(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        x = 1280
        y = random.randint(0, height)
        self.image = pygame.image.load('meteor.png')
        self.rect = self.image.get_rect(center=[x, y])
        self.destroy_sound = pygame.mixer.Sound('large-explosion-sound-effect.wav')

    def move_func(self):
        self.rect.x -= random.randint(10,20)
        if self.rect.x <= 0:
            self.kill()

    def destroy_func(self):
        if pygame.sprite.spritecollide(f_laser, meteor_group, True):
            self.kill()
            self.destroy_sound.play()



class f_laser_class(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('projectile.png')
        self.rect = self.image.get_rect(center=pos)
        self.shoot_sound = pygame.mixer.Sound('laser-gun-sound-effect.wav')
        pygame.display.update()
    def update(self):
        key = pygame.key.get_pressed()
        self.rect.x += 10
        if self.rect.x >= width:
            self.kill()
    def shoot(self):
        self.shoot_sound.play()


class player_class(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('spaceship.png')
        self.rect = self.image.get_rect()
        self.vel = 0

    def update(self):
        key = pygame.key.get_pressed()
        self.vel = 0
        if key[pygame.K_w]:
            self.vel = -10
        if key[pygame.K_s]:
            self.vel = 10
        self.rect.y += self.vel
        if self.rect.bottom >= height:
            self.rect.bottom = height
        if self.rect.top <= 0:
            self.rect.top = 0

    def destroy_func(self):
        if pygame.sprite.spritecollide(self, meteor_group, True):
            self.kill()
            window.blit(lose_screen, (0, 0))
            pygame.display.update()
            pygame.quit()


FPS = 120
run = True
clock = pygame.time.Clock()

# objects
player = player_class()
player_group = pygame.sprite.GroupSingle()
player_group.add(player)

meteor = meteor_class()
meteor_2 = meteor_class()
meteor_3 = meteor_class()
meteor_group = pygame.sprite.Group()

f_laser_group = pygame.sprite.Group()

f_laser = f_laser_class(player.rect.midright)
f_laser_group = pygame.sprite.Group()
while run:
    #pygame.mixer.Sound("space-cinematic-ambient-background-music-for-videos-royalty-free-music-by-ashamaluevmusic.wav").play()
    clock.tick(FPS)
    key = pygame.key.get_pressed()
    window.blit(pygame.image.load('background-black.png'), (0,0))
    for event in pygame.event.get():
        # exit loops
        if event.type == pygame.QUIT:
            run = False
            break
    if key[pygame.K_q]:
        if len(f_laser_group) == 0:
            f_laser = f_laser_class(player.rect.midright)
            f_laser_group = pygame.sprite.Group()
            f_laser_group.add(f_laser)
            f_laser.shoot()
        else:
            pass
    f_laser.update()

    if len(meteor_group) != 3:
        meteor = meteor_class()
        meteor_group = pygame.sprite.Group()
        meteor_group.add(meteor)
        meteor_group.add(meteor_2)
        meteor_group.add(meteor_3)

    else:

        print(meteor_group)
        print(len(meteor_group))

        meteor.move_func()
        meteor_2.move_func()
        meteor_3.move_func()

    player_group.update()
    meteor_group.update()
    f_laser_group.update()
    meteor.destroy_func()
    meteor_2.destroy_func()
    meteor_3.destroy_func()
    player.destroy_func()
    meteor_group.draw(window)
    player_group.draw(window)
    f_laser_group.draw(window)

    pygame.display.update()

pygame.quit()
