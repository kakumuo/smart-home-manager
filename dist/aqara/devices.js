var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { SmartDevice, DeviceProperty } from '../device/device.js';
export class AqaraDevice extends SmartDevice {
    constructor(details) {
        super();
        this.model = new DeviceProperty("model");
        this.updateTime = new DeviceProperty("updateTime");
        this.modelType = new DeviceProperty("modelType");
        this.state = new DeviceProperty("state");
        this.firmwareVersion = new DeviceProperty("firmwareVersion");
        this.deviceName = new DeviceProperty("deviceName");
        this.deviceId = new DeviceProperty("deviceId");
        this.deviceStateTimestamp = new DeviceProperty("deviceStateTimestamp");
        this.updateDeviceInfo = (details) => {
            this.model.set(details.model);
            this.updateTime.set(details.updateTime);
            this.modelType.set(details.modelType);
            this.state.set(details.state);
            this.firmwareVersion.set(details.firmwareVersion);
            this.deviceName.set(details.deviceName);
            this.deviceId.set(details.did);
        };
        this.updateDeviceState = (detail) => __awaiter(this, void 0, void 0, function* () { });
        this.updateDeviceInfo(details);
        this.model = new DeviceProperty("model");
        this.properties.push(this.model);
        this.properties.push(this.updateTime);
        this.properties.push(this.modelType);
        this.properties.push(this.state);
        this.properties.push(this.firmwareVersion);
        this.properties.push(this.deviceName);
        this.properties.push(this.deviceId);
        this.properties.push(this.deviceStateTimestamp);
    }
}
export const MOTION_SENSOR_ILLUMINANCE_RID = "0.3.85";
export const MOTION_SENSOR_BATTERY_STATUS_RID = "8.0.9001";
export const MOTION_SENSOR_ILLUMINATION_RID = "0.4.85";
export const MOTION_SENSOR_BATTERY_VOLTAGE_RID = "8.0.2008";
export const MOTION_SENSOR_ZIGBEE_SIGNAL_STRENGTH_RID = "8.0.2007";
export const MOTION_SENSOR_ZIGBEE_CHANNEL_RID = "8.0.2024";
export const MOTION_SENSOR_IDENTIFY_THE_DEVICE_RID = "8.0.2041";
export const MOTION_SENSOR_SAMPLE_PERIOD_RID = "8.0.2097";
export const MOTION_SENSOR_MOTION_STATUS_RID = "3.1.85";
export class AqaraMotionSensor extends AqaraDevice {
    constructor(details) {
        super(details);
        this.lumosity = new DeviceProperty("lumosity");
        this.presence = new DeviceProperty("presence");
        this.updateDeviceState = (detail) => __awaiter(this, void 0, void 0, function* () {
            if (detail.resourceId == MOTION_SENSOR_ILLUMINATION_RID) {
                this.lumosity.set(Number.parseInt(detail.value));
            }
            else if (detail.resourceId == MOTION_SENSOR_MOTION_STATUS_RID) {
                this.presence.set(detail.value == "1");
            }
            this.deviceStateTimestamp.set(detail.timeStamp);
        });
        this.properties.push(this.lumosity);
        this.properties.push(this.presence);
    }
}
//# sourceMappingURL=devices.js.map