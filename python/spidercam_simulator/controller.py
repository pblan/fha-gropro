from __future__ import annotations

import logging
import numpy as np

import spidercam_simulator


class Controller:
    """🎮 A class for initializing and controlling the spidercam"""

    def __init__(
        self,
        dim: tuple = (1, 1, 1),
        start: tuple = (0, 0, 0),
        max_velocity: float = 1.0,
        acceleration: float = 1.0,
        freq: float = 1.0,
        instructions: list[spidercam_simulator.Instruction] = None,
    ) -> None:
        """✨ Initializes the Controller class

        Args:
            dim (tuple, optional): The dimensions of the field. Defaults to (1, 1, 1).
            start (tuple, optional): The starting position of the spidercam. Defaults to (0, 0, 0).
            max_velocity (float, optional): The maximum velocity of the spidercam. Defaults to 1.0.
            acceleration (float, optional): The maximum acceleration of the spidercam. Defaults to 1.0.
            freq (float, optional): The discrete time frequency. Defaults to 1.0.
            instructions (list, optional): The instructions for the spidercam. Defaults to [].

        Returns:
            None
        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug(
            "Initializing Controller with dim=%s, start=%s, max_velocity=%s, acceleration=%s, freq=%s, instructions=%s",
            dim,
            start,
            max_velocity,
            acceleration,
            freq,
            instructions,
        )

        self.dim = dim
        self.spidercam = spidercam_simulator.Spidercam(
            self, max_velocity, acceleration, start
        )
        self.freq = freq
        self.instructions = instructions

        self.cam_positions = []
        self.rope_lengths = []

        self.store_anchors()

    def store_anchors(self) -> None:
        """📦 Stores the anchor positions in regard to the dimensions

        Returns:
            None
        """

        # Anchors are at the top corners of the field
        self.anchors = [
            (0, 0, self.dim[2]),
            (self.dim[0], 0, self.dim[2]),
            (0, self.dim[1], self.dim[2]),
            (self.dim[0], self.dim[1], self.dim[2]),
        ]

    @classmethod
    def from_dict(cls, data: dict) -> "Controller":
        """📔 Creates a Controller object from a dictionary

        Args:
            data (dict): The dictionary to create the Controller object from
                - dim (tuple): The dimensions of the field
                - start (tuple): The starting position of the spidercam
                - max_velocity (float): The maximum velocity of the spidercam
                - acceleration (float): The maximum acceleration of the spidercam
                - freq (float): The discrete time frequency
                - instructions (list): The instructions for the spidercam

        Returns:
            Controller: The Controller object
        """

        cls.logger = logging.getLogger(__name__)
        cls.logger.debug("Creating Controller from dict %s", data)
        return cls(**data)

    def __repr__(self) -> str:
        """🧵 Returns a string representation of the Controller object

        Returns:
            str: The string representation of the Controller object
        """
        return f"Controller({self.dim=}, {self.spidercam.start=}, {self.spidercam.max_velocity=}, {self.spidercam.acceleration=}, {self.freq=}, {self.instructions=})"

    def run(self) -> tuple[list[tuple], list[tuple]]:
        """👟 Runs the instructions for the spidercam

        Returns:
            tuple[list[tuple], list[tuple]]: The positions and rope lengths for each time step
        """

        current_time = 0

        while True:
            self.logger.info("Current time: %s", current_time)

            if len(self.instructions) != 0:
                # Check if there is a new instruction
                if current_time >= self.instructions[0].start_time:
                    instruction = self.instructions.pop(0)

                    self.spidercam.move(instruction)
            else:
                self.spidercam.move()

            # Store cam_positions and rope_lengths
            position = self.spidercam.get_position(current_time)
            self.logger.info("Current position: %s", position)

            self.cam_positions.append(position)
            self.rope_lengths.append(self.get_rope_lengths(position))

            # Check if the last instruction is finished
            if (
                len(self.instructions) == 0
                and self.spidercam.movements[-1].end_time() < current_time
                and self.spidercam.queue is None
            ):
                self.logger.info(
                    "Last instruction finished and no more instructions left"
                )
                break

            current_time += 1 / self.freq

        return self.cam_positions, self.rope_lengths

    def get_rope_lengths(self, position: tuple) -> list[tuple]:
        """📏 Returns the rope lengths for a given position

        Returns:
            list[tuple]: The rope lengths
        """

        rope_lengths = [
            np.linalg.norm(np.array(anchor) - np.array(position))
            for anchor in self.anchors
        ]

        self.logger.debug("Rope lengths: %s", rope_lengths)

        return rope_lengths
