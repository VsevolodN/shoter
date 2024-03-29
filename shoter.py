import pygame, random, os, io, csv

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int((SCREEN_WIDTH * 0.8))

multy_jump = False

mouse_raz = False

SCROOL_THRESH = 150  # Начало прокрутки экрана
SCREEN_SCROOL = 0
BG_SCROOL = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("shoter")

clock = pygame.time.Clock()
FPS = 60

ROWS = 16
COLS = 150

GRAVITY = 0.75
TILE_SIZE = SCREEN_HEIGHT // ROWS
TITE_TYPES = 21

level = 0

password = 'lemon'
file = io.open("pass_word.txt", 'r', encoding='utf-8')
if file.readline() == password:
    razrab = True
else:
    razrab = False
file.close()

font_colour = (0, 139, 139)

moving_left = False
moving_right = False

shoot = False
grand = False

sys_font = pygame.font.SysFont('Arial', 30)

pine2_img = pygame.image.load("img/background/pine1.png")
pine1_img = pygame.image.load("img/background/pine2.png")
mountain_img = pygame.image.load("img/background/mountain.png")
sky_cloud_img = pygame.image.load("img/background/sky_cloud.png")

death1 = pygame.mixer.Sound("Sound/death.mp3")
death2 = pygame.mixer.Sound("Sound/death_2.mp3")
death3 = pygame.mixer.Sound("Sound/death_3.mp3")
death4 = pygame.mixer.Sound("Sound/death_4.mp3")
death5 = pygame.mixer.Sound("Sound/death_5.mp3")
death6 = pygame.mixer.Sound("Sound/death_6.mp3")
death7 = pygame.mixer.Sound("Sound/death_7.mp3")
death8 = pygame.mixer.Sound("Sound/death_8.mp3")
death_spis_music = [death1, death2, death3, death4, death5, death6, death7, death8]

gun_spis = [pygame.mixer.Sound("Sound/gun1.mp3"),
            pygame.mixer.Sound("Sound/gun2.mp3"),
            pygame.mixer.Sound("Sound/gun3.mp3")]

grand_spis = [pygame.mixer.Sound("Sound/grand1.mp3")]

grand_boom_spis = [pygame.mixer.Sound("Sound/grand_boom1.mp3")]

ammo_box = pygame.image.load("img/icons/ammo_box.png").convert_alpha()
health_box = pygame.image.load("img/icons/health_box.png").convert_alpha()
grende_box = pygame.image.load("img/icons/grenade_box.png").convert_alpha()

item_boxes = {"Ammo": ammo_box, "Health": health_box, "Grenade": grende_box}

img_tile = []

for i in range(TITE_TYPES):
    img = pygame.image.load(f'img/tile/{i}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_tile.append(img)

music_len_spis = 7
pygame.mixer.music.load(f"music/{random.randint(0, music_len_spis)}.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# load img
bullet_img = pygame.image.load("img/icons/bullet.png")
grenade_img = pygame.image.load("img/icons/grenade.png")

BG = (144, 201, 120)
RED = (255, 0, 0)


def drow_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg():
    screen.fill(BG)

    width = sky_cloud_img.get_width()

    for x in range(5):
        screen.blit(sky_cloud_img, (x * width - BG_SCROOL * 0.2, 0))
        screen.blit(mountain_img, (x * width - BG_SCROOL * 0.3, 200))
        screen.blit(pine2_img, (x * width - BG_SCROOL * 0.5, 300))
        screen.blit(pine1_img, (x * width - BG_SCROOL * 0.8, 300))

    # down
    # pygame.draw.line(screen,RED,(0,400),(SCREEN_WIDTH,400),3)


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, granades):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.alive = True
        self.jump = False
        self.vel_y = 0
        self.doble_jump = 2
        self.ammo = ammo
        self.start_ammo = ammo
        self.ammo_to_reload = 25
        self.culdown_ammo = 0
        self.direction = 1
        self.health = 100
        self.reloading = True
        self.max_health = self.health
        self.culdown = 15
        self.culdown_count = self.culdown
        self.in_air = True
        self.can_reload = True
        self.flip = False
        self.granades = granades
        self.sound_play_death = True
        self.animetion_list = []
        self.frame_index = 0
        self.char_type = char_type
        self.update_time = pygame.time.get_ticks()
        self.action = 0
        animation_types = ["Idle", "Run", "Jump", "Death"]

        # Ai
        self.ai_move_counter = 0
        self.idle = 0
        self.idle_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)

        for animation in animation_types:
            self.temp_list = []
            num_of_frames = len(os.listdir(f"img/{self.char_type}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"img/{self.char_type}/{animation}/{i}.png").convert_alpha()

                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                self.temp_list.append(img)
            self.animetion_list.append(self.temp_list)

        self.image = self.animetion_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        # pygame.draw.rect(screen,RED,(self.rect.x,self.rect.y,self.rect.width,self.rect.height),3)

    def shoot(self):
        if self.ammo_to_reload > 0:
            if self.alive:
                if self.ammo > 0:
                    if self.culdown != 0:
                        self.culdown -= 1
                    else:
                        self.culdown = self.culdown_count
                        bullet = Bullet(self.rect.centerx + self.rect.width * 0.75 * self.direction, self.rect.centery,
                                        self.direction)
                        bullet_grup.add(bullet)
                        self.ammo -= 1
                        self.ammo_to_reload -= 1
                        pygame.mixer.Sound.play(gun_spis[random.randint(0, 2)])

    def ai(self):

        if self.alive and player.alive:

            if self.idle == False and random.randint(1, 100) == 11:
                self.idle = True
                self.idle_counter = 50
                self.update_action(0)

            if self.vision.colliderect(player):
                self.shoot()
                self.update_action(0)
                self.idle = True

            if self.idle == False:
                if self.direction == 1:
                    ai_moving_right = True
                else:
                    ai_moving_right = False

                ai_moving_left = not ai_moving_right

                self.move(ai_moving_left, ai_moving_right)

                if self.ai_move_counter >= TILE_SIZE:
                    self.direction *= -1
                    self.ai_move_counter *= -1
                self.ai_move_counter += 1
                self.update_action(1)

            else:
                self.idle_counter -= 1
                if self.idle_counter <= 0:
                    self.idle = False

            self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
            # pygame.draw.rect(screen,(0,0,0),self.vision,1)

        self.rect.x += SCREEN_SCROOL

    def move(self, moving_left, moving_right):
        SCREEN_SCROLL = 0

        if self.alive:
            dx = 0
            dy = 0

            if moving_left:
                if self.rect.x - self.speed > 0:
                    dx = -self.speed
                    self.direction = -1
                    self.flip = True
                else:
                    dx = 0

            if moving_right:
                if self.rect.right + self.speed < 800:
                    dx = self.speed
                    self.direction = 1
                    self.flip = False
                else:
                    dx = 0

            if self.jump and self.in_air == False:
                self.vel_y = -11

                self.jump = False

                if not multy_jump:
                    self.in_air = True

                    if self.doble_jump != 1:
                        self.in_air = False

                self.doble_jump -= 1

            self.vel_y += GRAVITY
            dy += self.vel_y

            for tile in world.obstacle_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False

                        self.doble_jump = 2
                    dy = 0

                    # dy = tile.

            self.rect.x += dx
            self.rect.y += dy

            # Обновит scrool при помоши играка

            if self.char_type == "player":
                if self.rect.right >= SCREEN_WIDTH - SCROOL_THRESH and BG_SCROOL < (world.level_length * TILE_SIZE) - SCREEN_WIDTH:
                    self.rect.x -= dx
                    SCREEN_SCROLL = -dx

                if self.rect.left <= SCROOL_THRESH and BG_SCROOL > 0:
                    self.rect.x -= dx
                    SCREEN_SCROLL = -dx

        return SCREEN_SCROLL

    def sound_test(self):
        if self.sound_play_death:
            if self.alive == False:
                death_spis_music[random.randint(0, len(death_spis_music) - 1)].play()
                self.sound_play_death = False

    def ubdate_animation(self):
        ANIMATION_COLDOWN = 100
        self.image = self.animetion_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animetion_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(self.animetion_list[self.action]) - 1
                else:
                    self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def cheak_alive(self):
        if self.health <= 0:
            self.alive = False
            self.health = 0
            self.update_action(3)

    def update(self):
        self.ubdate_animation()
        self.cheak_alive()
        self.sound_test()


class World():
    def __init__(self):
        self.obstacle_list = []

    def procss_data(self, data):
        global level

        self.level_length = len(data[0])
        temp = []
        for y, row in enumerate(data):
            for x, tile in enumerate(row):

                if tile >= 0:
                    img = img_tile[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)

                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)

                    elif tile >= 9 and tile <= 10:
                        whater = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        whater_grup.add(whater)

                    elif tile >= 11 and tile <= 14:
                        Decore = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_grup.add(Decore)

                    elif tile == 15:
                        player = Soldier("player", x * TILE_SIZE, y * TILE_SIZE, 1.65, 3, 100, 5)
                        health_bar = Health_bar(player.health, 10, 10, 100, 10, 3)

                    elif tile == 16:
                        enemy = Soldier("enemy", x * TILE_SIZE, y * TILE_SIZE, 1.65, 3, 100, 0)
                        enemy_grup.add(enemy)
                    if tile == 17:
                        item_boxes_grup.add(item_box("Ammo", x * TILE_SIZE, y * TILE_SIZE))
                    if tile == 18:
                        item_boxes_grup.add(item_box("Grenade", x * TILE_SIZE, y * TILE_SIZE))
                    if tile == 19:
                        item_boxes_grup.add(item_box("Health", x * TILE_SIZE, y * TILE_SIZE))
                    if tile == 20:
                        exit = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_grup.add(exit)
                        level += 1

        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1].x += SCREEN_SCROOL
            screen.blit(tile[0], tile[1])


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 7
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.flip = False

    def drow(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def update(self):
        self.rect.x += self.speed * self.direction

        if self.rect.x < 0 or self.rect.x > 800:
            self.kill()

        for tile in world.obstacle_list:
            if tile[1].colliderect(self):
                self.kill()

        if pygame.sprite.spritecollide(player, bullet_grup, False):
            if player.alive:
                player.health -= 5
                self.kill()
        for enemy in enemy_grup:
            if pygame.sprite.spritecollide(enemy, bullet_grup, False):
                if enemy.alive:
                    enemy.health -= 20
                    self.kill()

        self.rect.x += SCREEN_SCROOL


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 7
        self.vel_y = -13
        self.timer = 100
        self.music = True
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.flip = False
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.vel_y += GRAVITY

        dx = self.speed * self.direction
        dy = self.vel_y

        if self.rect.x + dx <= 0:
            self.direction *= -1

        if self.rect.right + dx >= 800:
            self.direction *= -1

            self.vel_y -= 5

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                self.direction *= -1

            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                if self.vel_y < 0:
                    dy = 0
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    self.vel_y = 0

                    dx = 0

        self.rect.x += SCREEN_SCROOL

        self.timer -= 1

        if self.timer == 0:
            self.kill()
            boom = Explosion(self.rect.centerx, self.rect.centery, 1)
            Explosion_grup.add(boom)

            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE and \
                    abs(self.rect.centery - player.rect.centery) < TILE_SIZE:
                player.health -= 50

            for enemy in enemy_grup:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE and \
                        abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE:
                    enemy.health -= 50

        self.rect.x += dx
        self.rect.y += dy


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = img

        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y)

    def update(self):
        self.rect.x += SCREEN_SCROOL


class Whater(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = img

        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y)

    def update(self):
        self.rect.x += SCREEN_SCROOL


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = img

        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y)

    def update(self):
        self.rect.x += SCREEN_SCROOL


class item_box(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.x = x
        self.y = y
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y)

    def update(self):
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == 'Health':

                player.health += 50

                if player.max_health < player.health:
                    player.health = player.max_health

            if self.item_type == 'Ammo':
                player.ammo += 25

            if self.item_type == 'Grenade':
                player.granades += 5

            self.kill()

        self.rect.x += SCREEN_SCROOL


class Health_bar():
    def __init__(self, health, x, y, wiegth, hieght, px):
        self.health = health
        self.px = px
        self.x = x
        self.y = y
        self.hieght = hieght
        self.wieght = wiegth

    def drow(self):
        pygame.draw.rect(screen, (0, 0, 0), (
            self.x - self.px, self.y - self.px, self.x + player.max_health + self.px * 2,
            self.y + self.hieght + self.px * 2), 5, 10)
        pygame.draw.rect(screen, (207, 24, 4), (self.x, self.y, self.x + player.max_health, self.y + self.hieght),
                         border_radius=10)
        if player.health <= 100:
            pygame.draw.rect(screen, (0, 255, 0),
                             (self.x, self.y, self.x + player.max_health / 100 * player.health, self.y + self.hieght),
                             border_radius=10)
        else:
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.x + 100, self.y + self.hieght),
                             border_radius=10)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.image_spis = []
        for i in range(1, 6):
            img = pygame.image.load(f"img/exposion/exp{i}.png")
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            self.image_spis.append(img)
        self.frame_index = 0
        self.image = self.image_spis[self.frame_index]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = random.randint(2, 7)

    def update(self):
        grand_boom_spis[random.randint(0, len(grand_boom_spis) - 1)].play()

        EXPLOSION_SPEED = 4

        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1

            if self.frame_index >= 5:
                self.kill()
            else:
                self.image = self.image_spis[self.frame_index]

        self.rect.x += SCREEN_SCROOL


# create grup sprite
enemy_grup = pygame.sprite.Group()
bullet_grup = pygame.sprite.Group()
Grenade_grup = pygame.sprite.Group()
Explosion_grup = pygame.sprite.Group()
item_boxes_grup = pygame.sprite.Group()
decoration_grup = pygame.sprite.Group()
whater_grup = pygame.sprite.Group()
exit_grup = pygame.sprite.Group()

world_data = []

for i in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
            # if int(tile) == 15:
            #     print("YES")

world = World()
# print(world.procss_data(world_data))
player, health_bar = world.procss_data(world_data)

run = True
while run:
    draw_bg()

    world.draw()

    drow_text("health: " + str(player.health), sys_font, font_colour, 600, 25)
    drow_text("ammo: " + str(player.ammo), sys_font, font_colour, 600, 50)
    drow_text("granades: " + str(player.granades), sys_font, font_colour, 600, 75)
    if player.reloading:
        drow_text("You can shoot!", sys_font, font_colour, 50, 50)
    else:
        drow_text("You can not shoot!", sys_font, font_colour, 50, 50)
        if player.can_reload:
            drow_text(f"coldown: {player.culdown_ammo}/150", sys_font, font_colour, 75, 75)
        else:
            drow_text("Press R to reload!", sys_font, font_colour, 75, 75)

    health_bar.drow()

    for enemy in enemy_grup:
        enemy.draw()
        enemy.update()
        enemy.ai()

    player.draw()

    SCREEN_SCROOL = player.move(moving_left, moving_right)
    BG_SCROOL -= SCREEN_SCROOL
    player.update()

    Grenade_grup.update()

    bullet_grup.update()
    bullet_grup.draw(screen)

    # random_drop()

    Grenade_grup.update()
    Grenade_grup.draw(screen)

    Explosion_grup.update()
    Explosion_grup.draw(screen)

    item_boxes_grup.update()
    item_boxes_grup.draw(screen)

    decoration_grup.update()
    decoration_grup.draw(screen)

    whater_grup.update()
    whater_grup.draw(screen)

    exit_grup.update()
    exit_grup.draw(screen)

    if player.ammo_to_reload != 0:
        player.reloading = True
    else:
        player.reloading = False

    if player.can_reload:
        player.culdown_ammo += 1

        if player.culdown_ammo >= 150:
            player.ammo_to_reload = 25
            player.culdown_ammo = 0
            player.can_reload = False

    if player.alive:
        if shoot:
            player.shoot()
        elif grand and player.granades > 0:
            grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), \
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
                shoot = True

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
                shoot = False

            if event.key == pygame.K_q:
                grand = True
            if event.key == pygame.K_r:
                if player.ammo_to_reload <= 0:
                    player.can_reload = True

            if razrab:
                if event.key == pygame.K_k:
                    player.alive = False
                    player.health = 0
                    player.update_action(3)
                if event.key == pygame.K_l:
                    player.alive = True

                    player.update_action(0)

                    player.health += 50
                if event.key == pygame.K_p:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(f"music/{random.randint(0, music_len_spis)}.mp3")
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)

                if event.key == pygame.K_o:
                    player.granades += 1
                if event.key == pygame.K_n:
                    player.ammo += 5

                if event.key == pygame.K_i:
                    if multy_jump == False:
                        multy_jump = True
                    else:
                        multy_jump = False

                if event.key == pygame.K_u:
                    if mouse_raz == False:
                        mouse_raz = True
                    else:
                        mouse_raz = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if razrab:
                if mouse_raz:
                    if event.button == 1:
                        player.rect.center = event.pos
                        player.jump = True
                        player.in_air = False
                    if event.button == 2:
                        BG = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    if event.button == 3:
                        font_colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    pygame.display.update()
    clock.tick(FPS)
