import pygame
import random

# Initialize pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixel Plane Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Frame rate
FPS = 60
clock = pygame.time.Clock()

# Load images
try:
    plane_img = pygame.image.load(r"D:\python games\pixel airplane\a-pixel-art-airplane-flying-in-the-air-free-vector.jpg").convert_alpha()
    plane_img = pygame.transform.scale(plane_img, (50, 50))  # Resize the image to fit the plane
except pygame.error as e:
    print(f"Unable to load image: {e}")
    pygame.quit()
    exit()

enemy_img = pygame.Surface((50, 50))
enemy_img.fill((255, 0, 0))  # Red for the enemy

# Player plane class
class PlayerPlane(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = plane_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        if keys[pygame.K_UP]:
            self.speed_y = -5
        if keys[pygame.K_DOWN]:
            self.speed_y = 5

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Boundary checking
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Enemy plane class
class EnemyPlane(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(2, 6)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(2, 6)

# Initialize sprites
player = PlayerPlane()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

enemy_planes = pygame.sprite.Group()
for i in range(10):
    enemy = EnemyPlane()
    all_sprites.add(enemy)
    enemy_planes.add(enemy)

# Game loop
running = True
while running:
    # Keep loop running at correct speed
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update sprites
    all_sprites.update()

    # Check for collision between player and enemies
    hits = pygame.sprite.spritecollide(player, enemy_planes, False)
    if hits:
        print("Collision! Game Over.")
        running = False

    # Draw/render
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Flip the display
    pygame.display.flip()

# Quit pygame
pygame.quit()