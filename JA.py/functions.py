import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.5
JUMP_STRENGTH = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 500, 50, 50)
        self.velocity_y = 0
        self.on_ground = False

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.on_ground = True
            self.velocity_y = 0

    def jump(self):
        if self.on_ground:
            self.velocity_y = -JUMP_STRENGTH
            self.on_ground = False

# Main game function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simple Platformer")
    clock = pygame.time.Clock()
    player = Player()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        player.update()

        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, player.rect)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()