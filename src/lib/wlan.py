"""
wlan
--------
Based on https://github.com/monkmakes/mm_wlan

"""

import network, time


class Wlan:
    def __init__(self, configReader):
        config = configReader.readWlanConfig()
        print("Wifi Config:")
        print(config)
        self.configureByConfig(config)

    def configureByConfig(self, config):
        verbose = True
        if (config.get("wifi_mode") == 0):
            mode = network.AP_IF
        elif (config.get("wifi_mode") == 1):
            mode = network.STA_IF
        wlan = network.WLAN(mode)
        if (mode == network.AP_IF):

            wlan.config(essid=config.get("wifi_name"))
            wlan.config(password=config.get("wifi_pass"))
            wlan.config(pm=0xa11140)
            wlan.active(True)
            while wlan.active() == False:
                pass
            print("WIFI Point active")
            print(wlan.ifconfig())
        elif (mode == network.STA_IF):
            wlan.active(True)
            wlan.config(pm=0xa11140)  # Disable power-save mode
            wlan.connect(config.get("wifi_name"), config.get("wifi_pass"))
            if verbose: print('Connecting to ' + config.get("wifi_name"), end=' ')
            retries = 0
            while retries > 0 and wlan.status() != network.STAT_GOT_IP:
                retries -= 1
                if verbose: print('.', end='')
                time.sleep(1)

            if wlan.status() != network.STAT_GOT_IP:
                if verbose: print('\nConnection failed. Check ssid and password')
                raise RuntimeError('WLAN connection failed')
            else:
                if verbose:
                    print('\nConnected. IP Address = ' + wlan.ifconfig()[0])
