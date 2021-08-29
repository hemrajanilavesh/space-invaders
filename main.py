import pygame
import random
import math

# Initialize the pygame
pygame.init()

# create a 800 x 600 screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('img/background.jpg')

# Title and Icon of the Game Window
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('img/game_icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('img/spaceship.png')
playerX = 370  # x-axis co-ordinate of the player image
playerY = 520  # y -axis co-ordinate of the player image
playerX_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('img/enemy.png'))
    enemyX.append(random.randint(0, 735))  # x-axis co-ordinate of the enemy image - randomly generated
    enemyY.append(random.randint(20, 100))  # y -axis co-ordinate of the enemy image - randomly generated
    enemyX_change.append(0.5)
    enemyY_change.append(20)

# Score
score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
game_over_font = pygame.font.Font('freesansbold.ttf', 32)
textX = 600
textY = 10

# Missile
# Ready - Missile is stationary.
# Fire - Missile is fired and is in motion.
missileImg = pygame.image.load('img/missile.png')
missileX = 0  # x-axis co-ordinate of the missile image
missileY = 480  # y -axis co-ordinate of the missile image
missileX_change = 0
missileY_change = 5
missile_state = "ready"


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missileImg, (x + 16, y + 10))


# check if the missile & enemy has collided and take appropriate action
# https://www.mathplanet.com/education/algebra-2/conic-sections/distance-between-two-points-and-the-midpoint
def is_collision(enemyX, enemyY, missileX, missileY):
    distance = math.sqrt((math.pow(enemyX - enemyY, 2)) + (math.pow(missileX - missileY, 2)))
    if distance < 27:
        return True  # its a collision
    return False  # not a collision


def show_score(x, y):
    color_white = (255, 255, 255)
    score_render = score_font.render("SCORE : " + str(score_value), True, color_white)
    screen.blit(score_render, (x, y))


def game_over(x, y):
    color_white = (255, 255, 255)
    game_over_render = game_over_font.render("GAME OVER", True, color_white)
    screen.blit(game_over_render, (x, y))


# Game Loop
running = True

while running:
    # RGB - Red Green Blue
    rgb_values = (0, 0, 0)
    screen.fill(rgb_values)
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # bye-bye
            running = False
        elif event.type == pygame.KEYDOWN:  # some key is pressed
            if event.key == pygame.K_LEFT:  # left key is pressed
                playerX_change -= 0.3
            elif event.key == pygame.K_RIGHT:  # right key is pressed
                playerX_change += 0.3
            elif event.key == pygame.K_SPACE:  # space key is pressed
                if missile_state == "ready":
                    missileX = playerX
                    fire_missile(missileX, playerY)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # boundary check for spaceship
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # size of the image is 64px
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > playerX:
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # move all enemies out of the window
            game_over(250, 250)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # size of the image is 64px
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Missile and Enemy Collision
        collision = is_collision(enemyX[i], enemyY[i], missileX, missileY)
        if collision:
            # reset the bullet so that it can be fired again
            missileY = 480
            missile_state = "ready"
            score_value += 1
            # reset the enemy
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(20, 100)
        enemy(enemyX[i], enemyY[i], i)  # updates the co-ordinates of the enemy

    # Missile Movement
    if missileY <= 0:
        # reset the bullet so that it can be fired again
        missileY = 480
        missile_state = "ready"

    if missile_state is "fire":
        fire_missile(missileX, missileY)
        missileY -= missileY_change

    player(playerX, playerY)  # updates the co-ordinates of the player
    show_score(textX, textY)
    pygame.display.update()
