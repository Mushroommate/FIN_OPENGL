import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np






# Cube vertices
cube_vertices = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
)

# Pyramid vertices
pyramid_vertices = (
    (0, 1, 0),    # top
    (-1, -1, 1),  # front left
    (1, -1, 1),   # front right
    (1, -1, -1),  # back right
    (-1, -1, -1)  # back left
)

# Cube surfaces with texture coordinates
cube_surfaces = (
    (0,1,2,3), (3,2,7,6), (6,7,5,4),
    (4,5,1,0), (1,5,7,2), (4,0,3,6)
)

# Texture coordinates for cube
cube_texcoords = ((0,0), (1,0), (1,1), (0,1))

# Pyramid surfaces
pyramid_surfaces = (
    (0,1,2), # front
    (0,2,3), # right
    (0,3,4), # back
    (0,4,1), # left
    (1,2,3,4) # bottom
)

colors = [
    (1,0,0), (0,1,0), (0,0,1),
    (1,1,0), (1,0,1), (0,1,1)
]

def create_texture():
    # Create a simple checkerboard pattern
    textureSurface = pygame.Surface((256, 256))
    textureSurface.fill((255, 255, 255))
    for y in range(32):
        for x in range(32):
            if (x + y) % 2 == 0:
                pygame.draw.rect(textureSurface, (200, 200, 200), 
                               (x*8, y*8, 8, 8))
    
    # Convert the surface to a string buffer
    textureData = pygame.image.tostring(textureSurface, 'RGB', 1)
    
    # Generate a texture ID
    textureId = glGenTextures(1)
    
    # Bind and set up texture
    glBindTexture(GL_TEXTURE_2D, textureId)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, 256, 256, 0, GL_RGB, 
                 GL_UNSIGNED_BYTE, textureData)
    
    return textureId

def create_sphere(radius, segments):
    vertices = []
    indices = []
    
    for i in range(segments + 1):
        lat = math.pi * (-0.5 + float(i) / segments)
        for j in range(segments + 1):
            lon = 2 * math.pi * float(j) / segments
            x = math.cos(lat) * math.cos(lon)
            y = math.sin(lat)
            z = math.cos(lat) * math.sin(lon)
            vertices.append((x * radius, y * radius, z * radius))
            
    for i in range(segments):
        for j in range(segments):
            first = (i * (segments + 1)) + j
            second = first + segments + 1
            indices.append((first, second, first + 1))
            indices.append((second, second + 1, first + 1))
            
    return vertices, indices

def draw_textured_cube():
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    for i, surface in enumerate(cube_surfaces):
        for vertex, texcoord in zip(surface, cube_texcoords):
            glTexCoord2fv(texcoord)
            glVertex3fv(cube_vertices[vertex])
    glEnd()
    glDisable(GL_TEXTURE_2D)

    # Draw edges in black
    glColor3f(0, 0, 0)
    glBegin(GL_LINES)
    for surface in cube_surfaces:
        for i in range(4):
            glVertex3fv(cube_vertices[surface[i]])
            glVertex3fv(cube_vertices[surface[(i+1)%4]])
    glEnd()

def draw_pyramid():
    glBegin(GL_TRIANGLES)
    for i, surface in enumerate(pyramid_surfaces[:4]):  # Side faces
        glColor3fv(colors[i])
        for vertex in surface:
            glVertex3fv(pyramid_vertices[vertex])
    glEnd()
    
    # Draw base separately as it's a quad
    glBegin(GL_QUADS)
    glColor3fv(colors[4])
    for vertex in pyramid_surfaces[4]:
        glVertex3fv(pyramid_vertices[vertex])
    glEnd()

def draw_sphere(radius=1, segments=20):
    vertices, indices = create_sphere(radius, segments)
    glColor3f(0.7, 0.7, 1.0)  # Light blue color
    glBegin(GL_TRIANGLES)
    for triangle in indices:
        for vertex_id in triangle:
            vertex = vertices[vertex_id]
            glNormal3fv(vertex)
            glVertex3fv(vertex)
    glEnd()

def init_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    glLight(GL_LIGHT0, GL_POSITION, (5, 5, 5, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))

def calculate_bezier_point(t, control_points):
    n = len(control_points) - 1
    point = [0, 0, 0]
    for i in range(n + 1):
        binomial = math.comb(n, i)
        t_power = t ** i
        one_minus_t_power = (1 - t) ** (n - i)
        for j in range(3):
            point[j] += binomial * one_minus_t_power * t_power * control_points[i][j]
    return point

def draw_bezier_curve(control_points):
    glDisable(GL_LIGHTING)
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINE_STRIP)
    for i in range(101):
        t = i / 100
        point = calculate_bezier_point(t, control_points)
        glVertex3fv(point)
    glEnd()
    glEnable(GL_LIGHTING)

def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    glEnable(GL_DEPTH_TEST)
    init_lighting()
    
    # Create and bind texture
    texture = create_texture()
    
    # Set white background
    glClearColor(1.0, 1.0, 1.0, 1.0)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -20)

    cube_control_points = [
        [-4, -2, 0], [-2, 2, 0], [2, 2, 0], [4, -2, 0]
    ]
    pyramid_control_points = [
        [-4, 2, -2], [-2, -2, -2], [2, -2, -2], [4, 2, -2]
    ]
    sphere_control_points = [
        [-4, 0, 2], [-2, 0, -2], [2, 0, -2], [4, 0, 2]
    ]

    rot_x = 0
    rot_y = 0
    zoom = 0
    auto_rotate = False
    show_path = True
    movement_time = 0

    clock = pygame.time.Clock()
    
    print("\nControls:")
    print("Arrow keys: Rotate scene")
    print("Z/X: Zoom in/out")
    print("SPACE: Toggle auto-rotation")
    print("P: Toggle paths visibility")
    print("ESC: Quit\n")

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

        glTranslatef(0, 0, zoom * 0.1)
        
        glPushMatrix()
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)

        if auto_rotate:
            rot_y += 0.5

        if show_path:
            draw_bezier_curve(cube_control_points)
            draw_bezier_curve(pyramid_control_points)
            draw_bezier_curve(sphere_control_points)

        movement_time += 0.01
        t = (math.sin(movement_time) + 1) / 2

        # Draw textured cube
        glColor3f(1, 1, 1)  # Reset color to white for proper texture
        cube_pos = calculate_bezier_point(t, cube_control_points)
        glPushMatrix()
        glTranslatef(*cube_pos)
        glRotatef(movement_time * 30, 1, 1, 0)
        draw_textured_cube()
        glPopMatrix()

        # Draw pyramid
        pyramid_pos = calculate_bezier_point(t, pyramid_control_points)
        glPushMatrix()
        glTranslatef(*pyramid_pos)
        glRotatef(movement_time * 30, 0, 1, 1)
        glScalef(0.8, 0.8, 0.8)
        draw_pyramid()
        glPopMatrix()

        # Draw sphere
        sphere_pos = calculate_bezier_point(t, sphere_control_points)
        glPushMatrix()
        glTranslatef(*sphere_pos)
        glRotatef(movement_time * 30, 1, 0, 1)
        draw_sphere(0.8, 16)
        glPopMatrix()

        glPopMatrix()
        glTranslatef(0, 0, -zoom * 0.1)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()