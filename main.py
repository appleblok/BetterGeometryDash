import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_LENGTH = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))
pygame.display.set_caption("Better Geometry Dash")

player = pygame.Rect(50, 500, 50, 50)
velocity_y = 0

platforms = [
    pygame.Rect(-2000, 550, 20000, 50),
    pygame.Rect(200, 450, 150, 20),
    pygame.Rect(400, 350, 150, 20),
    pygame.Rect(600, 250, 150, 20),
    pygame.Rect(400, 145, 150, 20),
    pygame.Rect(100, 145, 150, 20)
]

finish = pygame.Rect(700, 200, 50, 50)

player_speed = 5
gravity = 1
jump_strength = -20

last_dash_time = 0
dash_cooldown = 1000
dash_duration = 200
is_dashing = False
dash_end_time = 0
dash_distance = 90
dash_progress = 0
dash_direction = None

run = True

while run:
    pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()

    velocity_y += gravity
    player.y += velocity_y

    on_ground = False

    for platform in platforms:
        if player.colliderect(platform) and velocity_y > 0:
            player.y = platform.y - player.height
            velocity_y = 0
            on_ground = True
        elif player.colliderect(platform) and velocity_y < 0:
            player.y = platform.y + platform.height
            velocity_y = 0

    if key[pygame.K_RIGHT]:
        player.x += player_speed
    elif key[pygame.K_LEFT]:
        player.x -= player_speed

    if key[pygame.K_UP] and on_ground:
        velocity_y = jump_strength

    for platform in platforms:
        if player.colliderect(platform):
            if key[pygame.K_RIGHT] and player.right > platform.left:
                player.right = platform.left
            elif key[pygame.K_LEFT] and player.left < platform.right:
                player.left = platform.right

    current_time = pygame.time.get_ticks()

    if key[pygame.K_c] and current_time - last_dash_time > dash_cooldown and not is_dashing:
        last_dash_time = current_time
        dash_end_time = current_time + dash_duration
        is_dashing = True
        dash_progress = 0
        dash_direction = 'right' if key[pygame.K_RIGHT] else 'left'

    if is_dashing:
        if dash_direction == 'right' and key[pygame.K_RIGHT]:
            dash_speed = dash_distance / dash_duration * 30
            dash_progress += dash_speed
            player.x += dash_speed
            velocity_y = -0.2
        elif dash_direction == 'left' and key[pygame.K_LEFT]:
            dash_speed = dash_distance / dash_duration * 30
            dash_progress -= dash_speed
            player.x -= dash_speed
            velocity_y = -0.2

        if abs(dash_progress) >= dash_distance or current_time >= dash_end_time:
            is_dashing = False
            dash_direction = None

    player_color = (0, 255, 0) if not is_dashing else (255, 255, 0)

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, player_color, player)
    for platform in platforms:
        pygame.draw.rect(screen, (255, 0, 100), platform)

    # pygame.draw.rect(screen, (255, 255, 0), finish)

    pygame.display.update()

pygame.quit()
