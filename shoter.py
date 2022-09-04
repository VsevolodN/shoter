import pygame,random,os,io
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int((SCREEN_WIDTH*0.8))

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("shoter")

clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.75

password = 'lemon'
file = io.open("pass_word.txt",'r',encoding='utf-8')
if file.readline() == password:
    razrab = True
else:
    razrab = False
file.close()

moving_left = False
moving_right = False

shoot = False
grand = False

death1 = pygame.mixer.Sound("Sound/death.mp3")
death2 = pygame.mixer.Sound("Sound/death_2.mp3")
death3 = pygame.mixer.Sound("Sound/death_3.mp3")
death4 = pygame.mixer.Sound("Sound/death_4.mp3")
death5 = pygame.mixer.Sound("Sound/death_5.mp3")
death6 = pygame.mixer.Sound("Sound/death_6.mp3")
death7 = pygame.mixer.Sound("Sound/death_7.mp3")
death8 = pygame.mixer.Sound("Sound/death_8.mp3")
death_spis_music = [death1,death2,death3,death4,death5,death6,death7,death8]

gun_spis = [pygame.mixer.Sound("Sound/gun1.mp3"),
            pygame.mixer.Sound("Sound/gun2.mp3"),
            pygame.mixer.Sound("Sound/gun3.mp3")]

grand_spis = [pygame.mixer.Sound("Sound/grand1.mp3")]

grand_boom_spis = [pygame.mixer.Sound("Sound/grand_boom1.mp3")]


music_len_spis = 7
pygame.mixer.music.load(f"music/{random.randint(0,music_len_spis)}.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

#load img
bullet_img = pygame.image.load("img/icons/bullet.png")
grenade_img = pygame.image.load("img/icons/grenade.png")

BG = (144,201,120)
RED = (255,0,0)

def draw_bg():
    screen.fill(BG)

    #down
    pygame.draw.line(screen,RED,(0,400),(SCREEN_WIDTH,400),3)


class Soldier(pygame.sprite.Sprite):
    def __init__(self,char_type,x,y,scale,speed,ammo,granades):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.alive = True
        self.jump = False
        self.vel_y = 0
        self.ammo = ammo
        self.start_ammo = ammo
        self.direction = 1
        self.health = 100
        self.max_health = self.health
        self.culdown = 15
        self.culdown_count = self.culdown
        self.in_air = True
        self.flip = False
        self.granades = granades
        self.sound_play_death = True
        self.animetion_list = []
        self.frame_index = 0
        self.char_type = char_type
        self.update_time = pygame.time.get_ticks()
        self.action = 0
        animation_types = ["Idle", "Run", "Jump","Death"]



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
        # pygame.draw.rect(screen,RED,(self.rect.x,self.rect.y,self.rect.width,self.rect.height),3)

    def shoot(self):
        if self.alive:
            if self.ammo > 0:
                if self.culdown != 0:
                    self.culdown-=1
                else:
                    self.culdown = self.culdown_count
                    bullet = Bullet(self.rect.centerx + self.rect.width * 0.75 * self.direction, self.rect.centery,self                 .direction)
                    bullet_grup.add(bullet)
                    self.ammo-=1
                    pygame.mixer.Sound.play(gun_spis[random.randint(0,2)])

    def move(self,moving_left,moving_right):
        if self.alive:
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
    def sound_test(self):
        if self.sound_play_death:
            if self.alive == False:
                death_spis_music[random.randint(0,len(death_spis_music)-1)].play()
                self.sound_play_death=False

    def ubdate_animation(self):
        ANIMATION_COLDOWN = 100
        self.image = self.animetion_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COLDOWN:

            self.frame_index +=1
            self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animetion_list[self.action]):
                if self.action ==3:
                    self.frame_index = len(self.animetion_list[self.action])-1
                else:
                    self.frame_index = 0


    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action

            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    def cheak_alive(self):
        if self.health <= 0:
            self.alive = False
            self.health=0
            self.update_action(3)

    def update(self):
        self.ubdate_animation()
        self.cheak_alive()
        self.sound_test()


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 7
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
        self.flip = False

    def drow (self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)

    def update(self):
        self.rect.x += self.speed * self.direction

        if self.rect.x < 0 or self.rect.x > 800:
            self.kill()

        if pygame.sprite.spritecollide(player, bullet_grup, False):
            if player.alive:
                player.health -= 5
                self.kill()

        if pygame.sprite.spritecollide(enemy, bullet_grup, False):
            if enemy.alive:
                enemy.health-=20
                self.kill()

class Grenade(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 7
        self.vel_y = -13
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
        self.flip = False

    def update(self):
        self.vel_y += GRAVITY

        dx = self.speed * self.direction
        dy = self.vel_y


        if self.rect.x + dx <= 0:
            self.direction *= -1

        if self.rect.right + dx >= 800:
            self.direction *= -1

            self.vel_y -= 5


        if self.rect.bottom + dy > 400:

            grand_boom_spis[random.randint(0, len(grand_boom_spis) - 1)].play()

            dy = 400 - self.rect.bottom
            dx = 0

            self.kill()


        self.rect.x += dx
        self.rect.y += dy

#create grup sprite
bullet_grup = pygame.sprite.Group()
Grenade_grup = pygame.sprite.Group()



player = Soldier("player",300,300,2,5,100,5)
enemy = Soldier("enemy",200,300,2,5,10,5)


run = True
while run:
    draw_bg()
    player.draw()
    enemy.draw()
    player.move(moving_left,moving_right)
    player.update()
    enemy.update()
    Grenade_grup.update()

    bullet_grup.update()
    bullet_grup.draw(screen)

    Grenade_grup.update()
    Grenade_grup.draw(screen)


    if player.alive:
        if shoot:
            player.shoot()
        elif grand and player.granades > 0:
            grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
                              player.rect.top, player.direction)
            grand_spis[random.randint(0, len(grand_spis) - 1)].play()
            Grenade_grup.add(grenade)

            player.granades -= 1
        grand = False

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
            if event.key == pygame.K_d:
                moving_right = True

            if event.key == pygame.K_w:
                shoot=True

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

            if event.key == pygame.K_w:
                shoot=False

            if event.key == pygame.K_q:
                grand = True


            if razrab:
                if event.key == pygame.K_k:
                    player.alive=False
                    player.update_action(3)
                if event.key == pygame.K_m:
                    death_spis_music[random.randint(0, len(death_spis_music) - 1)].play()
                if event.key == pygame.K_l:
                    player.alive = True
                if event.key == pygame.K_p:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(f"music/{random.randint(0, music_len_spis)}.mp3")
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)

                if event.key == pygame.K_o:
                    player.granades+=1

    pygame.display.update()
    clock.tick(FPS)
