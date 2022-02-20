import pygame
import random
import math
from pygame import mixer
# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))


# background
background = pygame.image.load("background.png")
# background music
mixer.music.load("background.wav")
mixer.music.play(-1)
# title
pygame.display.set_caption("space invaders")
icon = pygame.image.load('001-ufo.png')
pygame.display.set_icon(icon)

# player image
playerimg = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6
for i in range(no_of_enemies):
    enemyimg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
# ready - you cant see the bullet on the screen
# Fire = the bullet is currently moving
Bulletimg = pygame.image.load("bullet.png")
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 10
Bullet_state = "ready"
# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)
# game over score
final_score = 0
font = pygame.font.Font('freesansbold.ttf', 50)


def show_score(x, y):
    score = font.render("score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    final_score = font.render("score: " + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    screen.blit(final_score, (264, 314))


def player(x, y):
     screen.blit(playerimg, (x, y))


def enemy(x, y, i):
     screen.blit(enemyimg[i], (x, y))

def fire_bullet(x,y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(Bulletimg, (x + 16, y + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2))+(math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
#game loop
running = True
while running:
    # RGB colors
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystorke is pressed check whether right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change= 5
            if event.key == pygame.K_SPACE:
               if Bullet_state == "ready":
                 bullet_sound = mixer.Sound('laser.wav')
                 bullet_sound.play()
                 #gets the current x coordinate of the spaceship
                 BulletX = playerX
                 fire_bullet(BulletX,BulletY)

        if event.type == pygame.KEYUP:
           if event.key == pygame.K_LEFT or event.key== pygame.K_RIGHT:
                playerX_change = 0

    #adding boundary
    #player moment
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >=736:
        playerX = 736

    # enemy moment
    for i in range(no_of_enemies):
        #game over
        if enemyY[i] > 440:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
                game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i]= 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] =-3

            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], BulletX, BulletY)
        if collision:
             explosion_sound = mixer.Sound("explosion.wav")
             explosion_sound.play()
             BulletY = 480
             Bullet_state = "ready"
             score_value += 1
             enemyX[i] = random.randint(0, 735)
             enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    #bullet moment
    if BulletY <= 0:
        BulletY = 480
        Bullet_state =  "ready"
    if Bullet_state == "fire":
        fire_bullet(BulletX,BulletY)
        BulletY -= BulletY_change


    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()