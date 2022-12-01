from __future__ import annotations

import logging

import numpy as np
import spidercam_simulator


class Movement:
    """➡️ A class for defining a movement"""

    phases: list[spidercam_simulator.Phase] = []

    def __init__(
        self,
        spidercam: spidercam_simulator.Spidercam,
        start_time: float = 0,
        start: tuple = (0, 0, 0),
        destination: tuple = (0, 0, 0),
    ) -> None:
        """✨ Initializes the Movement class

        Args:
            spidercam (Spidercam): The spidercam instance
            start_time (float, optional): The time to start the movement. Defaults to 0.
            start (tuple, optional): The starting position. Defaults to (0, 0, 0).
            destination (tuple, optional): The destination position. Defaults to (0, 0, 0).
        Returns:
            None
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            "Initializing Movement at %s with start %s and destination %s",
            start_time,
            start,
            destination,
        )

        self.spidercam = spidercam
        self.start_time = start_time
        self.start = start
        self.destination = destination

        self.calculate_phases()

    def duration(self) -> float:
        """⏳ Returns the duration of the movement

        Returns:
            float: The duration of the movement
        """
        return sum(phase.duration for phase in self.phases)

    def distance(self) -> float:
        """📐 Returns the distance of the movement

        Returns:
            float: The distance of the movement
        """
        return sum(phase.distance for phase in self.phases)

    def end_time(self) -> float:
        """🏁 Returns the end time of the movement

        Returns:
            float: The end time of the movement
        """
        return self.start_time + self.duration()

    def calculate_phases(self) -> None:
        """📐 Calculates the phases of the movement

        Returns:
            None
        """
        # HERE 3
        self.logger.info("Calculating phases")

        distance = np.linalg.norm(np.array(self.destination) - np.array(self.start))

        # Check how many phases are needed
        if distance <= 2 * self.spidercam.dist_vmax:
            # Only acceleration and deceleration
            self.logger.debug("Only acceleration and deceleration needed")

            # Calculate middle point
            middle_point = (
                self.start + (np.array(self.destination) - np.array(self.start)) / 2
            )
            self.phases = [
                spidercam_simulator.Phase(
                    self,
                    spidercam_simulator.Phase.Mode.ACCELERATION,
                    self.start,
                    middle_point,
                    0.0,
                ),
                spidercam_simulator.Phase(
                    self,
                    spidercam_simulator.Phase.Mode.DECELERATION,
                    middle_point,
                    self.destination,
                    # starting velocity is the velocity at the end of the acceleration phase
                    # v = sqrt(ad)
                    np.sqrt(self.spidercam.acceleration * distance),
                ),
            ]

        else:
            # Acceleration, constant velocity and deceleration
            # HERE 4
            self.logger.debug("Acceleration, constant velocity and deceleration needed")

            # Calculate needed points
            point_a = (
                np.array(self.start)
                + (np.array(self.destination) - np.array(self.start))
                * self.spidercam.dist_vmax
                / distance
            )

            point_b = (
                np.array(self.destination)
                - (np.array(self.destination) - np.array(self.start))
                * self.spidercam.dist_vmax
                / distance
            )

            self.phases = [
                spidercam_simulator.Phase(
                    self,
                    spidercam_simulator.Phase.Mode.ACCELERATION,
                    self.start,
                    point_a,
                    0.0,
                ),
                spidercam_simulator.Phase(
                    self,
                    spidercam_simulator.Phase.Mode.CONSTANT_VELOCITY,
                    point_a,
                    point_b,
                    self.spidercam.max_velocity,
                ),
                spidercam_simulator.Phase(
                    self,
                    spidercam_simulator.Phase.Mode.DECELERATION,
                    point_b,
                    self.destination,
                    self.spidercam.max_velocity,
                ),
            ]

    def start_deceleration(self, time: float) -> None:
        """🚦 Starts deceleration

        Args:
            time (float): The time to start deceleration

        Returns:
            None
        """

        # HERE 2
        self.logger.info("Starting deceleration at %s", time)

        # Getting the phase that is active at the time
        # and the time offset of the phase
        # update all phases after the phase

        time_sum = self.start_time

        for phase in self.phases:
            # Skip phases before the time
            if time_sum + phase.duration < time:
                time_sum += phase.duration
                continue

            # Nothing to do if already decelerating
            if phase.mode == spidercam_simulator.Phase.Mode.DECELERATION:
                self.logger.debug("Already decelerating, nothing to do")
                return

            offset = time - time_sum

            # Found phase should end at offset
            phase.destination = phase.get_position(offset)
            phase.update()

            # Update next phases
            # There always is a next phase because the final phase is deceleration and the previous phase was not
            next_phase = self.phases[self.phases.index(phase) + 1]

            next_phase.start = phase.destination
            next_phase.starting_velocity = (
                self.spidercam.max_velocity
                if phase.mode is spidercam_simulator.Phase.Mode.CONSTANT_VELOCITY
                else self.spidercam.acceleration * offset
            )
            next_phase.mode = spidercam_simulator.Phase.Mode.DECELERATION
            next_phase.destination = next_phase.get_position(
                next_phase.starting_velocity / self.spidercam.acceleration
            )
            next_phase.update()

            # If there is a phase after the next phase, pop it
            if len(self.phases) > self.phases.index(next_phase) + 1:
                self.phases.pop(self.phases.index(next_phase) + 1)

            break

        # # If there are two deceleration phases at the end, delete the second one
        # if (
        #     self.phases[-1].mode == spidercam_simulator.Phase.Mode.DECELERATION
        #     and self.phases[-2].mode == spidercam_simulator.Phase.Mode.DECELERATION
        # ):
        #     self.phases.pop()

        # Update the destination of the movement
        self.destination = self.phases[-1].destination

        # Debug: Check if destination of movement is the same as the destination of the last phase
        if not np.array_equal(self.destination, self.phases[-1].destination):
            self.logger.error(
                "Destination of movement is not the same as the destination of the last phase (%s != %s)",
                self.destination,
                self.phases[-1].destination,
            )

    def get_phase(self, time: float) -> spidercam_simulator.Phase:
        """📐 Returns the phase at the given time

        Args:
            time (float): The time to get the phase at

        Returns:
            Phase: The phase at the given time
        """
        time_sum = self.start_time

        for phase in self.phases:
            if time_sum + phase.duration > time:
                return phase
            time_sum += phase.duration

        return self.phases[-1]

    def __repr__(self):
        return f"Movement(start={repr(self.start)}, destination={repr(self.destination)}, start_time={self.start_time}, duration={self.duration()}, distance={self.distance()})"

    def get_position(self, time: float) -> tuple:
        """🔎 Returns the position of the movement at the time

        Args:
            time (float): The time to get the position for

        Returns:
            tuple: The position of the movement at the time
        """

        self.logger.info("Getting position for time %s", time)

        # Getting the phase that is active at the time
        # and the time offset of the phase
        time_sum = self.start_time

        for phase in self.phases:
            if time_sum + phase.duration >= time:
                return phase.get_position(time - time_sum)

            time_sum += phase.duration

        raise Exception("No phase found")
