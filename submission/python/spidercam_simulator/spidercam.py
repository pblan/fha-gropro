from __future__ import annotations

import logging

import spidercam_simulator


class Spidercam:
    """🕷️ A class for controlling the spidercam"""

    movements = []
    queue = None

    def __init__(
        self,
        controller: spidercam_simulator.Controller,
        max_velocity: float = 1.0,
        acceleration: float = 1.0,
        start: tuple = (0, 0, 0),
    ) -> None:
        """✨ Initializes the Spidercam class

        Args:
            controller (Controller): The controller instance
            max_velocity (float, optional): The maximum velocity of the spidercam. Defaults to 1.0.
            acceleration (float, optional): The maximum acceleration of the spidercam. Defaults to 1.0.
            start (tuple, optional): The starting position of the spidercam. Defaults to (0, 0, 0).

        Returns:
            None
        """

        self.logger = logging.getLogger(__name__)
        self.logger.debug(
            "Initializing Spidercam with max_velocity=%s, acceleration=%s, start=%s",
            max_velocity,
            acceleration,
            start,
        )

        self.controller = controller
        self.max_velocity = max_velocity
        self.acceleration = acceleration
        self.start = start

        self.movements = []
        self.queue = None

        self.calc_constants()

    def calc_constants(self) -> None:
        """🧮 Calculates the following constants for the spidercam:

        - time_vmax: The time it takes to reach the maximum velocity
        $$t_{\\max} = \\frac{v_{\\max}}{a_{\\max}}$$

        - dist_vmax: The distance it takes to reach the maximum velocity
        $$d_{\\max} = \\frac{v_{\\max}^2}{2a_{\\max}}$$

        Returns:
            None
        """

        self.logger.debug("Calculating constraints for spidercam")

        self.time_vmax = self.max_velocity / self.acceleration
        self.dist_vmax = self.acceleration * self.time_vmax**2 / 2

    def move(
        self, instruction: spidercam_simulator.Instruction = None, time: float = -1.0
    ) -> None:
        """🕹️ Moves the spidercam to a given position or updates the current movement at a given time

        Args:
            Instruction (Instruction): The instruction to move the spidercam. Defaults to None.
            time (float): The time to update the current movement at. Defaults to -1.0.

        Returns:
            None
        """

        # Check if parameters are valid
        if instruction is None and time == -1.0:
            self.logger.debug("No instruction or time given, returning")
            return

        # No instruction given, update the current movement
        if instruction is None and time != -1.0:
            self.logger.debug("Updating movement at time %s", time)

            # REDUNDANT?
            # If there is no movement in the queue, return
            if self.queue is None:
                self.logger.debug("No movement in queue, returning")
                return

            # If the last movement is finished, add the movement in the queue to the movements list
            if self.movements[-1].end_time() <= time:
                self.logger.debug(
                    "Last movement is finished, adding queue to movements list"
                )
                self.movements.append(self.queue)
                self.queue = None
                return

            return

        # Instruction given, apply the instruction
        self.logger.debug("Moving spidercam with instruction %s", instruction)

        # First movement is always possible
        if len(self.movements) == 0:
            self.logger.debug("First movement registered")

            self.movements.append(
                spidercam_simulator.Movement(
                    self, instruction.start_time, self.start, instruction.destination
                )
            )
            return

        self.logger.debug("Checking if last movement is finished")
        self.logger.debug("Last movement: %s", self.movements[-1])

        # If the last movement is not finished, decelerate and update the queue
        if self.movements[-1].end_time() > instruction.start_time:
            self.logger.debug("Last movement is not yet finished")

            self.logger.debug("Queueing instruction %s", instruction)

            # Decelerate
            self.movements[-1].start_deceleration(instruction.start_time)

            # Overwrite queue
            self.queue = spidercam_simulator.Movement(
                self,
                self.movements[-1].end_time(),
                self.movements[-1].destination(),
                instruction.destination,
            )

            return

        # REDUNDANT ?
        # If the last movement is finished and there is a queue, move to the queue
        if self.queue is not None:
            self.logger.debug("Last movement is finished and there is a queue")
            self.logger.debug("Executing queue")

            self.movements.append(self.queue)
            self.queue = None

            # Move to the destination after the queue
            self.move(instruction)
            return

        # If the last movement is finished and there is no queue, move to the destination
        self.logger.debug("Last movement is finished and there is no queue")

        self.movements.append(
            spidercam_simulator.Movement(
                self,
                max(self.movements[-1].end_time(), instruction.start_time),
                self.movements[-1].destination(),
                instruction.destination,
            )
        )

    def get_position(self, time: float) -> tuple:
        """📡 Gets the position of the spidercam at a given time

        Args:
            time (float): The time to get the position at

        Returns:
            tuple: The position of the spidercam at the given time
        """

        self.logger.debug("Getting position at time %s", time)

        self.move(time=time)

        # If there are no movements, return the start position
        if len(self.movements) == 0:
            self.logger.debug("No movements registered, returning start position")
            return self.start

        # If the time is before the first movement, return the start position
        if time < self.movements[0].start_time:
            self.logger.debug("Time is before first movement, returning start position")
            return self.start

        # If the time is after the last movement, return the destination of the last movement
        if time > self.movements[-1].end_time():
            self.logger.debug(
                "Time is after last movement, returning destination of last movement"
            )
            return self.movements[-1].destination()

        # If the time is during a movement, return the position of that movement
        for movement in self.movements:
            if movement.start_time <= time <= movement.end_time():
                self.logger.debug(
                    "Time is during movement %s, returning position of movement",
                    movement,
                )
                return movement.get_position(time)

        # If the time is between movements, return the destination of the previous movement
        for i in range(len(self.movements) - 1):
            if self.movements[i].end_time() < time < self.movements[i + 1].start_time:
                self.logger.debug(
                    "Time is between movements %s and %s, returning destination of previous movement",
                    self.movements[i],
                    self.movements[i + 1],
                )
                return self.movements[i].destination()

        # If the time is not in any of the above cases, return the start position
        self.logger.debug(
            "Time is not in any of the above cases, returning start position"
        )
