# This file is part of ts_rotator_analysis.
#
# Developed for the Rubin Observatory Telescope and Site System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import numpy as np
import numpy.typing
import matplotlib.pyplot as plt

from read_binary import read_binary


def normalize(
    data: numpy.typing.NDArray[np.float64],
) -> numpy.typing.NDArray[np.float64]:
    """Normalize the data.

    Parameters
    ----------
    data : `numpy.ndarray`
        Data to normalize.

    Returns
    -------
    `numpy.ndarray`
        Normalized data.
    """
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def analyze(data_filepath: str, first_points: int, cut_final_points: int) -> None:
    """Analyze the telemetry data.

    Parameters
    ----------
    data_filepath : `str`
        Path to the telemetry file.
    first_points : `int`
        Read the first n items of data (should be >= 0).
    cut_final_points : `int`
        Cut the final points (should be > 0).
    """

    first_n_items = None if (first_points == 0) else first_points
    data_file = read_binary(data_filepath, first_n_items=first_n_items)

    exp_times = np.array(data_file["time"])[:-cut_final_points]
    exp_times -= exp_times[0]

    ref_times = np.array(data_file["refTime"])[:-cut_final_points]
    ref_times -= ref_times[0]

    position = np.array(data_file["Rotator_Position_deg"])[:-cut_final_points]
    rate = np.array(data_file["Ch_RateFb"])[:-cut_final_points, :]
    rate_cmd = np.array(data_file["Ch_RateCmd"])[:-cut_final_points, :]

    current = np.array(data_file["actMotorCurrent"])[:-cut_final_points, :]
    current_cmd = np.array(data_file["CurrentOut_Axis"])[:-cut_final_points, :]

    linear_encoder = np.array(data_file["bissLinearEncoder_axis"])[
        :-cut_final_points, :
    ]
    motor_encoder = np.array(data_file["bissMotorEncoder_axis"])[:-cut_final_points, :]

    # Process the reference clock time
    diff_ref_times = np.diff(ref_times)
    diff_ref_times_processed = diff_ref_times[diff_ref_times > 0]

    # Print the information
    print("The delta processed reference clock time is:\n"
          f"mean = {np.mean(diff_ref_times_processed) * 1e9} ns\n"
          f"std = {np.std(diff_ref_times_processed) * 1e9} ns")
    print("The delta application time is:\n"
          f"mean = {np.mean(np.diff(exp_times)) * 1e9} ns\n"
          f"std = {np.std(np.diff(exp_times)) * 1e9} ns")

    # Check the application time
    plt.figure()
    plt.plot(exp_times, "bx-")
    plt.xlabel("Data point")
    plt.ylabel("Application Time [s]")

    # Check the reference clock time
    plt.figure()
    plt.plot(ref_times, "bx-")
    plt.xlabel("Data point")
    plt.ylabel("Reference clock Time [s]")

    # Check the time difference of the data
    plt.figure()
    plt.hist(diff_ref_times_processed, alpha=0.5, bins=100)
    plt.hist(np.diff(exp_times), alpha=0.5, bins=100)
    plt.legend(["Reference clock", "Application"])
    plt.xlabel("Time difference [s]")
    plt.ylabel("Amount")
    plt.title("Time difference distribution")

    # Check the position
    plt.figure()
    plt.plot(exp_times, position)
    plt.xlabel("Time [s]")
    plt.ylabel("Position [deg]")

    # Check the velocity and the related command
    plt.figure()
    plt.plot(exp_times, rate[:, 0], "b")
    plt.plot(exp_times, rate_cmd[:, 0], "r")
    plt.legend(["ChA", "ChA Cmd"])
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [deg/s]")

    plt.figure()
    plt.plot(exp_times, rate[:, 1], "b")
    plt.plot(exp_times, rate_cmd[:, 1], "r")
    plt.legend(["ChB", "ChB Cmd"])
    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [deg/s]")

    # Check the current and the related command
    plt.figure()
    plt.plot(exp_times, current[:, 0], "b")
    plt.plot(exp_times, current[:, 1], "r")
    plt.plot(exp_times, current_cmd[:, 0], "y--")
    plt.plot(exp_times, current_cmd[:, 1], "k--")
    plt.legend(["Current A", "Current B", "Current A Cmd", "Current B Cmd"])
    plt.xlabel("Time [s]")
    plt.ylabel("Current [A]")

    # Check the linear encoder
    plt.figure()
    plt.plot(exp_times, linear_encoder[:, 0] - linear_encoder[0, 0], "bx-")
    plt.plot(exp_times, linear_encoder[:, 1] - linear_encoder[0, 1], "rx--")
    plt.legend(["Shifted ChA", "Shifted ChB"])
    plt.xlabel("Time [s]")
    plt.ylabel("Encoder Value")
    plt.title("Linear Encoder (Shifted)")

    # Check the difference of linear encoder values
    plt.figure()
    plt.plot(exp_times[:-1], np.diff(linear_encoder[:, 0]), "bx-")
    plt.plot(exp_times[:-1], np.diff(linear_encoder[:, 1]), "rx-")
    plt.legend(["ChA", "ChB"])
    plt.xlabel("Time [s]")
    plt.ylabel("Encoder Value")
    plt.title("Diff Linear Encoder")

    # Check the motor encoder
    plt.figure()
    plt.plot(exp_times, motor_encoder[:, 0] - motor_encoder[0, 0], "bx-")
    plt.plot(exp_times, motor_encoder[:, 1] - motor_encoder[0, 1], "rx-")
    plt.legend(["Shifted ChA", "Shifted ChB"])
    plt.xlabel("Time [s]")
    plt.ylabel("Encoder Value")
    plt.title("Motor Encoder")

    # Check the difference of motor encoder values
    plt.figure()
    plt.plot(exp_times[:-1], np.diff(motor_encoder[:, 0]), "bx-")
    plt.plot(exp_times[:-1], np.diff(motor_encoder[:, 1]), "rx-")
    plt.legend(["ChA", "ChB"])
    plt.xlabel("Time [s]")
    plt.ylabel("Encoder Value")
    plt.title("Diff Motor Encoder")

    # Compare the differences of the linear and motor encoder values
    plt.figure()
    plt.plot(exp_times[:-1], normalize(np.diff(linear_encoder[:, 0])), "b")
    plt.plot(exp_times[:-1], normalize(np.diff(linear_encoder[:, 1])), "r--")
    plt.plot(exp_times[:-1], normalize(np.diff(motor_encoder[:, 0])), "k")
    plt.plot(exp_times[:-1], normalize(np.diff(motor_encoder[:, 1])), "y--")
    plt.legend(["Linear ChA", "Linear ChB", "Motor ChA", "Motor ChB"])
    plt.xlabel("Time [s]")
    plt.ylabel("Normalized Encoder Value")
    plt.title("Diff Linear and Moter Encoders")

    # Show all figures
    plt.show()


if __name__ == "__main__":
    # Define the parser
    parser = argparse.ArgumentParser(description="Analyze the telemetry file.")
    parser.add_argument("file", type=str, help="Path to the telemetry file.")
    parser.add_argument(
        "--first-points",
        type=int,
        default=0,
        help="Use the first points (should be > 0). If not specified, the default value is 0.",
    )
    parser.add_argument(
        "--cut-points",
        type=int,
        default=1,
        help="Cut the final points (should be > 0). If not specified, the default value is 1.",
    )

    args = parser.parse_args()

    # Read the telemetry file and analyze it
    cut_final_points = 1 if args.cut_points < 1 else args.cut_points
    analyze(args.file, args.first_points, cut_final_points)
