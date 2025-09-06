# DULA-E8: 3D Fluid Dynamics Simulation

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Language](https://img.shields.io/badge/Language-Julia-9558B2.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-brightgreen.svg)

A real-time, interactive 3D Navier-Stokes fluid simulation accelerated with `CUDA.jl`. This project visualizes fluid density fields using a vibrant, professional-style colormap and features an interactive cube obstacle that can be moved within the fluid. The simulation's inflow uses a unique turbulence generation method based on concepts from the E8 exceptional Lie group.

This project is hosted at the [DULA2025/Navier-Stokes](https://github.com/DULA2025/Navier-Stokes) repository.

![Simulation Screenshot](https://raw.githubusercontent.com/DULA2025/Navier-Stokes/main/simulation_screenshot.png)
*(**Note:** This is a placeholder image. You should upload a screenshot of your simulation named `simulation_screenshot.png` to your GitHub repository for it to display here.)*

## Features

-   **Real-time 3D Fluid Simulation:** Solves the Navier-Stokes equations on a 3D grid.
-   **GPU Acceleration:** All heavy computation is performed on an NVIDIA GPU using `CUDA.jl`.
-   **Interactive Obstacle:** A cube obstacle can be moved with the mouse or keyboard, allowing real-time interaction with the fluid flow.
-   **Vibrant Visualization:** Uses a multi-color, transparent colormap to visualize fluid density, inspired by professional computational fluid dynamics (CFD) software.
-   **E8-Based Inflow:** Generates complex inflow conditions using mathematical concepts from the E8 lattice.
-   **Cross-platform (Windows & Linux).**

## Prerequisites

Before you begin, ensure you have the following installed:

1.  **An NVIDIA GPU:** A CUDA-compatible graphics card is required.
2.  **NVIDIA CUDA Drivers:** Make sure you have the latest drivers for your GPU installed.
3.  **Julia:** This project is built on Julia (version 1.7 or newer). You can download it from the [official Julia website](https://julialang.org/downloads/). We recommend installing `juliaup` for easy version management.

## Installation

### 1. Download and Unzip the Project

First, download the project files.

* **Go to this URL:** [**E8_3D_SIM.zip Download Link**](https://github.com/DULA2025/Navier-Stokes/raw/main/E8_3D_SIM.zip)
* Your browser will download the `E8_3D_SIM.zip` file.

Next, unzip the file.

* **On Windows:** Find the downloaded `.zip` file, right-click it, and select **"Extract All..."**. Choose a location for the project folder.
* **On Linux:** Open a terminal, navigate to your Downloads folder, and run:
    ```bash
    unzip E8_3D_SIM.zip
    ```

This will create a folder containing all the necessary simulation files (`main_3d.jl`, `install.jl`, etc.).

### 2. Install Dependencies

Navigate into the newly created project folder using your terminal or PowerShell.

**On Windows (using PowerShell):**
```powershell
# Navigate into the unzipped project folder
cd C:\Path\To\Your\E8_3D_SIM

# Run the installation script
julia install.jl
```

**On Linux (using Terminal):**
```bash
# Navigate into the unzipped project folder
cd /path/to/your/E8_3D_SIM

# Run the installation script
julia install.jl
```

This script will activate the local project environment and install all required Julia packages.

## Running the Simulation

Once the installation is complete, you can run the simulation using the following command from inside the project's folder:

```bash
julia --project=. main_3d.jl
```

The `--project=.` flag tells Julia to use the packages defined in the local `Project.toml` file. A window should appear showing the fluid simulation.

## Controls

-   **Mouse (Left-click + Drag):** Move the cube obstacle in the horizontal (XY) plane.
-   **Keyboard (W, A, S, D):** Move the cube obstacle up, left, down, and right.
-   **Keyboard (ESC):** Close the simulation window.

## Configuration

You can easily tweak the simulation by editing `main_3d.jl`:

-   **Simulation Speed:** In the `FluidSim3D` constructor, change the multiplier in `sim_dt = 0.016 * 32.0` to adjust the speed. Higher values are faster but may become unstable.
-   **Grid Size:** In the `main()` function, change the arguments to `DULA_E8.FluidSim3D(64, 64, 64)`.
-   **Obstacle Position & Size:** In the `FluidSim3D` constructor, modify the `obstacle_pos` and `obstacle_radius` variables.

## License

This project is distributed under the MIT License. See the `LICENSE` file for more information.
