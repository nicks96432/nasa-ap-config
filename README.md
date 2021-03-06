# SOP for Setting Up Standalone AP when ZD is not working properly

Since APs are currently controlled by the only Zonedirector, when Zonedirector controler is out-of-order, it might cause all APs to not work properly as well and cannot connect to RADIUS server. This SOP provides a step-by-step instruction to make APs work in standalone-mode (each with its own SSID) even when Zonedirector is not out-of-order, and still have the capability to individually connect to RADIUS server. And we also provide another procedure and script to restore APs back to controller mode and connect them to the new or fixed Zonedirector.

## Preliminary

1. Decide which APs to configure

    Choose some of the APs in the building and visit each APs. This SOP requires onsite access to each APs to be configured.

2. Reset APs

    Reset APs using software reset(enter AP GUI or CLI to reset it) or hardware reset(by injecting pins into reset hole on AP for at least 8 seconds) and wait until it's done.

3. Set up static IP for laptop

    Set the IP address of laptop to any static address under `192.168.0.x` (except for `192.168.0.1`, which is IP address of the resetted AP), mask `255.255.255.0`.

4. Connect AP to laptop

    Use any ethernet cable to connect the AP to be set up to the laptop, and make sure the laptop can `ping 192.168.0.1`.

5. Required Python packages

    Our script requires following Python packages, please make sure they are available:

    ```text
    dotenv, pexpect
    ```

## Execute the script

1. Configure environment variables

    Follow `.env.example` to set up environment variables in file `.env`.

2. Execute the script to configure APs

    Make sure those APs are already resetted before execution. Note that the script will record the name, IP addresses, super user password and radius secret of configured AP in file `ap_list.csv`.

    Run the script:

    ```console
    python3 wifi.py <devie_name> <identifier>
    ```

    The identifier argument is the last 3 digits of product number, and the suggested device name is the location (e.g. r217) of the AP.

3. Execute the script to configures RADIUS server

    Make sure that all configured AP info are in file `ap_list.csv` and the info of RADIUS servers are correct before execution.

    Run the script:

    ```console
    python3 radius_set.py
    ```

## After Recovery of Zonedirector

1. Execute the script to configure APs

    *No* need to reset APs and onsite access to AP is *not* required in this part. Make sure file `ap_list.csv` contains all AP's information, including those APs that does not reset, before execution.

    Run the script:

    ```console
    python3 return_zd.py ap_list.csv
    ```

2. Execute the script to configure RADIUS server

    Make sure the info of RADIUS servers are correct before execution.

    Run the script:

    ```console
    python3 radius_return.py
    ```

## Troubleshooting

1. To access AP after executing the script on any AP, make sure the laptop is set under VLAN 4 (Linux and MacOS are suggested). Then we should be able to access the AP by its IP address, via ssh CLI or https GUI, to troubleshoot.

2. If the laptop cannot ping `192.168.0.1` after reset, it might be due to that the reseting of AP isn't finished yet or the reset isn't successful. Try to ping again in a few minutes, or reset again if it is still not working. The expected outcome after pressing reset hole for at least 8 seconds is a solid red PWR light, and then blinking green PWR light.
