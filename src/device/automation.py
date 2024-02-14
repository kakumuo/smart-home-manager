import json
import threading
from functools import partial
import time

from device.smartDevice import DeviceProperty, SmartDevice


class SmartHomeAutomation:
    SH_AUTO_ID:int = 0

    def __init__(self, name:str, deviceList:list[SmartDevice]):
        self.isRunning = True
        self.thread:threading.Thread
        self.deviceList:list[SmartDevice]
        self.name:str = name
        self.logMessages:list[SmartHomeAutomationLog] = []
        self.automationId = SmartHomeAutomation.SH_AUTO_ID
        SmartHomeAutomation.SH_AUTO_ID += 1

    def log(self, message:str):
        logMessage = SmartHomeAutomationLog(message)
        self.logMessages.append(logMessage)
        print(str(logMessage))

    def doUpdate(self, property:DeviceProperty):
        pass

    def run(self, property:DeviceProperty):
        self.doUpdate(property=property)
        # self.thread = threading.Thread(target=partial(self.doUpdate, property))

class SmartHomeAutomationJsonEncoder(json.JSONEncoder):
    def default(self, o:SmartHomeAutomation):
        tmp:dict = {}
        for key in o.__dict__:
            if key not in ['automationId', 'name', 'logMessages', 'isRunning']:
                continue
            targetVal = o.__dict__[key]
            if isinstance(targetVal, bool):
                targetVal = 'true' if targetVal == True else 'false'
            elif isinstance(targetVal, list):
                targetVal = [v.__dict__ for v in targetVal]
            elif targetVal is None:
                targetVal = 'null'
            tmp[key] = targetVal
        return tmp

class SmartHomeAutomationLog:
    def __init__(self, message:str):
        self.timestamp:int = time.time()
        self.message:str = message

    def __str__(self) -> str:
        timeStr = time.strftime("%a, %d %b %Y %H:%M:%S +0000",time.gmtime(self.timestamp))
        return f"{timeStr} | Automation | {self.message}"