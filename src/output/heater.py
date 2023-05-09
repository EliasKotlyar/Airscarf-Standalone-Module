from machine import Pin, ADC

from common.globalstate import state
import uasyncio
from machine import PWM
from common.logger import logger


class Heater:
    def setup(self):
        """
        Perform the setup for the Heater class.
        This method can be used to initialize any necessary resources or configurations.
        In this case, it sets up the PWM pin for controlling the heater output and retrieves the initial heater profile value.
        """
        self.PIN_HEATER_OUT = 22
        self.heater = PWM(Pin(self.PIN_HEATER_OUT))
        self.currentValue = state.getState('current_profile')
        pass

    async def run(self):
        """
        Run the Heater loop.
        Monitors changes in the heater profile and adjusts the heater output accordingly.
        The heater output is controlled using PWM signals based on the current heater profile.
        """
        while True:
            # Wait until the state changes (profile or settings have changed):
            await state.awaitStateChange()

            # Process Heater:
            current_profile = state.getState('current_profile')
            logger.info("Heater received Profile change to: " + str(current_profile))
            heater_duty = 0

            if current_profile == 0 or current_profile == -1:
                heater_freq = 0
            else:
                heater_freq = int(state.getState('heater_frequency'))
                if current_profile == 1:
                    heater_duty = int(state.getState('low_heater'))
                elif current_profile == 2:
                    heater_duty = int(state.getState('middle_heater'))
                elif current_profile == 3:
                    heater_duty = int(state.getState('high_heater'))

            heater_freq = int(heater_freq)
            logger.info("Heater changed to duty " + str(heater_freq) + " freq: " + str(heater_duty))

            if heater_freq < 8:
                heater_freq = 8

            self.heater.freq(heater_freq)
            self.heater.duty_u16(int(heater_duty))
