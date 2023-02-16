from ucollections import namedtuple
import ujson

"""
Config - Reads Config File into Dict Object

"""


class WlanConfig(dict):
    def getFields(self):
        return {
            "wifi_name": "str",
            "wifi_pass": "str",
            "wifi_mode": "int",
        }


class Profile(dict):
    def getFields(self):
        return {"rpm_freq": "int",
                "rpm_duty": "int",
                "heater_freq": "int",
                "heater_duty": "int",
                }


class Config(dict):
    def getFields(self):
        return {
            "current_profile": "int",
            "profile1": "Profile",
            "profile2": "Profile",
            "profile3": "Profile",
        }


class ConfigReader:
    '''
    Maps Attributes by Types:
    '''

    def mapAttributes(self, configObj, jsonObj):
        for attributeName, valueType in configObj.getFields().items():
            value = jsonObj[attributeName]
            if (valueType == "str"):
                value = str(value)
            elif (valueType == "int"):
                value = int(value)
            elif (valueType == "Profile"):
                profile = Profile()
                self.mapAttributes(profile, value)
                value = profile

            configObj[attributeName] = value

    '''
    Read Wlan Config
    '''

    def readWlanConfig(self):
        f = open('wifi.json')
        jsonObj = ujson.load(f)
        f.close()
        confData = WlanConfig()
        self.mapAttributes(confData, jsonObj)
        return confData

    '''
    Write Wlan Config
    '''

    def writeWlanConfig(self, config):
        f = open('wifi.json', "w")
        ujson.dump(config, f)
        f.close()
    '''
    Read Profiles Config
    '''

    def readProfiles(self):
        f = open('profiles.json')
        jsonObj = ujson.load(f)
        f.close()
        confData = Config()
        self.mapAttributes(confData, jsonObj)
        return confData

    '''
    Write Wlan Config
    '''

    def writeProfiles(self, config):
        f = open('profiles.json', "w")
        ujson.dump(config, f)
        f.close()
