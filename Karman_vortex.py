import numpy as np
import torch
import pygame
from pygame import surfarray

# Set device for GPU acceleration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")  # For debugging

# E8 and primes part from original (kept on CPU as it's small and one-time)
def chi(n):
    if n % 2 == 0 or n % 3 == 0:
        return 0
    if n % 6 == 1:
        return 1
    if n % 6 == 5:
        return -1

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def e8_root(p, chi_p):
    if chi_p == 0:
        return np.zeros(8)
    scale = np.log(p) / np.sqrt(2)
    np.random.seed(p)
    v_p = np.random.random(8)
    v_p /= np.linalg.norm(v_p)
    return chi_p * scale * v_p

def weyl_reflection(v, plane_normal):
    plane_normal = plane_normal / np.linalg.norm(plane_normal)
    return v - 2 * np.dot(v, plane_normal) * plane_normal

# E8 Parameters
N_primes = 1000
initial_primes = [p for p in range(2, N_primes+1) if is_prime(p)]
plane_normal = np.array([1.0, 0, 0, 0, 0, 0, 0, 0])
reflected_vectors = []
for p in initial_primes:
    chi_p = chi(p)
    v_p_ref = e8_root(p, chi_p) if chi_p != 0 else np.zeros(8)
    v_p_ref = weyl_reflection(v_p_ref, plane_normal)
    reflected_vectors.append((p, v_p_ref))

# Fluid sim constants (Stable Fluids for Karman vortex, higher res)
width, height = 512, 256  # Doubled for better graphics
scale = 1  # Adjusted scale for window size
dt = 0.1
diff = 0.0001
visc = 0.00005  # Low visc for vortices
force_scale = 0.005  # E8 modulation strength
iterations = 10  # Kept for accuracy, but GPU handles it fast

# Fluid arrays on GPU
dens = torch.zeros((height, width), device=device)
dens_prev = torch.zeros((height, width), device=device)
u = torch.zeros((height, width), device=device)
v = torch.zeros((height, width), device=device)
u_prev = torch.zeros((height, width), device=device)
v_prev = torch.zeros((height, width), device=device)
vort = torch.zeros((height, width), device=device)

# Cylinder obstacle (movable, on CPU for simplicity, converted to mask on GPU)
cyl_x, cyl_y = width // 4, height // 2
cyl_r = height // 8
xx_np, yy_np = np.meshgrid(range(width), range(height))
solid_np = ((xx_np - cyl_x)**2 + (yy_np - cyl_y)**2 < cyl_r**2)
solid = torch.tensor(solid_np, device=device, dtype=torch.bool)

def update_solid():
    global solid
    solid_np = ((xx_np - cyl_x)**2 + (yy_np - cyl_y)**2 < cyl_r**2)
    solid = torch.tensor(solid_np, device=device, dtype=torch.bool)

def set_bnd(b, x):
    if b == 2:
        x[0, 1:-1] = -x[1, 1:-1]
        x[-1, 1:-1] = -x[-2, 1:-1]
    else:
        x[0, 1:-1] = x[1, 1:-1]
        x[-1, 1:-1] = x[-2, 1:-1]
    if b == 1:
        x[1:-1, 0] = -x[1:-1, 1]
    else:
        x[1:-1, 0] = x[1:-1, 1]
    x[1:-1, -1] = x[1:-1, -2]
    x[0, 0] = 0.5 * (x[1, 0] + x[0, 1])
    x[0, -1] = 0.5 * (x[1, -1] + x[0, -2])
    x[-1, 0] = 0.5 * (x[-2, 0] + x[-1, 1])
    x[-1, -1] = 0.5 * (x[-2, -1] + x[-1, -2])

def diffuse(b, x, x0, kappa):
    a = dt * kappa * (width - 2) * (height - 2)
    for _ in range(iterations):
        x[1:-1, 1:-1] = (x0[1:-1, 1:-1] + a * (x[:-2, 1:-1] + x[2:, 1:-1] + x[1:-1, :-2] + x[1:-1, 2:])) / (1 + 4 * a)
        set_bnd(b, x)

def project(u, v, p, div):
    div[1:-1, 1:-1] = -0.5 * (u[1:-1, 2:] - u[1:-1, :-2] + v[2:, 1:-1] - v[:-2, 1:-1]) / max(width, height)
    p[:] = 0
    set_bnd(0, div)
    set_bnd(0, p)
    for _ in range(iterations):
        p[1:-1, 1:-1] = (div[1:-1, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:] + p[:-2, 1:-1] + p[2:, 1:-1]) / 4
        set_bnd(0, p)
    u[1:-1, 1:-1] -= 0.5 * (p[1:-1, 2:] - p[1:-1, :-2]) * max(width, height)
    v[1:-1, 1:-1] -= 0.5 * (p[2:, 1:-1] - p[:-2, 1:-1]) * max(width, height)
    set_bnd(1, u)
    set_bnd(2, v)

def advect(b, d, d0, u, v):
    dtx = dt * (max(width, height) - 2)
    j_grid, i_grid = torch.meshgrid(torch.arange(1, width-1, device=device), torch.arange(1, height-1, device=device), indexing='xy')
    x = j_grid - dtx * u[1:-1, 1:-1]
    y = i_grid - dtx * v[1:-1, 1:-1]
    x = torch.clamp(x, 0.5, width - 1.5)
    y = torch.clamp(y, 0.5, height - 1.5)
    j0 = torch.floor(x).long()
    j1 = j0 + 1
    i0 = torch.floor(y).long()
    i1 = i0 + 1
    s1 = x - j0.float()
    s0 = 1 - s1
    t1 = y - i0.float()
    t0 = 1 - t1
    d[1:-1, 1:-1] = s0 * (t0 * d0[i0, j0] + t1 * d0[i1, j0]) + s1 * (t0 * d0[i0, j1] + t1 * d0[i1, j1])
    set_bnd(b, d)

def compute_vorticity(u, v, vort):
    vort[1:-1, 1:-1] = (v[1:-1, 2:] - v[1:-1, :-2]) - (u[2:, 1:-1] - u[:-2, 1:-1])

def fluid_step(t):
    global u, v, dens, u_prev, v_prev, dens_prev
    
    # Compute E8 v_sum at current t (modulates inflow) - on CPU
    v_sum = np.zeros(8)
    for p, v_p_ref in reflected_vectors:
        if np.linalg.norm(v_p_ref) > 0:
            decay = np.exp(-t * np.log(p))
            v_sum += v_p_ref * decay
    
    # Inflow: base u=1 + E8 modulation, add density tracer
    inflow_u = 1.0 + force_scale * v_sum[0]
    inflow_v = force_scale * v_sum[1]  # Small vertical perturbation
    u[:, 1:3] = inflow_u
    v[:, 1:3] = inflow_v
    dens[height//4:3*height//4, 1:3] += 100  # Increased tracer for visibility
    
    # Diffuse velocity
    u_prev.copy_(u)
    diffuse(1, u, u_prev, visc)
    v_prev.copy_(v)
    diffuse(2, v, v_prev, visc)
    
    # Project
    project(u, v, u_prev, v_prev)
    
    # Advect velocity
    u_prev.copy_(u)
    v_prev.copy_(v)
    advect(1, u, u_prev, u, v)
    advect(2, v, v_prev, u, v)
    
    # Project again
    project(u, v, u_prev, v_prev)
    
    # Diffuse and advect density
    dens_prev.copy_(dens)
    diffuse(0, dens, dens_prev, diff)
    dens_prev.copy_(dens)
    advect(0, dens, dens_prev, u, v)
    
    # Enforce cylinder (no-slip, no density)
    u[solid] = 0
    v[solid] = 0
    dens[solid] = 0

# Pygame setup
pygame.init()
display = pygame.display.set_mode((width * scale, height * scale))
pygame.display.set_caption("E8-Bounded Karman Vortex Street Simulation (GPU-Accelerated with PyTorch - Interactive Object)")
clock = pygame.time.Clock()
t = 0.0
dragging = False
white = (255, 255, 255)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            gx = mx // scale
            gy = my // scale
            if (gx - cyl_x)**2 + (gy - cyl_y)**2 < cyl_r**2:
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            mx, my = event.pos
            cyl_x = mx // scale
            cyl_y = my // scale
            cyl_x = max(int(cyl_r), min(width - int(cyl_r) - 1, cyl_x))
            cyl_y = max(int(cyl_r), min(height - int(cyl_r) - 1, cyl_y))
            update_solid()
    
    fluid_step(t)
    t += dt
    
    # Compute vorticity for enhanced visualization
    compute_vorticity(u, v, vort)
    
    # Draw with light blue fluid (water color) on white background
    dens_clamped = torch.clamp(dens, 0, 255).byte()
    mask = dens_clamped > 0
    red = torch.where(mask, torch.tensor(0, device=device), torch.tensor(255, device=device))
    green = torch.where(mask, (dens_clamped * 0.5).byte(), torch.tensor(255, device=device))
    blue = torch.where(mask, dens_clamped, torch.tensor(255, device=device))
    colors = torch.stack([red, green, blue], dim=-1).byte()
    
    # Render to Pygame
    display.fill(white)
    surf = pygame.Surface((width, height))
    surfarray.blit_array(surf, colors.transpose(0, 1).cpu().numpy())
    pygame.transform.scale(surf, (width * scale, height * scale), display)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
