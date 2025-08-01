import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from plot3dPoints import x, y, z, yes_indices_set

green_points = []
red_points = []

for i in range(len(x)):
    coord = (x[i], y[i], z[i])
    if i + 1 in yes_indices_set:
        green_points.append(coord)
    else:
        red_points.append(coord)

center = np.array([14.26, 6.13, 10.66])
radius = 12.37

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection="3d")

# Split green coords
green_x = []
green_y = []
green_z = []
for coord in green_points:
    green_x.append(coord[0])
    green_y.append(coord[1])
    green_z.append(coord[2])

# Split red coords
red_x = []
red_y = []
red_z = []
for coord in red_points:
    red_x.append(coord[0])
    red_y.append(coord[1])
    red_z.append(coord[2])

ax.scatter(green_x, green_y, green_z, color="green", label="Soluble", s=50)
ax.scatter(red_x, red_y, red_z, color="red", label="Insoluble", s=50)

u = np.linspace(0, 2 * np.pi, 30)
v = np.linspace(0, np.pi, 30)
sphere_x = center[0] + radius * np.outer(np.cos(u), np.sin(v))
sphere_y = center[1] + radius * np.outer(np.sin(u), np.sin(v))
sphere_z = center[2] + radius * np.outer(np.ones(np.size(u)), np.cos(v))

ax.plot_surface(sphere_x, sphere_y, sphere_z, color="blue", alpha=0.1)

ax.scatter(
    [center[0]],
    [center[1]],
    [center[2]],
    color="blue",
    s=100,
    marker="*",
    label="Sphere Center",
)


def is_inside_sphere(point, center, radius):
    return np.sqrt(np.sum((np.array(point) - center) ** 2)) <= radius


green_inside = sum(1 for p in green_points if is_inside_sphere(p, center, radius))
red_inside = sum(1 for p in red_points if is_inside_sphere(p, center, radius))

green_total = len(green_points)
red_total = len(red_points)

stats_text = (
    f"Sphere stats:\n"
    f"Center: ({center[0]:.2f}, {center[1]:.2f}, {center[2]:.2f})\n"
    f"Radius: {radius:.2f}\n"
    f"Green inside: {green_inside}/{green_total} ({green_inside / green_total * 100:.1f}%)\n"
    f"Red inside: {red_inside}/{red_total} ({red_inside / red_total * 100:.1f}%)"
)

ax.text2D(
    0.02,
    0.95,
    stats_text,
    transform=ax.transAxes,
    fontsize=10,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.5),
)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
# ax.set_title("3D Scatter Plot with Goon Sphere")
ax.set_title("3D Scatter Plot with Blue Sphere")

ax.legend()

plt.tight_layout()
plt.show()
