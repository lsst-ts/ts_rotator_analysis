# Time Synchronization

At each time of assigning the new reference distribution clock (**REF_CLOCK_SLAVE** in `default.yaml`) or resetting the hardwares, it is **REQUIRED** to collect the high frequency telemetry data (use **LOGTLM_FILE: 1** in `default.yaml`) and use the [data_analysis.py](../script/data_analysis.py) to check the application loop time and reference clock time is closed to the  **LOOP_FREQUENCY_HZ** (2000 Hz is 500000 ns) in [sys.c](https://github.com/lsst-ts/ts_rotator_controller/blob/develop/src/sys.c) or not (the difference needs to be less than 1 ns).
Usually it will not and we need to adjust the value of **OFFSET_TIME_CONTROL_LOOP_NS** in `default.yaml`.

When collecting the high frequency telemetry data here, you only need to enable the system and collect 30 sec data (after this, disable the system to stop the logging of data).
If you do not see the pre-loading current after enabling the system, the restart of the control system and EtherCAT master would be required (by `/etc/init.d/rotator` and `/etc/init.d/ethercat`).
In this case, you would need to check the EtherCAT to be stable (see the **Tx frame rate [1/s]** to have the values of around 70 or lower when doing the `ethercat master`) before running the control application.
You will need to wait 5-10 minutes for this.

To stop the rotator, do:

```bash
/etc/init.d/rotator stop
```

To start the rotator, do:

```bash
/etc/init.d/rotator start
```

The control of EtherCAT master is the same as above except replace `rotator` with `ethercat` in the above commands.
It is noted that the `rotator` system can only run when the `ethercat` master is running and stable already.

Adjust the value of **OFFSET_TIME_CONTROL_LOOP_NS** in `default.yaml` when needed.
This will need to set the **UPDATE_OFFSET_TIME_CONTROL_LOOP_MANUALLY** value to be 1 as well (after the tuning, put this value back to 0).
For example, the following output of `data_analysis.py` has the good time synchronization (close to 500000 ns = 2k Hz by less than 1 ns):

```text
The delta processed reference clock time is:
mean = 499999.9898566895 ns
std = 1416.9839377781752 ns
The delta application time is:
mean = 499999.99614956917 ns
std = 236.99459219406006 ns
```

But the following needs to be tuned (> 1 ns):

```text
The delta processed reference clock time is:
mean = 499998.9898566895 ns
std = 1416.9839377781752 ns
The delta application time is:
mean = 499998.99614956917 ns
std = 236.99459219406006 ns
```

In this case, since the difference is `499998.989 - 500000 ~ -1`, the new **OFFSET_TIME_CONTROL_LOOP_NS** will be: **OFFSET_TIME_CONTROL_LOOP_NS** + 1.
After the adjustment, re-enable the control system (**Standby** -> **Enabled**) to read the configuration file.
You can check the high frequency telemetry data again to confirm the calculation and time synchronization.
You might need to do this for several times.
After the adjustments are done, you need to put **LOGTLM_FILE** to be 0 in `default.yaml` and re-enable the control system to load it to avoid the aggregated telemetry files to fill all the available disk space.

Usually the time synchronization can be persistent if you only restart the control system or EtherCAT master, but it is good for you to use the high frequency telemetry data to check the time synchronization to confirm it at each time before using the rotator.
