import numpy as np
from plot3dPoints import x, y, z, yes_indices_set
from scipy.optimize import minimize

green_points = []
red_points = []

for i in range(len(x)):
    if i + 1 in yes_indices_set:
        green_points.append([x[i], y[i], z[i]])
    else:
        red_points.append([x[i], y[i], z[i]])

green_points = np.array(green_points)
red_points = np.array(red_points)


def calculate_score(params):
    """
    Calculate a score for sphere parameters.
    Higher score is better (more green inside, more red outside).

    params: [center_x, center_y, center_z, radius]
    """
    center = params[:3]
    radius = params[3]

    green_distances = np.sqrt(np.sum((green_points - center) ** 2, axis=1))
    red_distances = np.sqrt(np.sum((red_points - center) ** 2, axis=1))

    green_inside = sum(1 for d in green_distances if d <= radius)
    red_inside = sum(1 for d in red_distances if d <= radius)

    green_total = len(green_points)
    red_total = len(red_points)

    green_inside_ratio = green_inside / green_total
    red_outside_ratio = (red_total - red_inside) / red_total

    score = 0.7 * green_inside_ratio + 0.3 * red_outside_ratio

    return -score


# Initial guess like clustering from dsci100 !
initial_center = np.mean(green_points, axis=0)
initial_radius = 9.9
initial_params = np.append(initial_center, initial_radius)

# bounds for sphere
bounds = [
    (
        min(min(green_points[:, 0]), min(red_points[:, 0])),
        max(max(green_points[:, 0]), max(red_points[:, 0])),
    ),
    (
        min(min(green_points[:, 1]), min(red_points[:, 1])),
        max(max(green_points[:, 1]), max(red_points[:, 1])),
    ),
    (
        min(min(green_points[:, 2]), min(red_points[:, 2])),
        max(max(green_points[:, 2]), max(red_points[:, 2])),
    ),
    (1, 20),
]

# optimization algo
try:
    from scipy.optimize import minimize

    result = minimize(calculate_score, initial_params, bounds=bounds, method="L-BFGS-B")
    optimized_params = result.x

    optimized_center = optimized_params[:3]
    optimized_radius = optimized_params[3]

    green_distances = np.sqrt(np.sum((green_points - optimized_center) ** 2, axis=1))
    red_distances = np.sqrt(np.sum((red_points - optimized_center) ** 2, axis=1))

    green_inside = sum(1 for d in green_distances if d <= optimized_radius)
    red_inside = sum(1 for d in red_distances if d <= optimized_radius)

    green_total = len(green_points)
    red_total = len(red_points)

    print("Optimization successful!")
    print(
        f"Optimized Center: ({optimized_center[0]:.2f}, {optimized_center[1]:.2f}, {optimized_center[2]:.2f})"
    )
    print(f"Optimized Radius: {optimized_radius:.2f}")
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

    green_distances_initial = np.sqrt(
        np.sum((green_points - initial_center) ** 2, axis=1)
    )
    red_distances_initial = np.sqrt(np.sum((red_points - initial_center) ** 2, axis=1))

    green_inside_initial = sum(
        1 for d in green_distances_initial if d <= initial_radius
    )
    red_inside_initial = sum(1 for d in red_distances_initial if d <= initial_radius)

    print("\nComparison with initial parameters:")
    print(
        f"Initial Center: ({initial_center[0]:.2f}, {initial_center[1]:.2f}, {initial_center[2]:.2f})"
    )
    print(f"Initial Radius: {initial_radius:.2f}")
    print(
        f"Initial Green inside: {green_inside_initial}/{green_total} ({green_inside_initial / green_total * 100:.1f}%)"
    )
    print(
        f"Initial Red inside: {red_inside_initial}/{red_total} ({red_inside_initial / red_total * 100:.1f}%)"
    )

    initial_score = -calculate_score(initial_params)
    optimized_score = -calculate_score(optimized_params)
    improvement = (optimized_score - initial_score) / initial_score * 100

    print(f"\nScore improvement: {improvement:.1f}%")

except ImportError:
    print("SciPy not installed. Using initial parameters.")
    optimized_center = initial_center
    optimized_radius = initial_radius

    green_distances = np.sqrt(np.sum((green_points - optimized_center) ** 2, axis=1))
    red_distances = np.sqrt(np.sum((red_points - optimized_center) ** 2, axis=1))

    green_inside = sum(1 for d in green_distances if d <= optimized_radius)
    red_inside = sum(1 for d in red_distances if d <= optimized_radius)

    green_total = len(green_points)
    red_total = len(red_points)

    print(
        f"Center: ({optimized_center[0]:.2f}, {optimized_center[1]:.2f}, {optimized_center[2]:.2f})"
    )
    print(f"Radius: {optimized_radius:.2f}")
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

# write optimized spehre paramters to a txt file
with open("optimized_sphere_params.txt", "w") as f:
    f.write(f"center_x={optimized_center[0]}\n")
    f.write(f"center_y={optimized_center[1]}\n")
    f.write(f"center_z={optimized_center[2]}\n")
    f.write(f"radius={optimized_radius}\n")
