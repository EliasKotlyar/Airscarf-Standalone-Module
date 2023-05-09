from machine import Pin

from common.globalstate import state
import uasyncio

from common.logger import logger


class Switch:

    def setup(self):
        """
        Perform the setup for the Switch class.
        Initialize the pin number and create a Pin instance.
        """
        self.IN_SWITCH = 21
        self.switch_pin = Pin(self.IN_SWITCH, Pin.IN)
        self.previous_state = 0
        state.setState('switch', False)

    async def run(self):
        """
        Run the Switch monitoring loop.
        Continuously monitors the state of the switch and performs actions based on changes.
        """
        while True:
            current_state = self.switch_pin.value()
            await uasyncio.sleep_ms(20)

            # Read the pin state again after a short delay
            debounced_state = self.switch_pin.value()

            if current_state != debounced_state:
                # Wait for another short delay to ensure stable state
                await uasyncio.sleep_ms(20)

                # Read the pin state again
                final_state = self.switch_pin.value()

                if debounced_state == final_state and final_state == True:
                    logger.info("Switch triggered. Switching Profile.")
                    # The pin state has stabilized, perform the desired actions
                    state.setState('switch', True)
                    current_profile = state.getState('current_profile')

                    if current_profile == -1:
                        state.setCurrentProfile(1)
                    if current_profile == 0:
                            state.setCurrentProfile(1)
                    if current_profile == 1:
                        state.setCurrentProfile(2)
                    elif current_profile == 2:
                        state.setCurrentProfile(3)
                    elif current_profile == 3:
                        state.setCurrentProfile(0)
                else:
                    state.setState('switch', False)

            self.previous_state = debounced_state
