import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ast

# Function to read data from a file and return it as a list of floats
def read_data(filename):
    with open(filename, 'r') as file:
        data = file.read()
    # Use ast.literal_eval to safely evaluate the string as a list
    data = ast.literal_eval(data)
    return data

# Read data from the files
x_data = read_data('species_infox.txt')
y_data = read_data('species_infoy.txt')
z_data = read_data('species_infoz.txt')

# Calculate the average and standard deviation for each dimension
x_mean, y_mean, z_mean = np.mean(x_data), np.mean(y_data), np.mean(z_data)
x_std, y_std, z_std = np.std(x_data), np.std(y_data), np.std(z_data)

print(f"X - Mean: {x_mean}, Standard Deviation: {x_std}")
print(f"Y - Mean: {y_mean}, Standard Deviation: {y_std}")
print(f"Z - Mean: {z_mean}, Standard Deviation: {z_std}")

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_data, y_data, z_data, c='r', marker='o')

# Set limits to show up to 3 standard deviations from the average in each dimension
ax.set_xlim([x_mean - 3*x_std, x_mean + 3*x_std])
ax.set_ylim([y_mean - 3*y_std, y_mean + 3*y_std])
ax.set_zlim([z_mean - 3*z_std, z_mean + 3*z_std])

# Set labels
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

# Show plot
plt.show()
