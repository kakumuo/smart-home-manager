import importlib
from device.smartDevice import SmartDevice, DeviceProperty

class AqaraDevice(SmartDevice):
    def __init__(self, details):
        super().__init__()
        self.model = DeviceProperty("model")
        self.updateTime = DeviceProperty("updateTime")
        self.modelType = DeviceProperty("modelType")
        self.state = DeviceProperty("state")
        self.firmwareVersion = DeviceProperty("firmwareVersion")
        self.name = DeviceProperty("name")
        self.deviceStateTimestamp = DeviceProperty("deviceStateTimestamp")
        self.dId = DeviceProperty("did")

        self.updateDeviceInfo(details)

        self.properties['model'] = self.model
        self.properties['updateTime'] = self.updateTime
        self.properties['modelType'] = self.modelType
        self.properties['state'] = self.state
        self.properties['firmwareVersion'] = self.firmwareVersion
        self.properties['name'] = self.name
        self.properties['deviceStateTimestamp'] = self.deviceStateTimestamp
        self.properties['did'] = self.dId

    def updateDeviceInfo(self, details):
        self.model.set(details.get("model"))
        self.updateTime.set(details.get("updateTime"))
        self.modelType.set(details.get("modelType"))
        self.state.set(details.get("state"))
        self.firmwareVersion.set(details.get("firmwareVersion"))
        self.name.set(details.get("deviceName"))
        self.dId.set(details.get("did"))

    def updateDeviceState(self, detail):
        pass


class AqaraMotionSensor(AqaraDevice):
    MOTION_SENSOR_ILLUMINATION_RID = "0.4.85"
    MOTION_SENSOR_PRESENCE_STATUS_RID = "3.51.85"
    MOTION_SENSOR_PRESENCE_Z1_STATUS_RID = "3.1.85"
    MOTION_SENSOR_PRESENCE_Z2_STATUS_RID = "3.2.85"
    MOTION_SENSOR_PRESENCE_Z3_STATUS_RID = "3.3.85"


    def __init__(self, details):
        super().__init__(details)
        self.lumosity = DeviceProperty("lumosity")
        self.presence = DeviceProperty("presence")
        self.zone1Presence = DeviceProperty('zone1Presence')
        self.zone2Presence = DeviceProperty('zone2Presence')
        self.zone3Presence = DeviceProperty('zone3Presence')

        self.properties['lumosity'] = self.lumosity
        self.properties['presence'] = self.presence
        self.properties['zone1Presence'] = self.zone1Presence
        self.properties['zone2Presence'] = self.zone2Presence
        self.properties['zone3Presence'] = self.zone3Presence
    
    def updateDeviceState(self, detail):
        # print("Motion Sensor device details: ", detail)
        match detail["resourceId"]:
            case AqaraMotionSensor.MOTION_SENSOR_ILLUMINATION_RID:
                self.lumosity.set(int(detail["value"]))
            case AqaraMotionSensor.MOTION_SENSOR_PRESENCE_STATUS_RID:
                self.presence.set(detail["value"] == "1")
            case AqaraMotionSensor.MOTION_SENSOR_PRESENCE_Z1_STATUS_RID:
                self.zone1Presence.set(detail["value"] == "1")
            case AqaraMotionSensor.MOTION_SENSOR_PRESENCE_Z2_STATUS_RID:
                self.zone2Presence.set(detail["value"] == "1")
            case AqaraMotionSensor.MOTION_SENSOR_PRESENCE_Z3_STATUS_RID:
                self.zone3Presence.set(detail["value"] == "1")

        # when getting response through api, response contains timeStamp attribute; through mq, response contains time attribute
        timeAttr:str = "timeStamp" if 'timeStamp' in detail else "time"
        self.deviceStateTimestamp.set(detail[timeAttr])
