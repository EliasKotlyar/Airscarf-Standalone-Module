from machine import Pin, ADC

from common.globalstate import state
import uasyncio
from machine import PWM
from common.logger import logger


class Fan:
    def setup(self):
        """
        Perform the setup for the Fan class.
        This method can be used to initialize any necessary resources or configurations.
        In this case, it sets up the PWM pin for controlling the fan speed and retrieves the initial fan profile value.
        """
        self.PIN_FAN_OUT = 16
        self.fan = PWM(Pin(self.PIN_FAN_OUT))
        self.currentValue = state.getState('current_profile')
        pass

    async def run(self):
        """
        Run the Fan loop.
        Monitors changes in the fan profile and adjusts the fan speed accordingly.
        The fan speed is controlled using PWM signals based on the current fan profile.
        """
        while True:
            # Wait until the state changes (profile or settings have changed):
            await state.awaitStateChange()

            # Process Fan:
            current_profile = state.getState('current_profile')
            logger.info("Fan received Profile change to: " + str(current_profile))
            rpm_duty = 0

            if current_profile == 0 or current_profile == -1:
                rpm_freq = 0
            else:
                rpm_freq = int(state.getState('fan_frequency'))
                if current_profile == 1:
                    rpm_duty = int(state.getState('low_fan'))
                elif current_profile == 2:
                    rpm_duty = int(state.getState('middle_fan'))
                elif current_profile == 3:
                    rpm_duty = int(state.getState('high_fan'))

            rpm_freq = int(rpm_freq)
            logger.info("Fan changed to duty " + str(rpm_freq) + " freq: " + str(rpm_duty))

            if rpm_freq < 8:
                rpm_freq = 8

            self.fan.freq(rpm_freq)
            self.fan.duty_u16(int(rpm_duty))
