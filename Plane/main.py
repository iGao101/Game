import codecs
import pygame
from pygame.locals import *  # 常量
from sys import exit
import time
import random

# 设置屏幕大小
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 700

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10  # 子弹速度
        self.damage = 1

    # 子弹移动
    def move(self):
        self.rect.top -= self.speed

    def enemies_move(self):
        self.rect.top += self.speed


# 玩家飞机类
class Player(pygame.sprite.Sprite):
    # 图片  图片位置  飞机位置
    def __init__(self, player_image, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 6
        self.bullets = pygame.sprite.Group()  # 发射的子弹
        self.is_hit = False  # 是否被击中
        self.image_index = 0  # 飞机图片索引
        self.image = player_image[self.image_index]  # 根据索引选择飞机相应状态的图片
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.interval = 0.2  # 发射间隔
        self.blood = 3  # 玩家血量

    # 发射子弹
    def shoot(self, bullet_image):
        bullet = Bullet(bullet_image, self.rect.midtop)
        self.bullets.add(bullet)

    # 飞机移动
    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0  # 防止超出边界
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height  # 防止超出边界
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0  # 防止超出边界
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width  # 防止超出边界
        else:
            self.rect.left += self.speed


# 敌机
class Enemy(pygame.sprite.Sprite):
    # 敌机图片   敌机类型  位置
    def __init__(self, enemy_img, kind, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.speed = 2
        self.bullets = pygame.sprite.Group()  # 敌机发射的子弹
        self.kind = kind + 1  # 取值范围为：1-3
        self.blood = kind + 1  # 三种敌机血量
        self.index = 0  # 坠机动画中的索引
        self.interval = 1.8  # 敌机发射子弹时间间隔
        self.start = time.time()  # 敌机被制造出来的时间

    # 敌机移动
    def move(self):
        self.rect.top += self.speed

    # 敌机发射子弹
    def shoot(self, bullets_image):
        bullet = Bullet(bullets_image[self.kind - 1], self.rect.midbottom)
        bullet.damage = self.kind
        if self.kind == 1:
            bullet.speed = 5
            self.interval = 1.2
        else:
            bullet.speed = 3
        return bullet


# 初始化pygame
pygame.init()
# 初始化混音器模块
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# 窗口名
pygame.display.set_caption("SpaceWar")
# 设置窗口图标
# ic_launcher = pygame.image.load("photoes/ic_launcher.jpg")
# pygame.display.set_icon(ic_launcher)
# 背景图片
background = pygame.image.load("photoes/background.png")
# 设置背景音乐
pygame.mixer.music.load("sounds/background.wav")
pygame.mixer.music.set_volume(0.2)  # 设置音量
# 游戏结束图片
again = pygame.image.load("photoes/again.png")
# 暂停
pause = pygame.image.load("photoes/pause_pressed.png")
# 恢复
resume = pygame.image.load("photoes/resume_pressed.png")
# 玩家飞机图片
player_img = []
player_img.append(pygame.image.load("photoes/me1.png"))
player_img.append(pygame.image.load("photoes/me2.png"))
# 玩家子弹图片
bullet_img = pygame.image.load("photoes/bullet1.png")
# 敌机发射的子弹
enemies_bullet_img = []
enemies_bullet_img.append(pygame.image.load("photoes/bullet2.png"))
enemies_bullet_img.append(pygame.image.load("photoes/bullet_supply.png"))
enemies_bullet_img.append(pygame.image.load("photoes/bomb_supply.png"))
# 敌机
enemies_img = []
enemies_img.append(pygame.image.load("photoes/enemy1.png"))
enemies_img.append(pygame.image.load("photoes/enemy2.png"))
enemies_img.append(pygame.image.load("photoes/enemy3_n1.png"))
# 玩家飞机坠毁图片
players_down = []
for i in range(1, 4):
    img = pygame.image.load("photoes/me_destroy_%s.png" % str(i))
    players_down.append(img)
# 敌机坠毁动画，敌机类型也存在差异
# 类型1坠机动画
enemies1_down_img = []
enemies1_down_img.append(pygame.image.load("photoes/enemy_down1.png"))
enemies1_down_img.append(pygame.image.load("photoes/enemy_down2.png"))
enemies1_down_img.append(pygame.image.load("photoes/enemy_down3.png"))
# 类型2坠机动画
enemies2_down_img = []
enemies2_down_img.append(pygame.image.load("photoes/enemy2_down1.png"))
enemies2_down_img.append(pygame.image.load("photoes/enemy2_down2.png"))
enemies2_down_img.append(pygame.image.load("photoes/enemy2_down3.png"))
# 类型3坠机动画
enemies3_down_img = []
enemies3_down_img.append(pygame.image.load("photoes/enemy3_down1.png"))
enemies3_down_img.append(pygame.image.load("photoes/enemy3_down2.png"))
enemies3_down_img.append(pygame.image.load("photoes/enemy3_down3.png"))
enemies3_down_img.append(pygame.image.load("photoes/enemy3_down4.png"))
enemies3_down_img.append(pygame.image.load("photoes/enemy3_down5.png"))
# 敌机坠机动画二维数组
enemies_down_img = []
enemies_down_img.append(enemies1_down_img)
enemies_down_img.append(enemies2_down_img)
enemies_down_img.append(enemies3_down_img)
# 设置游戏音乐
# 查看排行榜音效
rangking_sound = pygame.mixer.Sound("sounds/ranking.wav")
rangking_sound.set_volume(0.3)
# 玩家飞机发射子弹声效
player_shoot = pygame.mixer.Sound("sounds/me_shoot.wav")
player_shoot.set_volume(0.3)
# 游戏结束音效
over_sound = pygame.mixer.Sound("sounds/gameover.wav")
over_sound.set_volume(0.3)
# 敌方发射子弹声效
enemy3_shoot = pygame.mixer.Sound("sounds/shoot3.wav")
enemy3_shoot.set_volume(0.3)
# 飞机爆炸
plane_collision = pygame.mixer.Sound("sounds/collision.wav")
plane_collision.set_volume(0.4)


# 读取文件历史纪录分数
def readScores(path):
    with open(path, 'r', encoding="utf8") as f:
        lines = f.readlines()
    return lines


# 将成绩写入文件
def writeScores(context, srtim, path):
    f = codecs.open(path, srtim, "utf8")
    f.write(str(context))
    f.close()


# 游戏结束
def gameOver(scores):
    x = screen.get_rect().centerx
    y = screen.get_rect().centery
    # 重新开始
    start = pygame.font.Font(None, 45)
    start_text = start.render("New Game", True, (90, 160, 100))
    start_rect = start_text.get_rect()
    start_rect.centerx = x
    start_rect.centery = y + 40
    screen.blit(start_text, start_rect)

    # 显示游戏最终得分
    myfont = pygame.font.Font(None, 60)
    text = myfont.render("Scores: %s" % str(scores), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = y - 50
    screen.blit(text, text_rect)

    # 排行榜
    text = start.render("Ranking List", True, (90, 160, 100))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = y + 130
    screen.blit(text, text_rect)

    # 更新排行榜信息
    scores_array = readScores(r'score.txt')[0].split('mr')

    # 如果分数大于历史前三则显示破纪录的标签
    if scores >= int(scores_array[2]):
        start = pygame.font.Font(None, 70)
        text = start.render("NEW RECORD!!!", True, (255, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = x
        text_rect.centery = y - 160
        screen.blit(text, text_rect)

    temp = 0
    for i in range(0, len(scores_array)):
        # 判断当前获取的分数是否大于排行榜中的分数
        if scores > int(scores_array[i]):
            temp = int(scores_array[i])
            scores_array[i] = str(scores)
            scores = 0
        if temp > int(scores_array[i]):
            k = int(scores_array[i])
            scores_array[i] = str(temp)
            temp = k

    # 进行写入
    for i in range(0, len(scores_array)):
        if i == 0:
            writeScores(scores_array[i] + 'mr', 'w', 'score.txt')
        elif i == 9:
            writeScores(str(scores_array[i]), 'a', 'score.txt')
        else:
            writeScores(scores_array[i] + 'mr', 'a', 'score.txt')


# 显示得分
def showScores(scores):
    myfont = pygame.font.Font(None, 30)
    text = myfont.render("Scores: %s" % str(scores), True, (0, 0, 0))
    screen.blit(text, (320, 30))
    pygame.display.update()


# 显示暂停
def showPaused():
    myfont = pygame.font.Font(None, 60)
    text = myfont.render("Paused!!!", True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 30
    screen.blit(text, text_rect)
    pygame.display.update()


# 显示排行榜
def gameRanking():
    screen2 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen2.fill(0)
    screen2.blit(background, (0, 0))

    x = screen.get_rect().centerx
    y = screen.get_rect().centery
    # 显示排行榜文字
    myfont = pygame.font.Font(None, 60)
    text = myfont.render("Ranking List", True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = 50
    screen.blit(text, text_rect)

    # 重新开始
    start = pygame.font.Font(None, 45)
    start_text = start.render("New Game", True, (90, 160, 100))
    start_rect = start_text.get_rect()
    start_rect.centerx = x
    start_rect.centery = y + 40
    screen.blit(start_text, start_rect)

    # 获取文件中存储的分数记录
    scores_array = readScores(r'score.txt')[0].split('mr')
    text = start.render("Num1: %s" % scores_array[0], True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = 150
    screen.blit(text, text_rect)

    # 第二
    text = start.render("Num2: %s" % scores_array[1], True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = 200
    screen.blit(text, text_rect)

    # 第三
    text = start.render("Num3: %s" % scores_array[2], True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.centery = 250
    screen.blit(text, text_rect)


# 开始游戏
def startGame():
    scores = 0  # 得分
    player_pos = [180, 580]
    enemy_pos = [[random.randint(0, 50), -250], [random.randint(150, 200), -250], [random.randint(300, 350), -250]]
    player = Player(player_img, player_pos)

    global running  # 判断是否在游戏中
    running = True
    global is_paused  # 是否处于暂停状态
    is_paused = False
    start = time.time()  # 玩家开始时间，用于控制发射间隔
    change_times = 1  # 飞机闪耀
    arrive_times = 1  # 敌机出现时间间隔
    enemies_bomb = 1  # 敌机爆炸间隔
    bomb_times = 0.04  # 飞机爆炸动画
    enemies = pygame.sprite.Group()  # 敌机集合
    enemies_down = pygame.sprite.Group()  # 敌机坠机集合，用来播放坠机动画
    enemies_bullet = pygame.sprite.Group()  # 敌机发射的子弹集合

    # 游戏主循环
    while running:
        # 循环播放
        if not pygame.mixer.music.get_busy():  # 返回1代表正在播放
            pygame.mixer.music.play()  # 播放音乐
        screen.fill(0)
        screen.blit(background, (0, 0))  # 设置背景图片
        if is_paused == False:
            screen.blit(pause, (30, 10))  # 显示暂停按钮
        else:
            screen.blit(resume, (30, 10))  # 显示暂停按钮

        # 如果结束，程序退出
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and running:
                # 暂停
                if 30 <= event.pos[0] and event.pos[0] <= 80 and 60 >= event.pos[1] and event.pos[1] >= 10:
                    is_paused = True if is_paused == False else False

        # 如果游戏被暂停停止所有行为
        if is_paused:
            showPaused()
            continue;

        # 如果没有被击中
        if not player.is_hit:
            screen.blit(player.image, player.rect)
            if change_times % 55 == 0 and player.blood == 3:
                player.image_index = 1 if player.image_index % 2 == 0 else 0
                player.image = player_img[player.image_index]
                change_times = 0
            # 玩家受到伤害时改变闪烁状态
            elif change_times % 55 == 0 and player.blood < 3:
                player.image_index = 1 if player.image_index % 2 == 0 else 0
                if player.image_index == 1:
                    player.image = players_down[0]
                else:
                    player.image = player_img[player.image_index]
                change_times = 0
            change_times += 1

        # 产生敌机
        if arrive_times % 100 == 0:
            type = random.randint(0, len(enemies_img) - 1)
            pos = random.randint(0, len(enemies_img) - 1)
            enemy = Enemy(enemies_img[type], type, enemy_pos[2 - pos])
            enemies.add(enemy)
            arrive_times = 1
        arrive_times += 1

        # 敌机移动，超出边界删除对象
        for enemy in enemies:
            enemy.move()  # 敌机移动
            if time.time() - enemy.start > enemy.interval:
                if enemy.kind == 1:
                    player_shoot.play()
                else:
                    enemy3_shoot.play()
                enemies_bullet.add(enemy.shoot(enemies_bullet_img))
                enemy.start = time.time()
            # 敌机越界注销
            if enemy.rect.top > SCREEN_HEIGHT:
                enemies.remove(enemy)
            # 发生碰撞
            if pygame.sprite.collide_rect(enemy, player):
                enemies.remove(enemy)
                player.is_hit = True
                break
            enemy.bullets.draw(screen)

        # 敌机发射的子弹
        for enemy_bullet in enemies_bullet:
            enemy_bullet.enemies_move()
            # 越界注销
            if enemy_bullet.rect.top > SCREEN_HEIGHT:
                enemies_bullet.remove(enemy_bullet)
            # 与玩家的碰撞检测
            if pygame.sprite.collide_rect(enemy_bullet, player):
                enemies_bullet.remove(enemy_bullet)
                player.blood -= enemy_bullet.damage
            if player.blood <= 0:
                player.blood = 0
                player.is_hit = True
        enemies_bullet.draw(screen)

        # 如果玩家和敌机发生碰撞
        if player.is_hit:
            plane_collision.play()  # 播放爆炸声效
            over_sound.play()  # 游戏结束声效
            temp_time = time.time()
            j = 0
            # 产生碰撞动画
            while True:
                if time.time() - temp_time > bomb_times:
                    screen.blit(players_down[j], player.rect)
                    temp_time = time.time()
                    if j == len(players_down) - 1:
                        running = False
                        break
                    j += 1
        enemies.draw(screen)

        # 获取键盘事件
        key_pressed = pygame.key.get_pressed()
        # 移动
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()
        # 发射子弹
        if key_pressed[K_k] and time.time() - start >= player.interval:
            player.shoot(bullet_img)
            player_shoot.play()  # 发射子弹声效
            start = time.time()
        # 回收出界子弹
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                player.bullets.remove(bullet)
        # 绘制子弹
        player.bullets.draw(screen)

        # 检测子弹和敌机的碰撞
        for enemy in enemies:
            for bullet in player.bullets:
                # 发生碰撞
                if pygame.sprite.collide_rect(enemy, bullet):
                    player.bullets.remove(bullet)
                    enemy.blood -= bullet.damage
                    # 如果敌机血量小于等于0，则加入坠机队伍
                    if enemy.blood <= 0:
                        enemies_down.add(enemy)
                        plane_collision.play()
                        scores += enemy.kind * 10
                    else:
                        enemy.image = enemies_down_img[enemy.kind - 1][enemy.index]
                        enemy.index += 1
        # 显示分数
        showScores(scores)

        # 展示敌机爆炸动画
        for enemy in enemies_down:
            if enemies_bomb % 5 == 0:
                enemy.image = enemies_down_img[enemy.kind - 1][enemy.index]
                enemy.index += 1
                enemies_bomb = 0
            if enemy.index == len(enemies_down_img[enemy.kind - 1]):
                enemies.remove(enemy)
                enemies_down.remove(enemy)
        enemies_bomb += 1
        pygame.display.update()  # 更新屏幕

    # 游戏结束显示最终得分
    if not is_paused:
        gameOver(scores)


# 开始游戏
startGame()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # 判断鼠标点击事件
        elif event.type == pygame.MOUSEBUTTONDOWN and not running and not is_paused:
            x = screen.get_rect().centerx
            y = screen.get_rect().centery
            # 重新开始游戏
            if x - 100 <= event.pos[0] and event.pos[0] <= x + 100 and y + 70 >= event.pos[1] and event.pos[1] >= y + 40:
                startGame()

            # 显示排行榜
            if x - 120 <= event.pos[0] and event.pos[0] <= x + 120 and y + 160 >= event.pos[1] and event.pos[1] >= y + 130:
                rangking_sound.play()  # 播放查看排行榜音效
                gameRanking()

    pygame.display.update()
