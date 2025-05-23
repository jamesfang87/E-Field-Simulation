import matplotlib.pyplot as plt
import numpy as np

from physics import calculate_voltage


def display_voltage(charges):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Generate grid data
    x = np.linspace(-12, 12, 100)
    y = np.linspace(-7, 7, 100)
    X, Y = np.meshgrid(x, y)

    # Calculate voltage at each grid point
    Z = np.zeros_like(X)
    for i in range(len(x)):
        for j in range(len(y)):
            # Calculate voltage using your custom function
            Z[i, j] = calculate_voltage(X[i, j], Y[i, j], charges)

    # Surface plot
    surf = ax.plot_surface(X, Y, Z, cmap="viridis")
    fig.colorbar(surf)
    ax.set_title("Electric Potential Field")
    ax.set_xlabel("X Position")
    ax.set_ylabel("Y Position")
    ax.set_zlabel("Voltage")
    plt.show()
