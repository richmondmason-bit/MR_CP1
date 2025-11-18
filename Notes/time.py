import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = 10
MAX_FALL_SPEED = 15
PLAYER_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.velocity_y = 0
        self.on_ground = False

    def update(self):
        self.velocity_y += GRAVITY
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED
        self.rect.y += self.velocity_y

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity_y = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:  # Check if the player is on the ground
            self.velocity_y = -JUMP_STRENGTH  # Apply jump strength
            self.on_ground = False  # Set on_ground to False

    def move(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Improved Platformer")
clock = pygame.time.Clock()

# Create player
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-PLAYER_SPEED)
    if keys[pygame.K_RIGHT]:
        player.move(PLAYER_SPEED)

    # Update
    all_sprites.update()

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)