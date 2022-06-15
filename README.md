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
    ```python
    argparse, os, re, dotenv, pexpect, random, string
    ```

## Execute the script
1. Configure environment variables

    Follow README of the script to set up environment variables.

2. Execute the script to configure APs

    Follow the execution instruction in README of the script, and make sure those APs are already resetted before execution. Note that the script will record the IP addresses of configured AP in file `ap_list`.

3. Execute the script to configures RADIUS server

    Follow the execution instruction in README of the script, and make sure that all configured AP IP addresses are in file `ap_list` before execution.

## After Recovery of Zonedirector
1. Execute the script to configure APs

    Follow the execution instruction in README of the script. *No* need to reset APs and onsite access to AP is *not* required in this part. Make sure file `ap_list` contains all AP's IP addresses, including those APs that does not reset, before execution.
    - `ap_list` should content 'ip', 'passwd', 'secret', 'name'
    - Execute `return_zd.py` with the ap list name, for example: `python return_zd.py ap_list.csv`
    - Every AP in `ap_list` will connect to zd again 
    
2. Execute the script to configure RADIUS server

    Follow the execution instruction in README of the script. Make sure the info of RADIUS servers are correct before execution.

## Troubleshooting
1. To access AP after executing the script on any AP, make sure the laptop is set under VLAN 4 (Linux and MacOS are suggested). Then we should be able to access the AP by its IP address, via ssh CLI or https GUI, to troubleshoot.

2. If the laptop cannot ping `192.168.0.1` after reset, it might be due to that the reseting of AP isn't finished yet or the reset isn't successful. Try to ping again in a few minutes, or reset again if it is still not working. The expected outcome after pressing reset hole for at least 8 seconds is a solid red PWR light, and then blinking green PWR light.
