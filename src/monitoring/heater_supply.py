from machine import Pin

from common.globalstate import state
import uasyncio


class HeaterSupplyMonitoring:

    def setup(self):
        """
        Perform the setup for the HeaterSupplyMonitoring class.
        This method can be used to initialize any necessary resources or configurations.
        In this case, the method is empty.
        """
        pass

    async def run(self):
        """
        Run the HeaterSupplyMonitoring loop.
        Continuously monitors the heater supply current and checks if it exceeds the threshold.
        If the heater supply current is higher than the threshold, set the current profile to -1 and log an error.
        """
        return

        while True:
            diagnose_delay = int(state.getState("diagnose_delay_heater_current"))
            await uasyncio.sleep_ms(diagnose_delay)
            current_profile = state.getState('current_profile')

            if current_profile == -1:
                continue

            current_value = state.getState("current_heater")
            threshold_value = int(state.getState("monitoring_heater_current"))

            # If voltage is bigger than setting, go to error:
            if current_value > threshold_value:
                state.setCurrentProfile(-1)
                state.setState('error', "Heater Supply too high!")
