import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

vertices = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
)

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
)

colors = (
    (0.8,0,0),    # Red
    (0,0.8,0),    # Green
    (0,0,0.8),    # Blue
    (0.8,0.8,0),  # Yellow
    (0.8,0,0.8),  # Purple
    (0,0.8,0.8)   # Cyan
)

normals = (
    (0,0,-1),  # Back
    (-1,0,0),  # Left
    (0,0,1),   # Front
    (1,0,0),   # Right
    (0,1,0),   # Top
    (0,-1,0)   # Bottom
)

def init_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glLight(GL_LIGHT0, GL_POSITION, (5, 5, 5, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))



def draw_cube():
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        glNormal3fv(normals[i])
        glColor3fv(colors[i])
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glDisable(GL_LIGHTING)
    glColor3f(0, 0, 0)  # Black edges
    glBegin(GL_LINES)
    for surface in surfaces:
        for i in range(4):
            glVertex3fv(vertices[surface[i]])
            glVertex3fv(vertices[surface[(i+1)%4]])
    glEnd()
    glEnable(GL_LIGHTING)

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    glEnable(GL_DEPTH_TEST)
    init_lighting()

    # Set white background
    glClearColor(1.0, 1.0, 1.0, 1.0)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

    control_points = [
        [-4, -2, 0],
        [-2, 2, 0],
        [2, 2, 0],
        [4, -2, 0]
    ]

    rot_x = 0
    rot_y = 0
    zoom = 0
    auto_rotate = False
    show_path = True
    movement_time = 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_LEFT:
                    rot_y -= 5
                if event.key == pygame.K_RIGHT:
                    rot_y += 5
                if event.key == pygame.K_UP:
                    rot_x -= 5
                if event.key == pygame.K_DOWN:
                    rot_x += 5
                if event.key == pygame.K_SPACE:
                    auto_rotate = not auto_rotate
                if event.key == pygame.K_p:
                    show_path = not show_path
                if event.key == pygame.K_z:
                    zoom += 1
                if event.key == pygame.K_x:
                    zoom -= 1

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # Apply zoom
        glTranslatef(0, 0, zoom * 0.1)
        
        if show_path:
            draw_bezier_curve(control_points)

        movement_time += 0.01
        t = (math.sin(movement_time) + 1) / 2
        position = calculate_bezier_point(t, control_points)

        glPushMatrix()
        glTranslatef(position[0], position[1], position[2])
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)
        
        if auto_rotate:
            rot_y += 1

        draw_cube()
        glPopMatrix()

        # Reset zoom effect for next frame
        glTranslatef(0, 0, -zoom * 0.1)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()