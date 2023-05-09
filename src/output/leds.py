from machine import Pin

from common.globalstate import state
import uasyncio
from common.logger import logger


class Leds:

    def setup(self):
        """
        Perform the setup for the Leds class.
        This method can be used to initialize any necessary resources or configurations.
        In this case, it sets up the LED pins, initializes their initial states, and sets the initial LED states in the global state.
        """
        self.OUT_LED1 = 10
        self.OUT_LED2 = 14
        self.OUT_LED3 = 15

        self.led_pins = []

        for pin in [self.OUT_LED1, self.OUT_LED2, self.OUT_LED3]:
            p = Pin(pin, Pin.OUT)
            p.off()  # Set the initial state to off
            self.led_pins.append(p)

        state.setState('led1', False)
        state.setState('led2', False)
        state.setState('led3', False)

    async def run(self):
        """
        Run the Leds loop.
        Monitors changes in the current profile and updates the states of the LEDs accordingly.
        The LEDs are controlled by setting the corresponding pin states based on the current profile.
        The LED states are also updated in the global state.
        """
        while True:
            # Wait until state has changed:
            await state.awaitStateChange()

            current_profile = state.getState('current_profile')
            logger.info("LED received Profile change to: " + str(current_profile))

            led1 = False
            led2 = False
            led3 = False

            if current_profile == 1:
                led1 = True
            elif current_profile == 2:
                led1 = True
                led2 = True
            elif current_profile == 3:
                led1 = True
                led2 = True
                led3 = True

            self.led_pins[0].value(led1)
            self.led_pins[1].value(led2)
            self.led_pins[2].value(led3)

            state.setState('led1', led1)
            state.setState('led2', led2)
            state.setState('led3', led3)

            stage = state.getState('current_profile')
