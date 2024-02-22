import pygame
import sys
import math
from pygame.locals import *

# Initialize Pygame
pygame.init()
# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Cube vertices
vertices = [
    [-1, -1, -1],
    [-1, 1, -1],
    [1, 1, -1],
    [1, -1, -1],
    [-1, -1, 1],
    [-1, 1, 1],
    [1, 1, 1],
    [1, -1, 1]
]

# Cube edges (connecting vertices)
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Cube faces (connecting vertices)
faces = [
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (0, 1, 5, 4),
    (2, 3, 7, 6),
    (0, 3, 7, 4),
    (1, 2, 6, 5)
]

# Light sources
light_sources = [
    (1, 0, 0),  # Red light
    (0, 1, 0),  # Green light
    (0, 0, 1)   # Blue light
]

# Projection matrix
projection_matrix = [
    [1, 0, 0],
    [0, 1, 0]
]

# Rotate a point around the origin
def rotate_point(point, angle_x, angle_y, angle_z):
    x, y, z = point

    # Rotation around X-axis
    new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
    new_z = y * math.sin(angle_x) + z * math.cos(angle_x)
    y, z = new_y, new_z

    # Rotation around Y-axis
    new_x = x * math.cos(angle_y) + z * math.sin(angle_y)
    new_z = -x * math.sin(angle_y) + z * math.cos(angle_y)
    x, z = new_x, new_z

    # Rotation around Z-axis
    new_x = x * math.cos(angle_z) - y * math.sin(angle_z)
    new_y = x * math.sin(angle_z) + y * math.cos(angle_z)
    x, y = new_x, new_y

    return x, y, z

# Project a 3D point onto a 2D screen
def project_point(point):
    x, y, z = point
    return x * WIDTH / (z + 4) + WIDTH / 2, y * HEIGHT / (z + 4) + HEIGHT / 2

# Draw the cube
def draw_cube(screen, angle_x, angle_y, angle_z):
    screen.fill(BLACK)

    rotated_vertices = [rotate_point(v, angle_x, angle_y, angle_z) for v in vertices]

    for face in faces:
        # Calculate the normal vector for each face
        normal = [0, 0, 0]
        for v in face:
            normal[0] += rotated_vertices[v][0]
            normal[1] += rotated_vertices[v][1]
            normal[2] += rotated_vertices[v][2]
        normal = [n / len(face) for n in normal]

        # Calculate the intensity based on the dot product with each light source
        intensity = [0, 0, 0]
        for i, light in enumerate(light_sources):
            dot_product = sum(a * b for a, b in zip(normal, light))
            intensity[i] = max(dot_product, 0)

        # Draw the face with the corresponding intensity
        color = (
            int(RED[0] * intensity[0]),
            int(GREEN[1] * intensity[1]),
            int(BLUE[2] * intensity[2])
        )

        projected_face = [project_point(rotated_vertices[v]) for v in face]
        pygame.draw.polygon(screen, color, projected_face)

    for edge in edges:
        start = project_point(rotated_vertices[edge[0]])
        end = project_point(rotated_vertices[edge[1]])
        pygame.draw.line(screen, WHITE, start, end, 1)

    pygame.display.flip()

# Main loop
def main():
    clock = pygame.time.Clock()
    angle_x, angle_y, angle_z = 0, 0, 0

    # Set up Pygame window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rotating Cube with Light Sources")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        draw_cube(screen, angle_x, angle_y, angle_z)
        angle_x += 0.01
        angle_y += 0.02
        angle_z += 0.03

        clock.tick(FPS)

if __name__ == "__main__":
    main()
