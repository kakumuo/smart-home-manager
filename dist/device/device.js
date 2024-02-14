export class SmartDevice {
    constructor() {
        this.properties = new Array();
    }
}
export class DeviceProperty {
    constructor(name) {
        this.name = name;
    }
    get() {
        return this.value;
    }
    set(value) {
        this.prevValue = this.value;
        this.value = value;
    }
}
//# sourceMappingURL=device.js.map