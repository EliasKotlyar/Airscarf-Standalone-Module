"""
Temperature sensor Calculation
"""
import math


# http://www.scynd.de/tutorials/arduino-tutorials/5-sensoren/5-1-temperatur-mit-10k%CF%89-ntc.html
class Tempsensor:

    def convertValueToTemperature(self, val):
        ntcNominal = 10100  # Wiederstand des NTC bei Nominaltemperatur
        tempNominal = 25  # Temperatur bei der der NTC den angegebenen Wiederstand hat
        bCoefficient = 4000  # Beta Coefficient(B25 aus Datenblatt des NTC)
        serienResistance = 10000  # Series Resistance in Ohm
        val = 65535 / val - 1
        val = serienResistance / val
        temp = val / ntcNominal  # (R/Ro)
        temp = math.log(temp)  # ln(R/Ro)
        temp /= bCoefficient  # 1/B * ln(R/Ro)
        temp += 1.0 / (tempNominal + 273.15)  # + (1/To)
        temp = 1.0 / temp  # Invertieren
        temp -= 273.15  # Umwandeln in °C
        # String formatting:
        temp = round(temp, 2)
        temp = "{:10.2f}".format(temp)
        temp = str(temp) + " " + "C"
        return temp
