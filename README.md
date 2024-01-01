# Mibox Socket

The Xiaomi Mibox socket is a simple integration for Home Assistant that turns ON the Mibox without requiring the remote control. It uses the `bluetoothctl` tool as the base pairing method wrapped in the `Pexpect` spawning module.

## Hardware
It utilizes the default built-in Bluetooth device on the RPI4 to connect to the Xiaomi Mibox. It has not been tested with BT dongles.

## Why
While turning the Mibox off can be done easily with an ADB command, turning it ON is only possible with the remote control, because device goes into deep sleep. This component addresses this limitation by using the `bluetoothctl` `bluetooth pair` command. Note that this is still just a workaround.

## How
Before using the Mibox Socket HA integration, ensure that your RPI is not already paired with the Mibox. If it is, unpair it on the Mibox device itself. `Bluetoothctl` is used because it needs to scan for devices first. Once the device is found, the `pair` process can be called. The `Pexpect` module is used to ensure the sequence is followed in order. It takes about 15 secons to complete the sequence and to wake up Mibox.

## Home Assistant Setup
1. Copy the content to the `custom_components` directory.
2. In the `configuration.yaml` file, enter:

    ```yaml
    switch:
      - platform: mibox_socket
        device:
          mac: "XX:XX:XX:XX:XX:XX"
    ```

3. Replace "XX:XX:XX:XX:XX:XX" with the Bluetooth MAC of the Mibox.
4. Restart Home Assistant.
5. The component will create a `switch.mibox_socket_switch` entity. Use it to turn your Mibox ON.
