import uasyncio as asyncio
from machine import Pin, PWM
from rp2 import PIO, StateMachine, asm_pio

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
    async def run(self):
        input_pin = 18
        Pin(input_pin, Pin.IN)
        fan = PWM(Pin(16))
        fan.freq(1000)
        fan.duty_u16(int(2000))

        #self.pin = pin
        self._sm = StateMachine(0, pwm_counter, freq=1000000, in_base=Pin(input_pin))
        original_value =0xFFFFFFFF
        # Put value into FIFO
        self._sm.put(original_value)
        # Activate State Machine
        self._sm.active(1)
        # Wait 1 second, do other tasks:
        print("waiting for 1 second")
        await asyncio.sleep(1)
        print("waiting for 1 done")
        # Deactivate State Machine
        self._sm.active(0)
        # Put value of y into OSR
        self._sm.exec("mov(isr, y)")
        # Push value to FIFO
        self._sm.exec("push()")
        new_value = self._sm.get()
        print(original_value)
        print(new_value)
        print(original_value-new_value)

        fan.duty_u16(int(0))



async def main():
    counter = PWMCycleCounter()
    await counter.run()





loop = asyncio.get_event_loop()
loop.run_until_complete(main())
