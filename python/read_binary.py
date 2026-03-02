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
import warnings
from pathlib import Path

from file_telemetry import FileTelemetry


def read_binary(file_path, first_n_items=None):
    """Read the binary file.

    Parameters
    ----------
    file_path : str
        Binary file path.
    first_n_items : int or None, optional
        Read the first n items of data. If None, all items will be read.
        (default is None.)

    Returns
    -------
    data_file : dict
        Data of the file telemetry.
    """

    # Get the c structrue and related size
    struct_file_tel = FileTelemetry()
    size_file_tel = ctypes.sizeof(struct_file_tel)

    # Set the default data
    data_file = _get_default_data(struct_file_tel)

    # Read the binary file
    file_content = Path(file_path).read_bytes()

    idx = 0
    size_total = len(file_content)
    n_items = 0
    while idx < size_total:
        _map_data(
            struct_file_tel,
            file_content[idx : idx + size_file_tel],
            size_file_tel,
        )
        _put_data_point(data_file, struct_file_tel)

        # Index for the next iteration
        idx += size_file_tel

        # Update the number of data
        n_items += 1

        if (first_n_items is not None) and (n_items >= first_n_items):
            break

    print(f"Read {n_items} items of data.")

    if (idx != size_total) and (first_n_items is None):
        warnings.warn(
            "There is something wrong when reading the binary file. "
            f"The final index is {idx} and the total size of file is {size_total}.",
            category=UserWarning,
        )

    return data_file


def _get_default_data(c_struct_telemetry):
    """Get the default data of telemetry.

    Parameters
    ----------
    c_struct_telemetry : child class of ctypes.LittleEndianStructure
        Telemetry of the C structure.

    Returns
    -------
    data : dict
        Default data. The key is the field of C structure.
    """

    data = dict()
    for field in c_struct_telemetry._fields_:
        data[field[0]] = []

    return data


def _map_data(c_struct, data, count):
    """Map the data to C structure.

    Parameters
    ----------
    c_struct : child class of ctypes.LittleEndianStructure
        C structure.
    data : bytes
        Binary data.
    count : int
        Count bytes.
    """

    ctypes.memmove(ctypes.addressof(c_struct), data, count)


def _put_data_point(data, c_struct):
    """Put the data point.

    Parameters
    ----------
    data : dict
        Data.
    c_struct : child class of ctypes.LittleEndianStructure
        C structure.
    """

    for field in c_struct._fields_:
        field_name = field[0]
        value = _get_value(c_struct, field_name)
        data[field_name].append(value)


def _get_value(c_struct, field_name):
    """Get the value.

    Parameters
    ----------
    c_struct : child class of ctypes.LittleEndianStructure
        C structure.
    field_name : str
        Field name.

    Returns
    -------
    int, float, tuple, or list
        Value.
    """

    value = getattr(c_struct, field_name)
    try:
        size = len(value)
        return [_get_value_as_tuple_if_c_struct(value[idx]) for idx in range(size)]
    except TypeError:
        return _get_value_as_tuple_if_c_struct(value)


def _get_value_as_tuple_if_c_struct(input):
    """Get the value as tuple if the input is C structure.

    Parameters
    ----------
    input : int, float, or child class of ctypes.LittleEndianStructure
        Input.

    Returns
    -------
    int, float, or tuple
        value.
    """
    try:
        value = []
        for field in input._fields_:
            value.append(getattr(input, field[0]))

        return tuple(value)
    except AttributeError:
        return input
