from machine import Pin, ADC

from common.globalstate import state
import uasyncio


class HeaterCurrent:

    def setup(self):
        """
        Perform the setup for the HeaterCurrent class.
        Initialize the pin number and create an ADC instance.
        """
        self.PIN_HEATER_CURRENT = 28
        self.heater_adc = ADC(Pin(self.PIN_HEATER_CURRENT))
        self.setValue(0)

    async def run(self):
        """
        Run the HeaterCurrent measurement loop.
        Continuously measures the current value of the heater and updates the state.
        """
        while True:
            await uasyncio.sleep_ms(500)
            heaterAdc = self.heater_adc.read_u16()
            self.setValue(heaterAdc)

    def setValue(self, value):
        """
        Set the current value of the heater in the global state.
        Args:
            value: The current value to set.
        """
        state.setState('current_heater', value)
