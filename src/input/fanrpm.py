from machine import Pin, ADC

from common.globalstate import state
import uasyncio

from lib.pwmcounter import PWMCycleCounter
from common.logger import logger


class FanRpm:
    def setup(self):
        """
        Perform the setup for the FanRpm class.
        Initialize the pin numbers and create PWMCycleCounter instances.
        """
        self.waiting_time = 1000
        # Fan on 17 is fine
        self.PIN_FAN_RPM1 = 17
        # Fan on PIN 18
        self.PIN_FAN_RPM2 = 18

        self.fan1 = PWMCycleCounter(self.PIN_FAN_RPM1, self.waiting_time, 0)
        self.fan2 = PWMCycleCounter(self.PIN_FAN_RPM2, self.waiting_time, 1)

    async def run(self):
        """
        Run the FanRpm measurement loop.
        Continuously measures the RPM of the fans and updates the state.
        """
        while True:
            tasks = [
                self.fan1.run(),
                self.fan2.run()
            ]
            try:
                res = await uasyncio.gather(*tasks, return_exceptions=True)
                self.setRpm1(res[0])
                self.setRpm2(res[1])
            except uasyncio.TimeoutError:  # These only happen if return_exceptions is False
                logger.info("FANRPM: Timeout")
                pass
            except uasyncio.CancelledError:
                logger.info("FANRPM: Canceled")
                pass

    def calculate_rpm(self, counter, timeframe):
        """
        Calculate the RPM based on the counter and timeframe.
        Args:
            counter: The number of fan rotations counted.
            timeframe: The duration of the timeframe in milliseconds.
        Returns:
            The calculated RPM value.
        """
        rpm = (counter / (timeframe / 1000)) * 60
        return rpm

    def setRpm1(self, value):
        """
        Set the RPM value of fan 1 in the global state.
        Args:
            value: The RPM value to set.
        """
        state.setState('fan1_rpm', value)

    def setRpm2(self, value):
        """
        Set the RPM value of fan 2 in the global state.
        Args:
            value: The RPM value to set.
        """
        state.setState('fan2_rpm', value)
