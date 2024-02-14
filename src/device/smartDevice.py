from typing import Callable
from functools import partial
import json

class SmartDevice:
    DEVICE_ID_COUNTER:int = 0
    def __init__(self):
        self.properties:dict[str, DeviceProperty] = {}
        self.properties['shDeviceType'] = DeviceProperty('shDeviceType')
        self.properties['deviceId'] = self.deviceId =  DeviceProperty('deviceId')
        self.properties['ipAddress'] = self.ipAddress = DeviceProperty('ipAddress')

        self.properties['shDeviceType'].value = self.__class__.__name__
        self.properties['deviceId'].value = SmartDevice.DEVICE_ID_COUNTER
        SmartDevice.DEVICE_ID_COUNTER += 1

    def __str__(self) -> str:
        return str(self.properties)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def addListener(self, property:str, callback:Callable):
        self.properties[property].addListener(callback=callback)
    
class SmartDeviceJsonEncoder(json.JSONEncoder):
    def default(self, o:SmartDevice):
        tmp:dict = {}
        for key in o.properties.keys():
            targetVal = o.properties[key].value
            if isinstance(targetVal, bool):
                targetVal = 'true' if targetVal == True else 'false'
            elif targetVal is None:
                targetVal = 'null'
            tmp[key] = targetVal
        return tmp

class DeviceProperty:
    def __init__(self, name):
        self.name = name
        self.value = None
        self.propertyListeners:list[Callable] = []

    def __str__(self):
        if isinstance(self.value, str):
            return f"'{self.value}'"
        if isinstance(self.value, bool):
            return f"{self.value}".lower()
        return f"{self.value}"
    
    __repr__ = __str__

    def set(self, value):
        prevVal = self.value
        self.value = value
        if self.value is not None and self.value != prevVal:
            for listener in self.propertyListeners:
                partial(listener, self)()

    def addListener(self, callback:Callable):
        self.propertyListeners.append(callback)
