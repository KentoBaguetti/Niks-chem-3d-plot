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

# print statistics
print("Green points (soluble) stats:")
print(f"Count: {len(green_points)}")
print(f"Mean: {np.mean(green_points, axis=0)}")
print(f"Min: {np.min(green_points, axis=0)}")
print(f"Max: {np.max(green_points, axis=0)}")

print("\nRed points (insoluble) stats:")
print(f"Count: {len(red_points)}")
print(f"Mean: {np.mean(red_points, axis=0)}")
print(f"Min: {np.min(red_points, axis=0)}")
print(f"Max: {np.max(red_points, axis=0)}")

center = np.mean(green_points, axis=0)
print("\nPotential sphere center (mean of green points):")
print(f"Center: {center}")

green_distances = np.sqrt(np.sum((green_points - center) ** 2, axis=1))
red_distances = np.sqrt(np.sum((red_points - center) ** 2, axis=1))

print("\nDistances from center to green points:")
print(f"Min: {np.min(green_distances)}")
print(f"Max: {np.max(green_distances)}")
print(f"Mean: {np.mean(green_distances)}")

print("\nDistances from center to red points:")
print(f"Min: {np.min(red_distances)}")
print(f"Max: {np.max(red_distances)}")
print(f"Mean: {np.mean(red_distances)}")


green_distances.sort()
red_distances.sort()

print("\nSorted distances from center:")
print(f"Green: {green_distances}")
print(f"Red: {red_distances}")

best_radius = 0
best_score = -1

print("\nTesting different radii:")
for radius in np.linspace(0, 20, 100):
    green_included = sum(1 for d in green_distances if d <= radius)
    red_included = sum(1 for d in red_distances if d <= radius)

    green_percent = green_included / len(green_points) * 100
    red_percent = red_included / len(red_points) * 100

    score = green_included - red_included

    if score > best_score:
        best_score = score
        best_radius = radius

    if radius % 2 < 0.1:
        print(
            f"Radius: {radius:.2f}, Green included: {green_included}/{len(green_points)} ({green_percent:.1f}%), "
            f"Red included: {red_included}/{len(red_points)} ({red_percent:.1f}%), Score: {score}"
        )

print(f"\nBest radius: {best_radius:.2f}")
print(f"With this radius:")
green_included = sum(1 for d in green_distances if d <= best_radius)
red_included = sum(1 for d in red_distances if d <= best_radius)
print(
    f"Green included: {green_included}/{len(green_points)} ({green_included / len(green_points) * 100:.1f}%)"
)
print(
    f"Red included: {red_included}/{len(red_points)} ({red_included / len(red_points) * 100:.1f}%)"
)
