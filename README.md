# OpenGL CMPSC457 Final Project

## Project Description
An interactive 3D animation system featuring multiple geometric models with texture mapping, lighting effects, and Bezier curve motion paths. 
- Pyramid
- Sphere
- Cube

## Features
- Multiple 3D models 
- Texture mapping and lighting effects
- Interactive camera controls
- Bezier curve animation paths
- Real-time model transformations

## Requirements
- Python
- PyGame
- PyOpenGL
- NumPy


## Controls
- **Arrow Keys**: Rotate scene
- **Z/X**: Zoom in/out
- **Space**: Toggle auto-rotation
- **P**: Toggle path visibility
- **ESC**: Exit program

## Project Structure
```
CMPSC457_Final_Project/
├── py
├── requirement.txt
├── README.md
├── report.md
```

## Feature Implementation

### 1. 3D Models
- Textured cube with checkerboard pattern
- Colored pyramid with solid faces
- Smooth sphere with parametric generation

### 2. Transformations
- Translation along Bezier curves
- Rotation (manual and automatic)
- Scale transformations
- Interactive view control

### 3. Lighting and Materials
- Ambient lighting
- Diffuse lighting components
- Material properties for each model

### 4. Animation
- Bezier curve movement paths
- Smooth rotation animations
- Interactive camera transformations

### 5. Texturing
- Procedural texture generation
- Mapping
- Texture filtering implementation

## Development Notes
- OpenGL -> 3D rendering
- PyGame -> window creation and user input
- NumPy -> mathematical operations support
