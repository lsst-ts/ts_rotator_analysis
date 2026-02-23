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

import ctypes


class FileTelemetry(ctypes.LittleEndianStructure):
    """File telemetry from the controller. Called telemetryFileStructure_t
    in the controller's code.
    """

    _pack_ = 1
    _fields_ = [
        ("time", ctypes.c_double),
        ("refTime", ctypes.c_double),
        ("bissMotorEncoder_axis", ctypes.c_uint32 * 2),
        ("bissLinearEncoder_axis", ctypes.c_uint32 * 2),
        ("actual_torque_axis", ctypes.c_int16 * 2),
        ("actMotorCurrent", ctypes.c_double * 2),
        ("JerkCmd", ctypes.c_double),
        ("AccCmd", ctypes.c_double),
        ("RateCmd", ctypes.c_double),
        ("PositionCmd", ctypes.c_double),
        ("Ch_RateCmd", ctypes.c_double * 2),
        ("Ch_RateFb", ctypes.c_double * 2),
        ("Rotator_Position_deg", ctypes.c_double),
        ("CurrentOut_Axis", ctypes.c_double * 2),
    ]
