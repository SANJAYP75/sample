import pygame
import pymunk
import pymunk.pygame_util
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 60
GRAVITY = 900
FRICTION = 0.99
HEXAGON_RADIUS = 150
ROTATION_SPEED = 1  # Degrees per frame

# Pygame Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, GRAVITY)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Create a Ball
def create_ball(space, x, y, radius=15, mass=1):
    body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
    body.position = x, y
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 0.9  # Bounciness
    shape.friction = 0.4
    space.add(body, shape)
    return body

# Create Rotating Hexagon
def create_hexagon(space, center_x, center_y, radius):
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = (center_x, center_y)

    angle_step = math.pi / 3  # 60 degrees per side
    vertices = [(math.cos(i * angle_step) * radius, math.sin(i * angle_step) * radius) for i in range(6)]
    shapes = []

    for i in range(6):
        segment = pymunk.Segment(body, vertices[i], vertices[(i + 1) % 6], 3)
        segment.elasticity = 0.9
        segment.friction = 0.5
        space.add(segment)
        shapes.append(segment)

    return body, shapes

# Initialize Ball and Hexagon
ball = create_ball(space, WIDTH // 2, HEIGHT // 4)
hexagon_body, hexagon_sides = create_hexagon(space, WIDTH // 2, HEIGHT // 2, HEXAGON_RADIUS)

running = True
angle = 0  # Rotation Angle

# Game Loop
while running:
    screen.fill(WHITE)

    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rotate Hexagon
    angle += math.radians(ROTATION_SPEED)
    cos_a, sin_a = math.cos(angle), math.sin(angle)

    for i, segment in enumerate(hexagon_sides):
        x1, y1 = segment.a
        x2, y2 = segment.b

        # Rotate around the center
        new_x1 = cos_a * x1 - sin_a * y1
        new_y1 = sin_a * x1 + cos_a * y1
        new_x2 = cos_a * x2 - sin_a * y2
        new_y2 = sin_a * x2 + cos_a * y2

        segment.a = (new_x1, new_y1)
        segment.b = (new_x2, new_y2)

    # Apply friction to ball
    ball.velocity = (ball.velocity[0] * FRICTION, ball.velocity[1] * FRICTION)

    # Update Physics
    space.step(1 / FPS)
    
    # Draw Objects
    space.debug_draw(draw_options)

    # Update Screen
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
