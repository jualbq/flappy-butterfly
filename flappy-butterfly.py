import pygame, random
from pygame.locals import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SPEED = 10
GRAVITY = 1
GAME_SPEED = 5

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

TRUNK_WIDTH = 100
TRUNK_HEIGHT = 500

TRUNK_GAP = 100


class Butterfly(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        
        self.images = [
            pygame.image.load('butterfly1.png'),
            pygame.image.load('butterfly2.png'),
            pygame.image.load('butterfly3.png'),
            pygame.image.load('butterfly4.png'),
            pygame.image.load('butterfly5.png'),
            pygame.image.load('butterfly6.png'),
            pygame.image.load('butterfly7.png'),
            pygame.image.load('butterfly8.png'),
            pygame.image.load('butterfly9.png'),
            pygame.image.load('butterfly10.png'),
        ]
        self.speed = SPEED

        self.current_image = 0

        self.image = pygame.image.load('butterfly1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 4 # x
        self.rect[1] = SCREEN_HEIGHT / 4 # y

    def update(self):
        self.current_image = (self.current_image + 1) % 10
        self.image = self.images[ self.current_image ]

        self.speed += GRAVITY

        self.rect[1] += self.speed # y
    
    def bump(self):
        self.speed = -SPEED

class Trunk(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('tree-trunk.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (TRUNK_WIDTH,TRUNK_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

def is_trunk_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def is_butterfly_off_screen(sprite):
    return sprite.rect[1] > SCREEN_HEIGHT + 100 or sprite.rect[1] < -100

def get_random_trunks(xpos):
    size = random.randint(100, 300)
    trunk = Trunk(False, xpos, size)
    trunk_inverted = Trunk(True, xpos, SCREEN_HEIGHT - size - TRUNK_GAP)
    return (trunk, trunk_inverted)

# Iniciar o jogo
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

music = "Grassy World (8-Bit_Orchestral Overture) - Main Title Theme.mp3"
pygame.mixer.music.load(music)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()
pygame.event.wait()


jump_sound = pygame.mixer.Sound('sfx_jump.flac')

BACKGROUND = pygame.image.load('background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

GAME_OVER_BACKGROUND = pygame.image.load("gameover.png")
GAME_OVER_BACKGROUND = pygame.transform.scale(GAME_OVER_BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

butterfly_group = pygame.sprite.Group()
butterfly = Butterfly()
butterfly_group.add(butterfly)

trunk_group = pygame.sprite.Group()
for i in range(2):
    trunks = get_random_trunks(SCREEN_WIDTH * i + 800)
    trunk_group.add(trunks[0])
    trunk_group.add(trunks[1])


clock = pygame.time.Clock()

game_over = False
gameloop = True

while gameloop:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            gameloop = False

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if game_over:
                    game_over = False
                    pygame.mixer.music.stop()
                    music = "Grassy World (8-Bit_Orchestral Overture) - Main Title Theme.mp3"
                    pygame.mixer.music.load(music)
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play()
                butterfly.bump()
                jump_sound.play()
    if game_over:
        screen.blit(GAME_OVER_BACKGROUND, (0, 0))
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            music = "Game Over Music.mp3"
            pygame.mixer.music.load(music)
            pygame.mixer.music.play()
    else:
        screen.blit(BACKGROUND, (0, 0))

        if is_trunk_off_screen(trunk_group.sprites()[0]):
            trunk_group.remove(trunk_group.sprites()[0])
            trunk_group.remove(trunk_group.sprites()[0])

            trunks = get_random_trunks(SCREEN_WIDTH * 2)

            trunk_group.add(trunks[0])
            trunk_group.add(trunks[1])

        butterfly_group.update()
        trunk_group.update()

        butterfly_group.draw(screen)
        trunk_group.draw(screen)

        if is_butterfly_off_screen(butterfly_group.sprites()[0]) or pygame.sprite.groupcollide(butterfly_group, trunk_group, False, False, pygame.sprite.collide_mask):
            butterfly.rect[0] = SCREEN_WIDTH / 4
            butterfly.rect[1] = SCREEN_HEIGHT / 4
            trunk_group.remove(trunk_group.sprites()[0])
            trunk_group.remove(trunk_group.sprites()[0])

            trunks = get_random_trunks(SCREEN_WIDTH * 2)

            trunk_group.add(trunks[0])
            trunk_group.add(trunks[1])
            pygame.mixer.music.stop()
            game_over = True
    

    pygame.display.update()
