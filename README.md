# PyBox - 3D Python Sandbox

![1000169146](https://github.com/user-attachments/assets/2d8a571a-6bde-4fdd-a7e9-5ee68cdec4fd)

A minimalist 3D graphics sandbox created with Python and Pygame. Currently features only one animation with ambient background music.

## Features

- Animated 3D bodies showcasing the power of OpenGL
- Smooth rotation on multiple axes
- Background music
- Clean minimal interface
- Easy-to-use controls

## Controls

- Click on the desired animation button to show the simulation.
- Press `ESC` to:
  - Return to main menu (when viewing animation)
  - Exit application (when in main menu)

## Requirements

```python
pygame
numpy
```

## Installation

1. Clone this repository
2. Install dependencies:
```sh
pip install pygame numpy
```

 in the project directory
3. Run the application:
```sh
python main.py
```

## Coming Soon

- Additional 3D shapes and even more animations
- More interactive features
- Extended configuration options
- Advanced and higher resolution rendering capabilities

## Technical Details

The project uses:
- Pygame / OpenGL (modernGL) for rendering and window management
- NumPy for 3D matrix transformations
- HSV color space for rainbow effects
- Custom button and text rendering systems

## License

This project is licensed under the GPL v3.0 License. Additional assets are property of their respective creators and shouldn't be copied without authorization from them.
