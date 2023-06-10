import gc
import uasyncio
from config.advanced import AdvancedConfig
from config.profiles import ProfilesConfig
from config.wifi import WifiConfig
from input.switch import Switch
from input.fanrpm import FanRpm
from input.heatercurrent import HeaterCurrent
from input.supplycurrent import SupplyCurrent
from input.temperature import PcbTemperature
from monitoring.current_supply import CurrentSupplyMonitoring
from monitoring.heater_supply import HeaterSupplyMonitoring
from monitoring.rpmmonitoring import RpmMonitoring
from output.fan import Fan
from output.heater import Heater
from output.leds import Leds
from processes.wlan import Wlan
from processes.webserver import Webserver
from common.logger import logger
from common.globalstate import state
from processes.dns import Dns
import uasyncio
gc.collect()
uasyncio.new_event_loop()
logger.info("Starting Application!")
# Startup:

logger.info("Reading Config...")
# Init Configuration files:
configClasses = [AdvancedConfig, ProfilesConfig, WifiConfig]
for configClass in configClasses:
    configObj = configClass()
    config = configObj.read_config()
    state.addState(config)
# Set Profile to 0
state.setState("current_profile", 0)

logger.info("Reading Config completed!")
logger.info("Starting Background Tasks!")
# Start initing all the Background Processes:
processClasses = [
    # Inputs:
    PcbTemperature,
    Switch,
    FanRpm,
    HeaterCurrent,
    SupplyCurrent,
    # Outputs:
    Leds,
    Fan,
    Heater,
    # Monitorings:
    HeaterSupplyMonitoring,
    CurrentSupplyMonitoring,
    RpmMonitoring,

]
for processClass in processClasses:
    process = processClass()
    process.setup()
    uasyncio.create_task(process.run())


loop = uasyncio.get_event_loop()
wlan = Wlan()
loop.run_until_complete(wlan.run())
wlan = Dns()
loop.run_until_complete(wlan.run())

webserver = Webserver()
webserver.start()
