import pygame
import random
from time import sleep

white = (255, 255, 255)
screen_width = 601
screen_height = 800
clock = pygame.time.Clock()
gamepad = pygame.display.set_mode((screen_width, screen_height))
start_page = pygame.image.load('images/start_page.png')
background = pygame.image.load('images/background.png')
background2 = pygame.image.load('images/background2.png')
jet = pygame.image.load('images/jet.png')
bullet = pygame.image.load('images/bullet.png')
red_dragon = pygame.image.load('images/red_dragon.png')
red_dragon_2 = pygame.image.load('images/red_dragon_2.png')
red_dragon_animation = [red_dragon, red_dragon_2]
white_dragon = pygame.image.load('images/white_dragon.png')
white_dragon_2 = pygame.image.load('images/white_dragon_2.png')
white_dragon_animation = [white_dragon, white_dragon_2]
yellow_dragon = pygame.image.load('images/yellow_dragon.png')
yellow_dragon_2 = pygame.image.load('images/yellow_dragon_2.png')
yellow_dragon_animation = [yellow_dragon, yellow_dragon_2]
explosion = pygame.image.load('images/explosion.png')
press_one = pygame.image.load('images/press_one.png')
press_two = pygame.image.load('images/press_two.png')
press_three = pygame.image.load('images/press_three.png')
press_four = pygame.image.load('images/press_four.png')
press_animation = [press_one, press_two, press_three, press_four]
life1 = pygame.image.load('images/life1.png')
life2 = pygame.image.load('images/life2.png')
life3 = pygame.image.load('images/life3.png')
life = [life1, life2, life3]
gameover = pygame.image.load('images/gameover.jpg')
background_fall = pygame.image.load('images/background_fall.png')
background_fall_2 = pygame.image.load('images/background_fall_2.png')
booster = pygame.image.load('images/booster.png')




def runGame():
    # get_rect() 객체에 대한 사각형 영억을 만들어줌,
    # size는 해당 사각형의 가로와 세로 크기를 튜플로 반환
    jet_size = jet.get_rect().size
    jet_width = jet_size[0]
    jet_height = jet_size[1]

    bullet_size = bullet.get_rect().size
    bullet_width = bullet_size[0]
    bullet_height = bullet_size[1]

    x_change = 0

    background_y = 0
    background2_y = -screen_height
    # background3_y = 2 * screen_height

    # booster_size = booster.get_rect().size
    # booster_x = random.randrange(0, screen_width - booster_size[0])
    # booster_y += 7
    # gamepad.blit(booster, (booster_x, booster_y))

    x = screen_width * 0.05
    y = screen_height * 0.8

    bullet_xy = []
    shot_dragon = False
    kill_dragon_count = 0
    passed_dragon_count = 0
    font = pygame.font.Font(None, 36)

    # 램덤으로 적 출현시키기
    # red_enemy = [red_dragon, red_dragon_2]
    # white_enemy = [white_dragon, white_dragon_2]
    # yellow_enemy = [yellow_dragon, yellow_dragon_2]

    enemies = [red_dragon, white_dragon, yellow_dragon]
    # enemy = random.choice(enemies)

    enemy_animation = [red_dragon_animation, white_dragon_animation, yellow_dragon_animation]
    enemy_index = random.randint(0, len(enemies) - 1)
    enemy_animation = enemy_animation[enemy_index]
    enemy_image = enemies[enemy_index]
    animation_timer = pygame.time.get_ticks()



    # 적 출현 위치 정하기
    enemy_size = enemy_image.get_rect().size
    enemy_width = enemy_size[0]
    enemy_x = random.randrange(0, screen_width - enemy_width)
    enemy_y = 0
    animation_index = 0

    # times = pygame.time.Clock()

    elapsed_time = 0  # 경과시간 초기화.. 이걸 계속 while문 안에 넣고있어서 0으로 나왔음 ;;
    life_count = 3
    booster_y = 0

    crashed = False
    while not crashed:
        for event in pygame.event.get():  # 이벤트 발생 여부에 따른 반복문
            # if event.type == pygame.QUIT:
            #     crashed = True

            if event.type == pygame.KEYDOWN: # 만약 키가 눌리는 이벤트가 있다면
                if event.key == pygame.K_LEFT:
                    x_change = -10
                elif event.key == pygame.K_RIGHT:
                    x_change = 10
                elif event.key == pygame.K_SPACE:
                    # missileSound.play
                    bullet_x = x + jet_width/2  # 비행기의 앞부분 중간에서 나가도록 잡아줌
                    bullet_y = y - jet_height
                    bullet_xy.append([bullet_x, bullet_y])

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        x += x_change
        gamepad.fill(white)

        background_y += 5
        background2_y += 5

        if background_y == screen_height:
            background_y = -screen_height

        if background2_y == screen_height:
            background2_y = -screen_height


        # 배경화면 지정
        gamepad.blit(background, (0, background_y))
        gamepad.blit(background2, (0, background2_y))

        # 제트기 위치 지정
        gamepad.blit(jet, (x, y))

        # 총알 위치 지정
        count = 0
        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[1] -= 15
                bullet_xy[i][1] = bxy[1]
                if bxy[1] < enemy_y:
                    if bxy[0] > enemy_x and bxy[0] < enemy_x + enemy_width:
                        # bullet_xy.remove(bxy)
                        # shot_dragon = True
                        count += 1
                        # bullet_xy.remove(bxy)
                        if count == 2:
                            bullet_xy.remove(bxy)
                            kill_dragon_count += 1
                            shot_dragon = True
                if bxy[1] <= 0: # bullet이 화면 밖을 벗어나면 지움
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                gamepad.blit(bullet,(bx, by))

        # 적이 날아오게 하기
        # 드래곤 색깔마다 다가오는 속도를 다르게함
        # if enemy_image == enemies[0]:
        #     enemy_y += 7
        # elif enemy_image == enemies[1]:
        #     enemy_y += 6
        # else:
        #     enemy_y += 5
        enemy_y += 7
        #
        # gamepad.blit(life1, (10, 10))
        # gamepad.blit(life2, (60, 10))
        # gamepad.blit(life3, (110, 10))

        # booster_size = booster.get_rect().size
        # booster_x = random.randrange(0, screen_width - booster_size[0])
        # booster_y += 7
        # gamepad.blit(booster, (booster_x, booster_y))

        if enemy_y > screen_height:
            enemy_animation = [red_dragon_animation, white_dragon_animation, yellow_dragon_animation]
            enemy_index = random.randint(0, len(enemies) - 1)
            enemy_animation = enemy_animation[enemy_index]
            enemy_image = enemies[enemy_index]
            enemy_x = random.randrange(0, screen_width - enemy_width)
            enemy_y = 0
            life_count -= 1
            # booster_x = random.randrange(0, screen_width - booster_size[0])
            # booster_y += 7

        tao = font.render(f"LIFE: {life_count} ", True, (255, 255, 255))
        gamepad.blit(tao, (10,10))

        if life_count == 0:
            crashed = True
            gamepad.blit(gameover, (0, 0))
            kill_dragon_count= font.render(f"{kill_dragon_count} ", True, (0, 0, 0))
            gamepad.blit(kill_dragon_count, (300, 480))
            elapsed_text = font.render("{:.2f} m".format(elapsed_time), True, (0, 0, 0))
            gamepad.blit(elapsed_text, (230, 350))




        current_time = pygame.time.get_ticks()


        if current_time - animation_timer >= 300:  # 1초마다 애니메이션 변경
            animation_timer = current_time
            animation_index = (animation_index + 1) % len(enemy_animation)

        if shot_dragon is True:
            gamepad.blit(explosion, (enemy_x, enemy_y))
            enemy_x = random.randrange(0, screen_width - enemy_width)
            enemy_y = 0
            shot_dragon = False

        # 화면에 적 이미지 그리기
        gamepad.blit(enemy_animation[animation_index], (enemy_x, enemy_y))



        # 초당 1m 가는 것 구현
        dt = clock.tick(60) / 1000.0  # 경과 시간(초) 계산, (/1000.0) -> 밀리초를 초단위로 변경
        elapsed_time += dt

        if not crashed:
            elapsed_text_1 = font.render("flight distance: ", True, (255, 255, 255))
            elapsed_text = font.render("{:.2f} m".format(elapsed_time), True, (255, 255, 255))
            gamepad.blit(elapsed_text_1, (screen_width - elapsed_text_1.get_width() - 100, 10))
            gamepad.blit(elapsed_text, (screen_width - elapsed_text.get_width() - 10, 10))


        if elapsed_time >= 20:
            enemy_y += 8




        pygame.display.update()
        clock.tick(60)  # 1초당 60프레임을 화면에 보여줌
    # pygame.quit()
    # quit()



def main():
    pygame.init()
    # 타이틀 만들기
    pygame.display.set_caption('DRAGON STRIKER')
    gamepad.blit(start_page,(0,0))

    pygame.display.update()
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if event.type == pygame.KEYDOWN:  # 만약 키가 눌리는 이벤트가 있다면
                if event.key == pygame.K_SPACE:

                    runGame()

    clock.tick(60)
if __name__ == '__main__':
    main()
