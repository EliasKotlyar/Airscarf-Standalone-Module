from machine import Pin

from common.globalstate import state
import uasyncio


class CurrentSupplyMonitoring:

    def setup(self):
        """
        Perform the setup for the CurrentSupplyMonitoring class.
        This method can be used to initialize any necessary resources or configurations.
        In this case, the method is empty.
        """
        pass

    async def run(self):
        """
        Run the CurrentSupplyMonitoring loop.
        Continuously monitors the current supply and checks if it falls below the threshold.
        If the current supply is lower than the threshold, set the current profile to -1 and log an error.
        """
        # Wait 5 seconds to let it boot up
        await uasyncio.sleep_ms(5000)

        while True:
            diagnose_delay = int(state.getState("diagnose_delay_supply_current"))
            await uasyncio.sleep_ms(diagnose_delay)
            current_profile = state.getState('current_profile')

            if current_profile == -1:
                continue

            current_value = state.getState("current_supply")
            threshold_value = int(state.getState("monitoring_supply_current"))

            # If voltage is lower than setting, go to error:
            if current_value < threshold_value:
                state.setCurrentProfile(-1)
                state.setState('error', "VCC Supply Current too low to operate")
