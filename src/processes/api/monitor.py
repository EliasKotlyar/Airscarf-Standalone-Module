from common.globalstate import state
from lib.microdot_asyncio import Microdot

api_monitor = Microdot()


@api_monitor.get('/data.json')
def get_orders(request):
    return {
        "current_heater": format_to_volt(state.getState("current_heater")),
        "current_supply": format_to_volt(state.getState("current_supply")),
        "monitoring_rpm": state.getState("monitoring_rpm"),
        "fan1_rpm": state.getState("fan1_rpm"),
        "fan2_rpm": state.getState("fan2_rpm"),
        "pcb_temperature": format_to_volt(state.getState("pcb_temperature")),
        "switch": state.getState("switch"),
        "led1": state.getState("led1"),
        "led2": state.getState("led2"),
        "led3": state.getState("led3")
    }


def format_to_volt(raw_value):
    volt = raw_value * (3.3 / 65535)
    volt = round(volt, 2)
    volt = "{:.2f}".format(volt)
    ret_value = str(volt) + " " + "V (RAW-Value:" + str(raw_value) + ")"
    return ret_value
