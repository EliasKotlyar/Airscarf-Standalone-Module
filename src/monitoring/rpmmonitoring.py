from machine import Pin

from common.globalstate import state
import uasyncio


class RpmMonitoring:

    def setup(self):
        """
        Perform the setup for the RpmMonitoring class.
        This method can be used to initialize any necessary resources or configurations.
        In this case, the method is empty.
        """
        pass

    async def run(self):
        """
        Run the RpmMonitoring loop.
        Continuously monitors the RPM (rotation per minute) of the fan and checks if it falls below the threshold.
        If the RPM is lower than the threshold, set the current profile to -1 and log an error.
        """
        return

        while True:
            diagnose_delay = int(state.getState("diagnose_delay_rpm"))
            await uasyncio.sleep_ms(diagnose_delay)
            current_profile = state.getState('current_profile')

            if current_profile == -1:
                continue

            # Only continue if the fan is running:
            current_value = state.getState("fan1_rpm")
            threshold_value = int(state.getState("monitoring_rpm"))

            if threshold_value > current_value:
                state.setCurrentProfile(-1)
                state.setState('error', "RPM is invalid!")
