# Rotator Analysis

This repository contains code for analyzing the performance of a rotator system with the high frequency telemetry data.

## Dependency

- Python >= 3.7.10

Use the `conda` or `pip` to install the followings:

- numpy
- matplotlib

## Setup the Environment

Under the repository directory, do:

```bash
export PYTHONPATH=${PYTHONPATH}:$(pwd)/python
```

## Log the Local Telemetry File


To log the high frequency telemetry data, you need to log in the rotator PXI controller with `ssh` command (the credential and IP are in the Rubin 1Password **MainTel** vault):

```bash
ssh -o "PubkeyAuthentication=no" ${account}@${ip}
```

Modify the **LOGTLM_FILE** to be 1 in the `/home/admin/github/ts_rotator_controller/configRotator/default.yaml`.
After enabling the rotator, the new value of `default.yaml` will be read.
The log files are in the `/home/admin/github/ts_rotator_controller/log/` directory.
If you do not need to log the file, put the **LOGTLM_FILE** back to be 0.
The logging frequency is 2000 Hz, and you need to avoid to fill all the disk space with the log files.
You can use the `scp` command to copy the log files to your host machine to analyze the data:

```bash
scp -o "PubkeyAuthentication=no" ${account}@${ip}:/home/admin/github/ts_rotator_controller/log/tlm* ${destination_path_in_host}
```

## Use of Python

To read the high frequency telemetry binary log file, do:

```python
from read_binary import read_binary
data_file = read_binary(path_to_binary_file, first_n_items=None)
```

The output is the data as dictionaries.
If the `first_n_items` is `None`, all items in file will be read.
Otherwise, the function will only read the first n items.

Note: The Python code is modified from [here](https://github.com/lsst-ts/ts_hexapod_gui/tree/develop/python).

## Data Analysis

To analyze the data, do:

```bash
python script/data_analysis.py path_to_file
```

To get more information, do:

```bash
python script/data_analysis.py -h
```

## Tune the Time Synchronization

See the details in [time_synchronization.md](./doc/time_synchronization.md).
