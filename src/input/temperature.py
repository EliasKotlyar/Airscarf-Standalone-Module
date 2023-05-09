import math

from machine import Pin, ADC
from common.globalstate import state
import uasyncio


class PcbTemperature:
    def setup(self):
        """
        Perform the setup for the PcbTemperature class.
        Initialize the pin number and create an ADC instance.
        """
        self.PIN_TEMPERATURE = 27
        self.adc = ADC(Pin(self.PIN_TEMPERATURE))
        state.setState('pcb_temperature', 0)

    async def run(self):
        """
        Run the PcbTemperature monitoring loop.
        Continuously reads the temperature from the ADC and updates the PCB temperature state.
        """
        while True:
            await uasyncio.sleep_ms(1000)
            temperature = self.adc.read_u16()
            state.setState('pcb_temperature', temperature)

    def convertValueToTemperature(self, val):
        """
        Convert the ADC value to temperature using the NTC characteristics.
        """
        ntcNominal = 10100  # Resistance of NTC at nominal temperature
        tempNominal = 25  # Temperature at which the NTC has the specified resistance
        bCoefficient = 4000  # Beta Coefficient (B25 from NTC datasheet)
        serienResistance = 10000  # Series Resistance in Ohm

        val = 65535 / val - 1
        val = serienResistance / val
        temp = val / ntcNominal  # (R/Ro)
        temp = math.log(temp)  # ln(R/Ro)
        temp /= bCoefficient  # 1/B * ln(R/Ro)
        temp += 1.0 / (tempNominal + 273.15)  # + (1/To)
        temp = 1.0 / temp  # Invert
        temp -= 273.15  # Convert to °C

        # String formatting:
        temp = round(temp, 2)
        temp = "{:10.2f}".format(temp)
        temp = str(temp) + " " + "C"
        return temp
