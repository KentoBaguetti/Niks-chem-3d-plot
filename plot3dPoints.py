x = [15.5, 15.8, 15.8, 15.8, 15.3, 15.3, 16.8, 16.8, 19.4, 18.4, 14.5, 14.6, 19, 17.4, 16, 17.1, 18, 16.2, 15.5, 17, 16, 18, 14.7, 17, 17.8, 16, 7.9, 15.1, 15.6, 17.8, 18, 16, 16.9, 17.2, 16.7]
y = [10.4, 8.8, 6.1, 5.3, 0, 18, 5.7, 10.4, 7.4, 16.4, 8, 10, 8.8, 13.7, 5.7, 6.8, 12.3, 7.8, 8.6, 7.3, 5, 1.4, 12.3, 8, 4.4, 9, 12, 2.8, 5.6, 8.4, 16.6, 7.6, 5, 1.8, 4.3]
z = [7, 19.4, 16.4, 7.2, 0, 6.1, 8, 21.3, 5.3, 10.2, 13.5, 14, 5.9, 11.3, 15.8, 7.8, 7.2, 12.6, 9.7, 7.1, 11.2, 2, 22.3, 5, 6.9, 5.1, 8.7, 5.8, 9.8, 5.1, 7.4, 12.5, 4.3, 4.3, 4.3]

# Define soluble points
yes_indices = [2, 5, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 25, 27, 28, 30, 31, 32, 33, 34]
yes_indices_set = set(yes_indices)

# points with the indices listed in "yes_indices" should be coloured green, others are coloured red

green_points = []
red_points = []

for i in range(len(x)):
    coord = (x[i], y[i], z[i])
    if i + 1 in yes_indices_set:
        green_points.append(coord)
    else:
        red_points.append(coord)
        
print(f"Green Points: {green_points}")
print(f"Red Points: {red_points}")