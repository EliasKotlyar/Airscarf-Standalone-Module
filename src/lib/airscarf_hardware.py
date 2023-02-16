PIN_FAN_RPM1 = 17
PIN_FAN_RPM2 = 18
PIN_FAN_OUT = 16
PIN_HEATER_CURRENT = 28
PIN_TEMPERATUR = 27
PIN_SUPPLY = 26
OUT_HEATER_PWM = 22
IN_SWITCH = 21
OUT_LED1 = 10
OUT_LED2 = 14
OUT_LED3 = 15
import uasyncio
from machine import ADC, Pin, PWM
from tempsensor import Tempsensor



class AirScarf:
    def __init__(self, configReader):
        self.configReader = configReader
        self.heaterCurrent = ADC(Pin(PIN_HEATER_CURRENT))
        self.temperatur = ADC(Pin(PIN_TEMPERATUR))
        self.supply = ADC(Pin(PIN_SUPPLY))
        self.fan = PWM(Pin(PIN_FAN_OUT))
        self.fan.duty_u16(0)
        self.heater = PWM(Pin(OUT_HEATER_PWM))
        self.heater.duty_u16(0)
        self.led1 = Pin(OUT_LED1, Pin.OUT, value=0)
        self.led2 = Pin(OUT_LED2, Pin.OUT, value=0)
        self.led3 = Pin(OUT_LED3, Pin.OUT, value=0)
        self.switch = Pin(IN_SWITCH, Pin.IN)
        # self.rpm1 = ADC(Pin(PIN_FAN_RPM1))
        # self.rpm2 = ADC(Pin(PIN_FAN_RPM2))
        uasyncio.create_task(self.backgroundProcess())
        self.reload()
        pass

    def reload(self):
        config = self.configReader.readProfiles()
        currentProfileNumber = config.get('current_profile')
        if (currentProfileNumber > 3):
            currentProfileNumber = 0
        print("Profile Nr " + str(currentProfileNumber) + " selected:")
        self.setLedValue(currentProfileNumber)
        if (currentProfileNumber == 0):
            currentProfile = {'rpm_freq': 0, 'rpm_duty': 0, 'heater_freq': 0, 'heater_duty': 0}
            self.setValues(currentProfile)
        else:
            currentProfile = config.get("profile" + str(currentProfileNumber))
            self.setValues(currentProfile)

    def nextProfile(self):
        config = self.configReader.readProfiles()
        currentProfileNumber = int(config.get('current_profile'))
        currentProfileNumber += 1
        if (currentProfileNumber > 3):
            currentProfileNumber = 0
        config['current_profile'] = currentProfileNumber
        # print(config)
        self.configReader.writeProfiles(config)
        self.reload()

    def setValues(self, profile):
        print("Setting values to:")
        print(profile)
        rpm_freq = profile.get('rpm_freq')
        rpm_duty = profile.get('rpm_duty')
        rpm_freq = int(rpm_freq)
        if (rpm_freq < 8):
            rpm_freq = 8
        self.fan.freq(rpm_freq)
        self.fan.duty_u16(int(rpm_duty))
        # Heater Freq:
        heater_freq = profile.get('heater_freq')
        heater_duty = profile.get('heater_duty')
        heater_freq = int(heater_freq)
        if (heater_freq < 8):
            heater_freq = 8
        self.heater.freq(heater_freq)
        self.heater.duty_u16(int(heater_duty))

    def getLiveData(self):
        heater_current_raw = self.heaterCurrent.read_u16()
        temperature_raw = self.temperatur.read_u16()
        supply_voltage_raw = self.supply.read_u16()
        heater_current_value = self.convertValueToVolt(heater_current_raw)
        sensor = Tempsensor()
        temperature_value = sensor.convertValueToTemperature(temperature_raw)
        supply_voltage_value = self.convertValueToVolt(supply_voltage_raw)
        return {
            # Original Values:
            "rpm_freq": self.fan.freq(),
            "rpm_duty": self.fan.duty_u16(),
            "heater_freq": self.heater.freq(),
            "heater_duty": self.heater.duty_u16(),

            "heater_current_raw": heater_current_raw,
            "heater_current_value": heater_current_value,

            "temperature_raw": temperature_raw,
            "temperature_value": temperature_value,

            "supply_voltage_raw": supply_voltage_raw,
            "supply_voltage_value": supply_voltage_value,

        }

    def convertValueToVolt(self, val):
        val = val * (3.3 / 65535)
        val = round(val, 2)
        val = "{:10.2f}".format(val)
        val = str(val) + " " + "V"
        return val

    def setLedValue(self, value):
        self.led1.off()
        self.led2.off()
        self.led3.off()
        if (value == 1):
            self.led1.on()
        elif (value == 2):
            self.led2.on()
        elif (value == 3):
            self.led3.on()
        pass

    async def backgroundProcess(self):
        oldValue = self.switch.value()
        while True:
            await uasyncio.sleep_ms(300)
            newValue = self.switch.value()
            if (oldValue != newValue):
                if (newValue == 1):
                    print("Switch clicked!")
                    self.nextProfile()
                pass
            oldValue = newValue
