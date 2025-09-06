# DULA-E8: 3D Fluid Dynamics Simulation

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Language](https://img.shields.io/badge/Language-Julia-9558B2.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-brightgreen.svg)

A real-time, interactive 3D Navier-Stokes fluid simulation accelerated with `CUDA.jl`. This project visualizes fluid density fields using a vibrant, professional-style colormap and features an interactive cube obstacle that can be moved within the fluid. The simulation's inflow uses a unique turbulence generation method based on concepts from the E8 exceptional Lie group.

![Simulation Screenshot](https://i.imgur.com/your-screenshot-url.png)
*(**Note:** Replace the link above with a URL to your own screenshot or GIF of the simulation running! I recommend using [ScreenToGif](https://www.screentogif.com/) to capture a cool animation.)*

## Features

-   **Real-time 3D Fluid Simulation:** Solves the Navier-Stokes equations on a 3D grid.
-   **GPU Acceleration:** All heavy computation is performed on an NVIDIA GPU using `CUDA.jl`.
-   **Interactive Obstacle:** A cube obstacle can be moved with the mouse or keyboard, allowing real-time interaction with the fluid flow.
-   **Vibrant Visualization:** Uses a multi-color, transparent colormap to visualize fluid density, inspired by professional computational fluid dynamics (CFD) software.
-   **E8-Based Inflow:** Generates complex inflow conditions using mathematical concepts from the E8 lattice.
-   **Configurable:** Easily change simulation speed, grid size, and obstacle properties directly in the code.

## Prerequisites

Before you begin, ensure you have the following installed:

1.  **An NVIDIA GPU:** A CUDA-compatible graphics card is required.
2.  **NVIDIA CUDA Drivers:** Make sure you have the latest drivers for your GPU installed.
3.  **Julia:** This project is built on Julia (version 1.7 or newer). You can download it from the [official Julia website](https://julialang.org/downloads/). We recommend installing `juliaup` for easy version management.
4.  **Git:** Required for cloning the repository. [Download Git](https://git-scm.com/downloads).

## Installation

### 1. Clone the Repository

Open a terminal or PowerShell and clone this repository to your local machine.

```bash
git clone https://github.com/DULA2025/Navier-Stokes/
cd your-repository-name
```

### 2. Install Dependencies

The project includes an `install.jl` script to set up the environment and install all required packages.

**On Windows (using PowerShell):**

```powershell
# Navigate to the project directory
cd C:\Path\To\Your\Project

# Run the installation script
julia install.jl
```

**On Linux (using Terminal):**

```bash
# Navigate to the project directory
cd /path/to/your/project

# Run the installation script
julia install.jl
```

This script will activate the local project environment defined by `Project.toml` and install `GLMakie`, `CUDA`, `StaticArrays`, and other dependencies.

## Running the Simulation

Once the installation is complete, you can run the simulation using the following command from the project's root directory:

```bash
julia --project=. main_3d.jl
```

The `--project=.` flag tells Julia to use the packages defined in the local `Project.toml` file. A window should appear showing the fluid simulation.

## Controls

-   **Mouse (Left-click + Drag):** Move the cube obstacle in the horizontal (XY) plane.
-   **Keyboard (W, A, S, D):** Move the cube obstacle up, left, down, and right.
-   **Keyboard (ESC):** Close the simulation window.

## Configuration

You can easily tweak the simulation by editing the `main()` function or the `FluidSim3D` constructor in `main_3d.jl`:

-   **Simulation Speed:** In the `FluidSim3D` constructor, change the multiplier in `sim_dt = 0.016 * 32.0` to adjust the speed. Higher values are faster but may become unstable.
-   **Grid Size:** In the `main()` function, change the arguments to `DULA_E8.FluidSim3D(64, 64, 64)` to alter the simulation resolution.
-   **Obstacle Position & Size:** In the `FluidSim3D` constructor, modify the `obstacle_pos` and `obstacle_radius` variables.

## License

This project is distributed under the MIT License. See the `LICENSE` file for more information.
