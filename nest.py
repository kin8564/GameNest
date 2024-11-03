import pygame
from pygame.locals import *
import random

# Init pygame and joystick
pygame.init()
pygame.joystick.init()

# Game clock for framerate
clock = pygame.time.Clock()

# Creates game screen
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Assets
player = pygame.image.load("bfb.png")
player = pygame.transform.scale(player, (50, 50))  # Resize for game
ground = pygame.Surface((screen_width, 40))  # Ground surface
ground.fill((83, 83, 83))  # Gray color for ground

# Player state
playerX = 320
playerY = 625
playerX_change = 5  # Constant forward movement speed
playerY_change = 0
is_jumping = False
gravity = 1
jump_strength = -20

# Obstacles
obstacles = []
obstacle_speed = 5
obstacle_timer = 0

# Scrolling background
background_x = 0

# Score (and speedup)
score = 0
speedup = 0
font = pygame.font.Font(None, 36)

# Draws player icon onto screen
def draw_player(x, y):
    screen.blit(player, (x,y))

# Draw obstacles onto screen
def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(screen, (34, 177, 76), obs)  # Green color for obstacles

# Game loop
running = True
while running:
    screen.fill((126, 189, 255))                # sky color
    screen.blit(ground, (background_x, 680))    # ground color

    # Scrolling background effect
    # background_x -= playerX_change
    # if background_x <= -screen_width:
    #     background_x = 0

    # Game Input Handler
    for event in pygame.event.get():
        # exits the game
        if event.type == pygame.QUIT:
            running = False

        # detects if a controller is pluged in
        if event.type == pygame.JOYDEVICEADDED:
            print("Controller connected: " + str(event))
            joy = pygame.joystick.Joystick(event.device_index)

        # Jump! with controller
        if event.type == pygame.JOYBUTTONDOWN:
            if not is_jumping:  # jump with any button
                if event.button == 0 or 1 or 2 or 3:    
                    playerY_change = jump_strength
                    is_jumping = True

        # Jump! with keyboard
        if event.type == pygame.KEYDOWN:    # jump with any space
            if not is_jumping:
                if event.key == pygame.K_UP or pygame.K_SPACE:
                    playerY_change = jump_strength
                    is_jumping = True

    # Changes player position 
    #playerX += playerX_change
    playerY += playerY_change
    playerY_change += gravity

    # Check if player is on the ground
    if playerY >= 625:
        playerY = 625
        playerY_change = 0
        is_jumping = False

    # Spawn obstacles at random intervals
    obstacle_timer += 1
    if obstacle_timer > random.randint(60, 600):  # Spawn at least every 60 frames
        obstacle_x = screen_width
        obstacle_y = 645  # Position on ground level
        obstacles.append(pygame.Rect(obstacle_x, obstacle_y, 20, 40))  # Rectangle obstacles
        obstacle_timer = 0

    # Move obstacles and check for collisions
    for obs in obstacles[:]:
        obs.x -= obstacle_speed
        if obs.colliderect(pygame.Rect(playerX, playerY, 50, 50)):
            running = False  # Game over on collision
        if obs.x < -20:
            obstacles.remove(obs)  # Remove obstacle once it's off-screen

    # Draw objects
    draw_player(playerX, playerY)
    draw_obstacles(obstacles)

    # Update score and display
    score += 1
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    speedup += 1

    # Increase speed at higher scores
    if speedup == 500:
        playerX_change += 5
        obstacle_speed += 5
        speedup = 0

    pygame.display.update()
    # Framerate 60 fps
    clock.tick(60)
        
pygame.quit()              