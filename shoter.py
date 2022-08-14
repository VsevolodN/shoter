import pygame,random,os
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = (SCREEN_WIDTH*0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("shoter")

clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.75

moving_left = False
moving_right = False

BG = (144,201,120)
RED = (255,0,0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen,RED,(0,400),(SCREEN_WIDTH,400),3)

class Soldier(pygame.sprite.Sprite):
    def __init__(self,char_type,x,y,scale,speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.alive = True
        self.jump = False
        self.vel_y = 0
        self.direction = 1
        self.in_air = True
        self.flip = False
        self.animetion_list = []
        self.frame_index = 0
        self.char_type = char_type
        self.update_time = pygame.time.get_ticks()
        self.action = 0
        animation_types = ["Idle", "Run", "Jump"]



        for animation in animation_types:
            self.temp_list = []
            num_of_frames = len(os.listdir(f"img/{self.char_type}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"img/{self.char_type}/{animation}/{i}.png").convert_alpha()

                img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
                self.temp_list.append(img)
            self.animetion_list.append(self.temp_list)

        self.image=self.animetion_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)
        pygame.draw.rect(screen,RED,(self.rect.x,self.rect.y,self.rect.width,self.rect.height),3)

    def move(self,moving_left,moving_right):
        dx = 0
        dy = 0

        if moving_left:
            if self.rect.x - self.speed> 0:
                dx = -self.speed
                self.direction=-1
                self.flip = True
            else:
                dx = 0


        if moving_right:
            if self.rect.right + self.speed < 800:
                dx = self.speed
                self.direction = 1
                self.flip = False
            else:
                dx=0


        if self.jump and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.bottom + dy > 400:
            dy = 400-self.rect.bottom
            self.in_air=False

        self.rect.x+=dx
        self.rect.y+=dy
    def ubdate_animation(self):
        ANIMATION_COLDOWN = 100
        self.image = self.animetion_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COLDOWN:
            self.frame_index +=1
            self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animetion_list[self.action]):
                self.frame_index = 0

    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()




player = Soldier("player",300,200,2,5)
enemy = Soldier("enemy",200,200,2,5)


run = True
while run:
    draw_bg()
    player.draw()
    enemy.draw()
    player.move(moving_left,moving_right)
    player.ubdate_animation()
    enemy.ubdate_animation()

    if player.alive:
        if moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)
        if player.in_air:
            player.update_action(2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            else:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = True
            else:
                moving_right = False

            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()
    clock.tick(FPS)
