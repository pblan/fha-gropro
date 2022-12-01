from __future__ import annotations
import logging
import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    """📊 A class for plotting camera positions and rope lengths"""

    def __init__(
        self,
        dim: tuple = None,
        freq: float = 1.0,
        cam_positions: list = None,
        rope_lengths: list = None,
        output_dir: str = None,
        name: str = None,
    ) -> None:
        """✨ Initializes the Plotter class

        Args:
            dim (tuple, optional): The dimensions of the field. Defaults to None.
            freq (float, optional): The discrete time frequency. Defaults to 1.0.
            cam_positions (list, optional): The camera positions. Defaults to None.
            rope_lengths (list, optional): The rope lengths. Defaults to None.
            output_dir (str, optional): The output directory. Defaults to None.
            name (str, optional): The name of the plot. Defaults to None.

        Returns:
            None
        """

        self.logger = logging.getLogger(__name__)
        # Setting log level info to suppress matplotlib font manager warnings
        self.logger.setLevel(logging.INFO)

        self.logger.info("Initializing Plotter for %s", name)

        self.dim = dim
        self.freq = freq
        self.cam_positions = np.array(cam_positions)
        self.rope_lengths = np.array(rope_lengths)
        self.output_dir = output_dir
        self.name = name

    def plot_cam_positions(self) -> None:
        """📈 Plots the camera positions

        Returns:
            None
        """

        self.logger.info("Plotting camera positions for %s", self.name)

        # If output directory is not specified, plot to screen
        if self.output_dir is None:
            plt.ion()

        # Plot camera positions projection = 3d
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        # Set axis labels
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        # Set axis limits
        ax.set_xlim3d(0, self.dim[0])
        ax.set_ylim3d(0, self.dim[1])
        ax.set_zlim3d(0, self.dim[2])

        # Rotate so that origin is in the bottom left and z is up, angle is normal
        # ax.view_init(azim=0, elev=90)

        # Plot camera positions
        xline = self.cam_positions[:, 0]
        yline = self.cam_positions[:, 1]
        zline = self.cam_positions[:, 2]

        # Define color as distance from one point to the previous
        color = np.zeros(len(xline))
        for i in range(1, len(xline)):
            color[i] = np.linalg.norm(
                np.array([xline[i], yline[i], zline[i]])
                - np.array([xline[i - 1], yline[i - 1], zline[i - 1]])
            )

        # Plot camera positions
        ax.scatter(xline, yline, zline, c=color, cmap="coolwarm")

        # Plot start as big green x
        ax.scatter(xline[0], yline[0], zline[0], c="green", s=200, marker="x")

        # Set title for whole figure
        # fig.suptitle("Camera Positions for " + self.name)

        # Save or show plot
        if self.output_dir is None:
            plt.show()
        else:
            # Save at output + name + cam_pos.png
            plt.savefig(
                f"{self.output_dir}/{self.name}_cam_pos.png",
                bbox_inches="tight",
                dpi=300,
            )

    def plot_rope_lengths(self) -> None:
        """📈 Plots the rope lengths

        Returns:
            None
        """

        self.logger.info("Plotting rope lengths for %s", self.name)

        # If output directory is not specified, plot to screen
        if self.output_dir is None:
            plt.ion()

        # Plot rope lengths as a function of time (discrete)
        fig = plt.figure()

        # Set axis labels
        plt.xlabel("Time (s)")
        plt.ylabel("Rope Length (m)")

        # Set axis limits
        plt.xlim(0, len(self.rope_lengths) / self.freq)
        plt.ylim(0, np.max(self.rope_lengths) * 1.1)

        # Plot rope lengths
        plt.plot(
            np.arange(0, len(self.rope_lengths) / self.freq, 1 / self.freq),
            self.rope_lengths,
        )

        # Legend of Rope i
        plt.legend([f"Rope {i}" for i in range(len(self.rope_lengths[0]))])

        # Set title for whole figure
        # fig.suptitle("Rope Lengths for " + self.name)

        # Save or show plot
        if self.output_dir is None:
            plt.show()
        else:
            # Save at output + name + rope_lengths.png
            plt.savefig(
                f"{self.output_dir}/{self.name}_rope_lengths.png",
                bbox_inches="tight",
                dpi=300,
            )

    def plot(self) -> None:
        """📈 Plots the camera positions and rope lengths

        Returns:
            None
        """

        self.logger.info("Plotting camera positions and rope lengths for %s", self.name)

        self.plot_cam_positions()
        self.plot_rope_lengths()
