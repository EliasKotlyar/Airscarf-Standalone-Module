PIN_FAN_RPM1 = 17
PIN_FAN_RPM2 = 18
PIN_FAN_OUT = 16
PIN_HEATER_CURRENT = 28
PIN_TEMPERATUR = 27
PIN_SUPPLY = 26
from machine import ADC, Pin, PWM
class AirScarf:
    def __init__(self):
        self.heaterCurrent = ADC(Pin(PIN_HEATER_CURRENT))
        self.temperatur = ADC(Pin(PIN_TEMPERATUR))
        self.supply = ADC(Pin(PIN_SUPPLY))

        #self.rpm1 = ADC(Pin(PIN_FAN_RPM1))
        #self.rpm2 = ADC(Pin(PIN_FAN_RPM2))
        pass
    def setRpm(self, freq,duty):
        pwm0 = PWM(Pin(22))
        pwm0.freq(freq)
        pwm0.duty_u16(duty)
    def getData(self):
        return {
            "heaterCurrent": self.heaterCurrent.read_u16(),
            "temperatur": self.temperatur.read_u16(),
            "supply": self.supply.read_u16()
        }