from __future__ import annotations

import logging
from enum import Enum

import numpy as np
import spidercam_simulator


class Phase:
    """🌔 A class for defining a phase"""

    Mode = Enum("Mode", ["ACCELERATION", "CONSTANT_VELOCITY", "DECELERATION"])

    def __init__(
        self,
        movement: spidercam_simulator.Movement,
        mode: Mode,
        start: tuple = (0, 0, 0),
        destination: tuple = (0, 0, 0),
        starting_velocity: float = 0,
    ) -> None:
        """✨ Initializes the Phase class

        Args:
            movement (Movement): The movement instance
            mode (Mode): The type of phase. Can be ACCELERATION, CONSTANT_VELOCITY, or DECELERATION
            start (tuple, optional): The starting position. Defaults to (0, 0, 0).
            destination (tuple, optional): The destination position. Defaults to (0, 0, 0).
            starting_velocity (float, optional): The starting velocity. Defaults to 0.

        Returns:
            None
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            "Initializing Phase with mode %s, start %s, destination %s, and starting velocity %s",
            mode,
            start,
            destination,
            starting_velocity,
        )

        self.movement = movement
        self.mode = mode
        self.start = start
        self.destination = destination
        self.starting_velocity = starting_velocity

        self.update()

    def update(self) -> None:
        """🔄 Updates the phase

        Args:
            None

        Returns:
            None
        """
        self.logger.debug("Updating phase %s", self.mode)

        self.distance = self.calc_distance()
        self.duration = self.calc_duration()

        self.logger.debug(
            "Updated phase with distance %s and duration %s",
            self.distance,
            self.duration,
        )

    def calc_distance(self) -> float:
        """📐 Returns the distance of the phase

        Returns:
            float: The distance of the phase
        """
        return np.linalg.norm(np.array(self.destination) - np.array(self.start))

    def calc_duration(self) -> float:
        """⏳ Returns the duration of the phase

        Returns:
            float: The duration of the phase
        """

        if self.mode == Phase.Mode.ACCELERATION:
            # t = sqrt(2 * d / a)
            return np.sqrt((2 * self.distance) / self.movement.spidercam.acceleration)
        elif self.mode == Phase.Mode.CONSTANT_VELOCITY:
            # t = d / v
            return self.distance / self.starting_velocity
        elif self.mode == Phase.Mode.DECELERATION:
            # t = v0 / a, because final velocity is 0
            return self.starting_velocity / self.movement.spidercam.acceleration

    def get_position(self, offset: float) -> tuple:
        """📍 Returns the position of the phase after a given offset

        Args:
            offset (float): The offset to get the position after

        Returns:
            tuple: The position of the phase after the given offset
        """

        self.logger.debug(
            "Getting position after %s seconds, mode %s", offset, self.mode
        )

        # if offset > self.duration:
        #     self.logger.debug(
        #         f"Offset {offset} is greater than duration {self.duration}, returning destination {repr(self.destination)}"
        #     )
        #     return self.destination

        if self.mode == Phase.Mode.ACCELERATION:
            distance = self.movement.spidercam.acceleration * offset**2 / 2
        elif self.mode == Phase.Mode.CONSTANT_VELOCITY:
            distance = self.starting_velocity * offset
        elif self.mode == Phase.Mode.DECELERATION:
            distance = (
                self.starting_velocity * offset
                - self.movement.spidercam.acceleration * offset**2 / 2
            )

        self.logger.debug("Phase distance: %s", distance)

        # if distance almost 0, return start
        if np.isclose(distance, 0):
            self.logger.debug(
                "Distance is almost 0, returning start %s", repr(self.start)
            )
            return self.start

        position = np.array(self.start) + (
            np.array(self.destination) - np.array(self.start)
        ) * distance / np.linalg.norm(np.array(self.destination) - np.array(self.start))

        self.logger.debug("Phase position: %s", position)

        return tuple(position)
