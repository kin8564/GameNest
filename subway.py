import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (135, 206, 235)  # Sky blue
PLAYER_SPEED = 5
OBSTACLE_SPEED = 8

# Set up display and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Subway Surfers Clone")
clock = pygame.time.Clock()

# Define Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))  # Red color for visibility
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        self.jump = False
        self.jump_speed = 10
        self.gravity = 0.5
        self.vel_y = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.jump:
            self.jump = True
            self.vel_y = -self.jump_speed

        if self.jump:
            self.vel_y += self.gravity
            self.rect.y += self.vel_y
            if self.rect.y >= SCREEN_HEIGHT // 2:
                self.rect.y = SCREEN_HEIGHT // 2
                self.jump = False
                self.vel_y = 0

# Define Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))  # Blue color for visibility
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT // 2

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.x < -50:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = SCREEN_HEIGHT // 2  # Reset position

# Initialize player and obstacles
player = Player()
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

all_sprites.add(player)
for _ in range(3):  # Create multiple obstacles
    obstacle = Obstacle()
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

# Background scrolling
bg_x = 0
bg_speed = 5

def scroll_background():
    global bg_x
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, (34, 139, 34), (0, SCREEN_HEIGHT // 2 + 50, SCREEN_WIDTH, SCREEN_HEIGHT // 2))  # ground
    pygame.draw.rect(screen, (139, 69, 19), (0, SCREEN_HEIGHT // 2 + 80, SCREEN_WIDTH, SCREEN_HEIGHT // 2 - 80))  # darker ground
    bg_x -= bg_speed
    if bg_x <= -SCREEN_WIDTH:
        bg_x = 0

# Scoring
score = 0
font = pygame.font.Font(None, 36)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update sprites
    all_sprites.update()

    # Collision detection
    if pygame.sprite.spritecollide(player, obstacles, False):
        print("Game Over")
        running = False

    # Scrolling background
    scroll_background()

    # Update score and difficulty
    score += 1
    if score % 100 == 0:
        OBSTACLE_SPEED += 1  # Increase obstacle speed every 100 points

    # Draw all sprites
    all_sprites.draw(screen)

    # Display score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)  # 30 FPS

pygame.quit()
