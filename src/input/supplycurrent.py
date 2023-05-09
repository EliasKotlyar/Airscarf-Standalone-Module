from machine import Pin, ADC

from common.globalstate import state
import uasyncio


class SupplyCurrent:

    def setup(self):
        """
        Perform the setup for the SupplyCurrent class.
        Initialize the pin number and create an ADC instance.
        """
        self.PIN_SUPPLY_CURRENT = 26
        self.supply_adc = ADC(Pin(self.PIN_SUPPLY_CURRENT))
        self.setValue(0)

    async def run(self):
        """
        Run the SupplyCurrent measurement loop.
        Continuously measures the current value of the supply and updates the state.
        """
        while True:
            await uasyncio.sleep_ms(500)
            supply_adc = self.supply_adc.read_u16()
            self.setValue(supply_adc)

    def setValue(self, value):
        """
        Set the current value of the supply in the global state.
        Args:
            value: The current value to set.
        """
        state.setState('current_supply', value)
