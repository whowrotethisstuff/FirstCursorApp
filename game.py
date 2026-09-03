import math
import pygame
import sys

# Window
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
SKY = (135, 206, 235)
PACMAN_YELLOW = (255, 221, 0)
PACMAN_EYE = (30, 30, 30)
PLATFORM_COLOR = (76, 153, 76)
GROUND_COLOR = (101, 67, 33)

# Physics
GRAVITY = 0.6
JUMP_STRENGTH = -14
MOVE_SPEED = 6


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing = 1
        self.mouth_phase = 0.0

    def handle_input(self, keys):
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -MOVE_SPEED
            self.facing = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = MOVE_SPEED
            self.facing = 1
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += GRAVITY
        if self.vel_y > 20:
            self.vel_y = 20

    def move(self, platforms):
        self.rect.x += self.vel_x
        self._resolve_horizontal(platforms)

        self.rect.y += int(self.vel_y)
        self.on_ground = False
        self._resolve_vertical(platforms)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def _resolve_horizontal(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_x > 0:
                    self.rect.right = platform.left
                elif self.vel_x < 0:
                    self.rect.left = platform.right

    def _resolve_vertical(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.bottom
                    self.vel_y = 0

    def draw(self, screen):
        if self.vel_x != 0:
            self.mouth_phase += 0.28
        mouth_deg = 8 + abs(math.sin(self.mouth_phase)) * 32

        cx, cy = self.rect.centerx, self.rect.centery
        radius = self.rect.width // 2
        facing_deg = 0 if self.facing > 0 else 180

        points = [(cx, cy)]
        start_deg = facing_deg + mouth_deg
        sweep = 360 - 2 * mouth_deg
        steps = 28
        for i in range(steps + 1):
            rad = math.radians(start_deg + sweep * i / steps)
            points.append((cx + radius * math.cos(rad), cy + radius * math.sin(rad)))

        pygame.draw.polygon(screen, PACMAN_YELLOW, points)

        eye_x = cx + int(4 * self.facing)
        eye_y = cy - 10
        pygame.draw.circle(screen, PACMAN_EYE, (eye_x, eye_y), 4)


def create_platforms():
    return [
        pygame.Rect(0, HEIGHT - 40, WIDTH, 40),           # ground
        pygame.Rect(150, 480, 200, 20),
        pygame.Rect(450, 400, 180, 20),
        pygame.Rect(80, 320, 160, 20),
        pygame.Rect(350, 260, 200, 20),
        pygame.Rect(600, 320, 150, 20),
        pygame.Rect(250, 180, 140, 20),
        pygame.Rect(500, 140, 180, 20),
    ]


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man Platformer")
    clock = pygame.time.Clock()

    platforms = create_platforms()
    player = Player(100, HEIGHT - 120)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.apply_gravity()
        player.move(platforms)

        screen.fill(SKY)
        for platform in platforms:
            color = GROUND_COLOR if platform.y >= HEIGHT - 40 else PLATFORM_COLOR
            pygame.draw.rect(screen, color, platform)

        player.draw(screen)

        font = pygame.font.SysFont(None, 24)
        hint = font.render("Arrow keys / WASD to move, Space to jump", True, (30, 30, 30))
        screen.blit(hint, (20, 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
