from config import ConfigReader
from airscarf_webserver import Webserver
from airscarf_hardware import AirScarf
from wlan import Wlan
import gc
import uasyncio

gc.collect()
reader = ConfigReader()
wlan = Wlan(reader)
airscarf = AirScarf(reader)
webserver = Webserver(airscarf, reader)
webserver.start()


