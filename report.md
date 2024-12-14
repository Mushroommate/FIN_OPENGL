# CMPSC 457 Final Project Report

## Project Information
- **Title**: Interactive 3D Animation System
- **Course**: CMPSC 457 - Computer Graphics
- **Semester**: Fall 2024


## Project Description
This project implements an interactive 3D graphics system that demonstrates fundamental computer graphics concepts using OpenGL. The system features multiple 3D models, texture mapping, lighting effects, and parametric motion paths.

## Technical Implementation and Proof

### 1. 2D/3D Modeling 
#### Implementation Details:
```python
# 1. Cube Definition
vertices = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
)
surfaces = (
    (0,1,2,3), (3,2,7,6), (6,7,5,4),
    (4,5,1,0), (1,5,7,2), (4,0,3,6)
)

# 2. Sphere Generation
def create_sphere(radius, segments):
    vertices = []
    for i in range(segments + 1):
        lat = math.pi * (-0.5 + float(i) / segments)
        for j in range(segments + 1):
            lon = 2 * math.pi * float(j) / segments
            x = math.cos(lat) * math.cos(lon)
            y = math.sin(lat)
            z = math.cos(lat) * math.sin(lon)
            vertices.append((x * radius, y * radius, z * radius))
    return vertices

# 3. Pyramid Construction
pyramid_vertices = (
    (0, 1, 0),    # top
    (-1, -1, 1),  # front left
    (1, -1, 1),   # front right
    (1, -1, -1),  # back right
    (-1, -1, -1)  # back left
)
```

### 2. Transformations and Color Models
#### Matrix Transformations:
```python
def apply_transformations():
    # Model transformations
    glTranslatef(*position)            # Translation
    glRotatef(rot_x, 1, 0, 0)         # X-axis rotation
    glRotatef(rot_y, 0, 1, 0)         # Y-axis rotation
    glScalef(scale_x, scale_y, scale_z)# Scaling

# Color implementation
colors = [
    (1,0,0),    # Red - diffuse reflection
    (0,1,0),    # Green - specular highlight
    (0,0,1),    # Blue - ambient light
]
```

### 3. Projections and Clipping 
#### Projection Setup:
```python
def setup_projection():
    # Perspective projection matrix
    gluPerspective(45,                    # Field of View
                  (display[0]/display[1]), # Aspect Ratio
                  0.1,                    # Near clipping plane
                  50.0)                   # Far clipping plane
    
    # View matrix
    glTranslatef(0.0, 0.0, -20)          # Camera position

# Enable depth testing for proper 3D rendering
glEnable(GL_DEPTH_TEST)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
```

### 4. Shader and Texture 
#### Texture Generation and Mapping:
```python
def create_texture():
    textureSurface = pygame.Surface((256, 256))
    for y in range(32):
        for x in range(32):
            if (x + y) % 2 == 0:
                # Create checkerboard pattern
                pygame.draw.rect(textureSurface, 
                               (200, 200, 200),
                               (x*8, y*8, 8, 8))

def apply_texture():
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textureId)
    # Texture coordinates for proper mapping
    texcoords = ((0,0), (1,0), (1,1), (0,1))
    for vertex, texcoord in zip(surface, texcoords):
        glTexCoord2fv(texcoord)
        glVertex3fv(vertices[vertex])
```

### 5. Lighting Implementation 
#### Lighting System:
```python
def init_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    
    # Light position and properties
    glLight(GL_LIGHT0, GL_POSITION, (5, 5, 5, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    
    # Material properties
    glMaterialfv(GL_FRONT, GL_SPECULAR, (1, 1, 1, 1))
    glMaterialf(GL_FRONT, GL_SHININESS, 50)
```

### 6. Parametric Curves/Surfaces 
#### Bezier Curve Implementation:
```python
def calculate_bezier_point(t, control_points):
    n = len(control_points) - 1
    point = [0, 0, 0]
    for i in range(n + 1):
        # Bernstein polynomial calculation
        binomial = math.comb(n, i)
        t_power = t ** i
        one_minus_t_power = (1 - t) ** (n - i)
        
        # Point calculation using Bezier formula
        for j in range(3):
            point[j] += binomial * one_minus_t_power * t_power * 
                       control_points[i][j]
    return point

# Control points for motion paths
control_points = [
    [-4, -2, 0],  # Start point
    [-2, 2, 0],   # Control point 1
    [2, 2, 0],    # Control point 2
    [4, -2, 0]    # End point
]
```

### Interactive 
#### User Controls:
```python
def handle_input(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            rot_y -= 5              # Rotate left
        elif event.key == pygame.K_RIGHT:
            rot_y += 5              # Rotate right
        elif event.key == pygame.K_SPACE:
            auto_rotate = not auto_rotate  # Toggle rotation
        elif event.key == pygame.K_z:
            camera_distance -= 1    # Zoom in
        elif event.key == pygame.K_x:
            camera_distance += 1    # Zoom out
```

### Animation System
```python
def update_animation():
    # Update time parameter
    movement_time += 0.01
    t = (math.sin(movement_time) + 1) / 2
    
    # Calculate new position
    position = calculate_bezier_point(t, control_points)
    
    # Apply rotation
    if auto_rotate:
        rot_y += 1
```



## Challenges

1. **Challenge**: Complex 3D Model Coordination
   **Solution**:
   ```python
   # Implemented model management system
   class Model:
       def __init__(self, vertices, surfaces):
           self.vertices = vertices
           self.surfaces = surfaces
           self.position = [0, 0, 0]
           self.rotation = [0, 0, 0]
   ```

2. **Challenge**: Smooth Animation Paths
   **Solution**:
   ```python
   # Implemented interpolation system
   def interpolate_position(start, end, t):
       return [start[i] + (end[i] - start[i]) * t 
               for i in range(3)]
   ```

3. **Challenge**: Texture Coordination
   **Solution**:
   ```python
   # Implemented proper texture coordinate management
   def calculate_texture_coordinates(vertex):
       u = (vertex[0] + 1) * 0.5
       v = (vertex[1] + 1) * 0.5
       return (u, v)
   ```

## What could be improved 
1. Shadow mapping implementation
2. More complex texture patterns
3. Physics-based animations
4. Particle effects
5. Advanced camera controls

