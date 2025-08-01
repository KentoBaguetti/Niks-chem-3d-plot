import numpy as np
from plot3dPoints import x, y, z, yes_indices_set

green_points = []
red_points = []

for i in range(len(x)):
    if i + 1 in yes_indices_set:
        green_points.append([x[i], y[i], z[i]])
    else:
        red_points.append([x[i], y[i], z[i]])

green_points = np.array(green_points)
red_points = np.array(red_points)

initial_center = np.mean(green_points, axis=0)
print(f"Initial center: {initial_center}")


def calculate_score(center, radius):
    """
    Calculate a score for sphere parameters.
    Higher score is better.

    We'll use a weighted sum of:
    - Percentage of green points inside the sphere
    - Percentage of red points outside the sphere
    """
    green_distances = np.sqrt(np.sum((green_points - center) ** 2, axis=1))
    red_distances = np.sqrt(np.sum((red_points - center) ** 2, axis=1))

    green_inside = sum(1 for d in green_distances if d <= radius)
    red_inside = sum(1 for d in red_distances if d <= radius)

    green_total = len(green_points)
    red_total = len(red_points)

    green_inside_percent = green_inside / green_total * 100
    red_outside_percent = (red_total - red_inside) / red_total * 100

    weight_green = 0.7
    weight_red = 0.3
    score = weight_green * green_inside_percent + weight_red * red_outside_percent

    return score, green_inside, green_total, red_inside, red_total


center_range = 2.0
center_steps = 5
radius_min = 5.0
radius_max = 15.0
radius_steps = 20

x_centers = np.linspace(
    initial_center[0] - center_range, initial_center[0] + center_range, center_steps
)
y_centers = np.linspace(
    initial_center[1] - center_range, initial_center[1] + center_range, center_steps
)
z_centers = np.linspace(
    initial_center[2] - center_range, initial_center[2] + center_range, center_steps
)
radii = np.linspace(radius_min, radius_max, radius_steps)

best_score = -1
best_center = initial_center
best_radius = 9.9
best_metrics = None

#  grid search
print("Starting grid search...")
total_iterations = len(x_centers) * len(y_centers) * len(z_centers) * len(radii)
print(f"Total combinations to test: {total_iterations}")

iteration = 0
for x_c in x_centers:
    for y_c in y_centers:
        for z_c in z_centers:
            center = np.array([x_c, y_c, z_c])

            for radius in radii:
                iteration += 1
                if iteration % 1000 == 0:
                    print(
                        f"Progress: {iteration}/{total_iterations} ({iteration / total_iterations * 100:.1f}%)"
                    )

                score, green_inside, green_total, red_inside, red_total = (
                    calculate_score(center, radius)
                )

                if score > best_score:
                    best_score = score
                    best_center = center.copy()
                    best_radius = radius
                    best_metrics = (green_inside, green_total, red_inside, red_total)

# Print results
print("\nGrid search complete!")
print(
    f"Best center: ({best_center[0]:.2f}, {best_center[1]:.2f}, {best_center[2]:.2f})"
)
print(f"Best radius: {best_radius:.2f}")
print(f"Best score: {best_score:.2f}")

green_inside, green_total, red_inside, red_total = best_metrics
print(
    f"Green points inside: {green_inside}/{green_total} ({green_inside / green_total * 100:.1f}%)"
)
print(
    f"Red points inside: {red_inside}/{red_total} ({red_inside / red_total * 100:.1f}%)"
)
print(
    f"Green points outside: {green_total - green_inside}/{green_total} ({(green_total - green_inside) / green_total * 100:.1f}%)"
)
print(
    f"Red points outside: {red_total - red_inside}/{red_total} ({(red_total - red_inside) / red_total * 100:.1f}%)"
)

(
    initial_score,
    initial_green_inside,
    initial_green_total,
    initial_red_inside,
    initial_red_total,
) = calculate_score(initial_center, 9.9)
print("\nComparison with initial parameters:")
print(
    f"Initial center: ({initial_center[0]:.2f}, {initial_center[1]:.2f}, {initial_center[2]:.2f})"
)
print(f"Initial radius: 9.90")
print(f"Initial score: {initial_score:.2f}")
print(
    f"Initial green inside: {initial_green_inside}/{initial_green_total} ({initial_green_inside / initial_green_total * 100:.1f}%)"
)
print(
    f"Initial red inside: {initial_red_inside}/{initial_red_total} ({initial_red_inside / initial_red_total * 100:.1f}%)"
)

improvement = (best_score - initial_score) / initial_score * 100
print(f"\nScore improvement: {improvement:.1f}%")

with open("best_sphere_params.txt", "w") as f:
    f.write(f"center_x={best_center[0]}\n")
    f.write(f"center_y={best_center[1]}\n")
    f.write(f"center_z={best_center[2]}\n")
    f.write(f"radius={best_radius}\n")
