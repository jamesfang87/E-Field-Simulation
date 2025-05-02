import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Generate grid data
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))  # Example function

# Surface plot
surf = ax.plot_surface(X, Y, Z, cmap="viridis")
fig.colorbar(surf)  # Add color bar
ax.set_title("3D Surface Plot")
plt.show()
