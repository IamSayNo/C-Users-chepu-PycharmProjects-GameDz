import pygame, random
pygame.init()

size = (1200, 700)

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Zombies attack')
icon = pygame.image.load('icon.png')
icon = pygame.transform.scale(icon, (50, 50))
pygame.display.set_icon(icon)

background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (size[0], size[1]))

pygame.mixer.music.load('Musics/Menu_music.mp3')
pygame.mixer.music.play(-1)

font = pygame.font.Font(None, 70)

sound_mode = True

def sound_set_buttom_draw(sound_set):
    sound_buttom = pygame.image.load('Buttoms/Sound/' + str(sound_set) + '.jpg')
    sound_buttom = pygame.transform.scale(sound_buttom, (40, 40))
    sound_buttom.set_colorkey((255, 255, 255))
    screen.blit(sound_buttom, (size[0] - 70, 20))

play_buttom = pygame.image.load('Buttoms/Start_game.jpg')
play_buttom = pygame.transform.scale(play_buttom, (100, 60))
def start_game_bottom_draw():
    screen.blit(play_buttom, (size[0] // 2 - 100, size[1] - 80))

stop_buttom = pygame.image.load('Buttoms/stop_level.png')
stop_buttom = pygame.transform.scale(stop_buttom, (50, 50))
stop_buttom.set_colorkey((255, 255, 255))
def stop_buttom_draw():
    screen.blit(stop_buttom, (30, 30))

inst_buttom = pygame.image.load('Buttoms/inst.png')
inst_buttom = pygame.transform.scale(inst_buttom, (150, 50))
def inst_button_draw():
    screen.blit(inst_buttom, (900, 20))

inst_background = pygame.image.load('inst_background.png')
def inst_draw():
    screen.blit(inst_background, (350, 250))

bullet_img = pygame.image.load('bullet.jpg')
gun_ready = True
b_x = 60
b_y = 540
def shoot_draw():
    screen.blit(bullet_img, (b_x, b_y))

gun_q = 0
gun_need = 15

player_img = pygame.image.load('Player.png')
player_img = pygame.transform.scale(player_img, (35, 70))
player_img.set_colorkey((255, 255, 255))
player_y = 540

zombies = []
num_zombies = 6
for _ in range(num_zombies):
    zombies.append([100, random.randint(570, 630), random.randint(1000, 1220), random.randint(1, 2)])

player_damg = 20
base_hp = 100

lose = False

lose_img = pygame.image.load('lose_img.png')
lose_img = pygame.transform.scale(lose_img, (600, 120))
lose_img.set_colorkey((255, 255, 255))

with open('Best_score.txt', 'r') as file:
    best_score = file.read()

menu_mode = True
inst_mode = False
q = 1
q2 = 0

score = 0
while True:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if menu_mode and lose:
                lose = False
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if menu_mode and lose:
                lose = False

            if (mouse_pos[0] > 500 and mouse_pos[0] < 600) and (mouse_pos[1] < 680 and mouse_pos[1] > 560) and menu_mode and not inst_mode:
                score = 0
                pygame.mixer.music.stop()
                pygame.mixer.music.load('Musics/Game_music.mp3')
                pygame.mixer.music.play(-1)
                menu_mode = False
                lose = False

            elif (mouse_pos[0] > size[0] - 70 and mouse_pos[0] < size[0] - 30) and (mouse_pos[1] > 20 and mouse_pos[1] < 60):
                sound_mode = not sound_mode
                pygame.mixer.music.set_volume(int(sound_mode))
                lose = False

            elif (mouse_pos[0] > 30 and mouse_pos[0] < 80) and (mouse_pos[1] > 30 and mouse_pos[1] < 80) and not menu_mode:
                pygame.mixer.music.stop()
                pygame.mixer.music.load('Musics/Menu_music.mp3')
                pygame.mixer.music.play(-1)
                menu_mode = True

                zombies = []
                num_zombies = 5
                for _ in range(num_zombies):
                    zombies.append([100, random.randint(500, 630), random.randint(1000, 1220), random.randint(2, 4)])

            elif (mouse_pos[0] > 900 and mouse_pos[0] < 1050) and (mouse_pos[1] > 20 and mouse_pos[1] < 70) and menu_mode:
                inst_mode = not inst_mode

    key = pygame.key.get_pressed()
    if key[pygame.K_UP] and player_y >= 530:
        player_y -= 0.8
    elif key[pygame.K_DOWN] and player_y <= 630:
        player_y += 0.8

    elif key[pygame.K_SPACE] and gun_ready and not menu_mode and gun_q == gun_need:
        b_x = 60
        b_y = player_y + 38
        gun_q = 0
        gun_ready = False

    sound_set_buttom_draw(int(sound_mode))

    if not gun_ready:
        b_x += 30
        shoot_draw()
        if b_x >= size[0]:
            gun_ready = True

    if menu_mode:
        if not inst_mode:
            start_game_bottom_draw()
        inst_button_draw()
        q = 1
        q2 = 0
        if inst_mode:
            inst_draw()

        with open('Best_score.txt', 'r') as file:
            best_score = file.read()
        best_score_draw = font.render('Record: ' + best_score, True, (0, 0, 0))
        screen.blit(best_score_draw, (20, 20))

    else:
        stop_buttom_draw()
        screen.blit(player_img, (60, player_y))

        q2 += 1
        if q2 == 35:
            q += 1
            q2 = 0
        if q > 4:
            q = 1

        pygame.draw.rect(screen, (0, 0, 0), (200, 20, 320, 60))
        pygame.draw.rect(screen, (255, 0, 0), (210, 30, base_hp * 3, 40))

        if not menu_mode:
            for i in range(num_zombies):

                zombie = zombies[i]

                zombies_img = pygame.image.load('Zombie_an/' + str(q) + '.bmp')
                zombies_img = pygame.transform.scale(zombies_img, (45, 70))
                zombie_rect = zombies_img.get_rect(center=(zombie[2], zombie[1] + 17))
                zombies_img.set_colorkey((255, 255, 255))
                screen.blit(zombies_img, (zombie[2], zombie[1]))
                zombie[2] -= zombie[3]

                player_rect = player_img.get_rect(center=(60, player_y))
                if zombie[2] <= -35 or player_rect.colliderect(zombie_rect):
                    base_hp -= 10
                    zombies[i] = [100, random.randint(570, 630), random.randint(1000, 1220), random.randint(1, 3)]

                b_rect = bullet_img.get_rect(center=(b_x, b_y))
                if b_rect.colliderect(zombie_rect) and not gun_ready:
                    zombies[i][0] -= player_damg
                    gun_ready = True

                if zombies[i][0] == 0:
                    zombies[i] = [100, random.randint(570, 630), random.randint(1000, 1220), random.randint(1, 3)]
                    score += 1

        if gun_q < gun_need:
            player_img = pygame.image.load('Shoot.png')
            player_img = pygame.transform.scale(player_img, (46, 70))
            player_img.set_colorkey((255, 255, 255))
            gun_q += 1

        else:
            player_img = pygame.image.load('Player.png')
            player_img = pygame.transform.scale(player_img, (38, 70))
            player_img.set_colorkey((255, 255, 255))

        if base_hp == 0:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('Musics/Menu_music.mp3')
            pygame.mixer.music.play(-1)
            menu_mode = True
            lose = True
            base_hp = 100

            if int(best_score) < score:
                with open('Best_score.txt', 'w') as file:
                    file.write(str(score))

        score_draw = font.render('Score: ' + str(score), True, (0, 0, 0))
        screen.blit(score_draw, (800, 20))

    if lose:
        screen.blit(lose_img, (300, 290))

    pygame.display.update()