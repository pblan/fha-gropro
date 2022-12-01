import csv
import sys
import numpy as np  # have to be installed via 'pip install numpy'
from matplotlib import (
    pyplot as plt,
    animation,
)  # have to be installed via 'pip install matplotlib'


def read_csv_file(filename: str):
    line_data = []
    with open(filename, mode="r", newline="") as file:
        csv_reader = csv.reader(file, delimiter=",")
        # first line: dim
        row = next(csv_reader)
        dim = [float(i) for i in row]
        for row in csv_reader:
            row = [float(i) for i in row]
            line_data.append(row)
    return [dim, line_data]


def plot_data(filename: str):
    [dim, line_data] = read_csv_file(filename)

    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    # Set axis ratio equal to values
    ax.set_box_aspect(dim)
    # Set view angle (elevation, azimuth)
    ax.view_init(7, 7)
    # Setting the axes properties
    ax.set_xlim3d([0.0, dim[0]])
    ax.set_xlabel("X")
    ax.set_ylim3d([0.0, dim[1]])
    ax.set_ylabel("Y")
    ax.set_zlim3d([0.0, dim[2]])
    ax.set_zlabel("Z")
    ax.set_title("Spidercam")

    # Plot green play ground
    xx, yy = np.meshgrid(range(int(dim[0])), range(int(dim[1])))
    zz = 0 * xx * yy
    ax.plot_surface(xx, yy, zz, alpha=0.5, color="g")
    time_label = fig.text(0.5, 0.1, "")

    # Initialize (empty) plots (values of every step will be set in animate function)
    lines = [ax.plot([], [], [], color="blue")[0] for _ in range(4)]
    # Define the points of the deflection pulleys (T=transpose, to use same indexing as line_data)
    r = np.array(
        [
            [0, 0, dim[2]],
            [dim[0], 0, dim[2]],
            [0, dim[1], dim[2]],
            [dim[0], dim[1], dim[2]],
        ]
    ).T

    # Function called every animation step
    # i: nr. of step
    def animate(i):
        for k in range(4):
            # set coordinates of the points
            lines[k].set_xdata([r[0][k], line_data[1][i]])
            lines[k].set_ydata([r[1][k], line_data[2][i]])
            lines[k].set_3d_properties([r[2][k], line_data[3][i]])
            time_label.set_text("t = " + str(line_data[0][i]))
        return lines

    # Start animation
    ani = animation.FuncAnimation(
        fig, animate, range(len(line_data[0])), interval=0, blit=False
    )

    # Show plot
    plt.show()


# Main
if len(sys.argv) < 2:
    raise Exception("Keine Datendatei angegeben")
else:
    plot_data(sys.argv[1])
