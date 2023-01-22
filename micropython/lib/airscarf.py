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
        self.fan = PWM(Pin(PIN_FAN_OUT))
        #self.rpm1 = ADC(Pin(PIN_FAN_RPM1))
        #self.rpm2 = ADC(Pin(PIN_FAN_RPM2))
        pass
    def setRpm(self, freq,duty):
        self.fan.freq(freq)
        self.fan.duty_u16(duty)

    def getData(self):
        return {
            "heaterCurrent": self.heaterCurrent.read_u16(),
            "temperatur": self.temperatur.read_u16(),
            "supply": self.supply.read_u16()
            "fan_freq" : self.fan.freq()
            "fan_duty" : self.fan.duty_u16()
        }
