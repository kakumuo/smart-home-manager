import asyncio
import importlib
from device.smartDevice import SmartDevice, DeviceProperty
from tapo import ApiClient 
import base64

"""
{
  "avatar": "bulb",
  "brightness": 10,
  "color_temp": 2700,
  "default_states": {
    "state": {
      "brightness": 10
    },
    "type": "last_states"
  },
  "device_id": "80235CA0FF2FDFBB1BECEA40CBEB4A952128F998",
  "device_on": true,
  "dynamic_light_effect_enable": false,
  "dynamic_light_effect_id": null,
  "fw_id": "00000000000000000000000000000000",
  "fw_ver": "1.1.0 Build 230721 Rel.224802",
  "has_set_location_info": true,
  "hue": 0,
  "hw_id": "FDE1C68674D1535B12A042682B192E4E",
  "hw_ver": "2.0",
  "ip": "192.168.0.142",
  "lang": "en_US",
  "latitude": 407159,
  "longitude": -740784,
  "mac": "78-8C-B5-A9-FD-B5",
  "model": "L530",
  "nickname": "bottom lamp",
  "oem_id": "90171A8CAC7DBD1A9BE64C1449D24A6A",
  "on_time": null,
  "overheated": false,
  "region": "America/New_York",
  "rssi": -51,
  "saturation": 0,
  "signal_level": 2,
  "specs": "",
  "ssid": "lil bish 2.4G",
  "time_diff": -300,
  "type": "SMART.TAPOBULB"
}

"""

class TapoDevice(SmartDevice):
    def __init__(self, details:dict, lightHandler):
        super().__init__()
        self.lightHandler = lightHandler
    pass

class TapoSmartBulb(TapoDevice):
    def __init__(self, details:dict, lightHandler):
        super(TapoSmartBulb, self).__init__(details, lightHandler)
        self.hue = DeviceProperty("hue")
        self.sat = DeviceProperty("sat")
        self.bri = DeviceProperty("bri")
        self.isOn = DeviceProperty("isOn")
        self.name = DeviceProperty("name")

        self.properties["hue"] = self.hue
        self.properties["sat"] = self.sat
        self.properties["bri"] = self.bri
        self.properties["isOn"] = self.isOn
        self.properties["name"] = self.name

        self.updateDeviceInfo(details)

    def updateDeviceInfo(self, details):
        self.ipAddress.set(details["hue"])
        self.hue.set(details["hue"])
        self.sat.set(details["saturation"])
        self.bri.set(details["brightness"])
        self.isOn.set(details["device_on"])
        self.name.set(base64.b64decode(details["nickname"]).decode('utf-8'))

    def refreshDeviceInfo(self):
        async def updateDeviceHelper():
            deviceInfo  = await self.lightHandler.get_device_info_json()
            self.updateDeviceInfo(deviceInfo)

        loop = asyncio.new_event_loop()
        loop.run_until_complete(updateDeviceHelper())
        pass

    def updateDevice(self, properties:dict):
        async def updateDeviceHelper():
            if 'bri' in properties:
                await self.lightHandler.set_brightness(int(properties['bri']))

            if 'isOn' in properties:
                await self.lightHandler.on() if  properties['isOn'] else self.lightHandler.off()

            # deviceInfo  = await self.lightHandler.get_device_info_json()
            # self.updateDeviceState(deviceInfo)

        loop = asyncio.new_event_loop()
        loop.run_until_complete(updateDeviceHelper())
        pass


    def updateDeviceState(self, detail):
        pass

