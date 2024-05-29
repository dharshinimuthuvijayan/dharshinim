import pygame
import math
import random

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
bg = pygame.image.load('bg.jpg')

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo (1).png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('rocket (2).png')
playerX = 370
playerY = 480
playerX_change = 0

# Ghost
ghostImg = []
ghostX = []
ghostY = []
ghostX_change = []
ghostY_change = []
num_of_ghosts = 6

for i in range(num_of_ghosts):
    ghostImg.append(pygame.image.load('ghost.png'))
    ghostX.append(random.randint(0, 735))
    ghostY.append(random.randint(50, 150))
    ghostX_change.append(4)
    ghostY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Font
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def ghost(x, y, i):
    screen.blit(ghostImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def iscollision(ghostX, ghostY, bulletX, bulletY):
    distance = math.sqrt(math.pow(ghostX - bulletX, 2) + math.pow(ghostY - bulletY, 2))
    return distance < 27


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_ghosts):
        ghostX[i] += ghostX_change[i]
        if ghostX[i] <= 0:
            ghostX_change[i] = 4
            ghostY[i] += ghostY_change[i]
        elif ghostX[i] >= 736:
            ghostX_change[i] = -4
            ghostY[i] += ghostY_change[i]

        collision = iscollision(ghostX[i], ghostY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            ghostX[i] = random.randint(0, 736)
            ghostY[i] = random.randint(50, 150)

        ghost(ghostX[i], ghostY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()

pygame.quit()