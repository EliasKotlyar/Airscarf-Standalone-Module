"""
wlan
--------
Based on https://github.com/monkmakes/mm_wlan
"""

import network, time
from common.logger import logger
from common.globalstate import state


class Wlan:
    def setup(self):
        """
        Perform the setup for the Wlan class.
        This method can be used to initialize any necessary resources or configurations.
        In this case, it does not require any specific setup.
        """
        pass

    async def run(self):
        """
        Run the Wlan loop.
        Depending on the configured mode (AP or STA), it creates an access point or connects to a Wi-Fi network.
        The Wi-Fi configuration parameters are obtained from the global state.
        If the mode is AP, it configures and activates the access point.
        If the mode is STA, it connects to the specified Wi-Fi network using the provided credentials.
        It waits for a successful connection or retries for a limited number of attempts.
        After a successful connection, it logs the IP address obtained.
        """
        logger.info('Creating AP')
        wifi_name = state.getState('wifi_name')
        wifi_mode = state.getState('wifi_mode')
        wifi_pass = state.getState('wifi_pass')

        mode = network.STA_IF
        if wifi_mode == 0:
            mode = network.AP_IF
            logger.info('Creating AP ' + wifi_name)
        elif wifi_mode == 1:
            logger.info('Connecting to WiFi: ' + wifi_name + " using password " + wifi_pass)

        wlan = network.WLAN(mode)

        if mode == network.AP_IF:
            wlan.config(essid=wifi_name)
            wlan.config(password=wifi_pass)
            wlan.config(pm=0xa11140)
            wlan.active(True)

            while not wlan.active():
                pass

            logger.info("WIFI Point active")
            logger.info(wlan.ifconfig())

        elif mode == network.STA_IF:
            wlan.active(True)
            wlan.config(pm=0xa11140)  # Disable power-save mode
            wlan.connect(wifi_name, wifi_pass)

            retries = 10
            while retries > 0 and wlan.status() != network.STAT_GOT_IP:
                retries -= 1
                logger.info('.')
                time.sleep(1)

            if wlan.status() != network.STAT_GOT_IP:
                logger.info('\nConnection failed. Check SSID and password')
                raise RuntimeError('WLAN connection failed')
            else:
                logger.info('\nConnected. IP Address = ' + wlan.ifconfig()[0])
