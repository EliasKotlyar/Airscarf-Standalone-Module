import uasyncio as asyncio
from machine import Pin, PWM
from rp2 import PIO, StateMachine, asm_pio

# Created using following Tutorial as Reference:
# https://dernulleffekt.de/doku.php?id=raspberrypipico:pico_pio
@asm_pio()
def pwm_counter():
    wrap_target()
    # Gets Values from main program into OSR
    pull(noblock)
    # Move value to y register
    mov(y, osr)
    # Label for indifenetly loop
    label("loop")
    # Wait for low:
    wait(0, pin, 0)
    # Wait for high:
    wait(1, pin, 0)
    # Decrement Y , jmp to next instruction
    jmp(y_dec, "loop")

    wrap()


class PWMCycleCounter:
    def __init__(self, pin, waiting_time,state_machine_nr):
        self.waiting_time = waiting_time
        # Set Pin to IN
        Pin(pin, Pin.IN)
        PIO(state_machine_nr).remove_program()
        # Init State Machine:
        self._sm = StateMachine(state_machine_nr, pwm_counter, freq=1000000, in_base=Pin(pin))

    async def run(self):
        self._sm.restart()
        original_value = 0xFFFFFFFF
        # Put value into FIFO
        self._sm.put(original_value)
        # Activate State Machine
        self._sm.active(1)
        # Wait 1 second, do other tasks:
        # print("waiting for 1 second")
        await asyncio.sleep_ms(self.waiting_time)
        # print("waiting for 1 done")
        # Deactivate State Machine
        self._sm.active(0)
        # Put value of y into OSR
        self._sm.exec("mov(isr, y)")
        # Push value to FIFO
        self._sm.exec("push()")
        new_value = self._sm.get()
        calc_value = original_value - new_value
        return calc_value
