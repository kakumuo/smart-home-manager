import { APIClient } from "./client.js"

export class SmartDeviceElement {
    static DEVICE_TYPE_MOTION_SENSOR = 0
    static DEVICE_TYPE_SMART_BULB = 1
    static DEVICE_TYPE_SMART_STRIP = 2

    widgetElement
    widgetMiniElement
    deviceInfo
    deviceId
    documentRef
    deviceType
    constructor(deviceInfo, documentRef){
        this.documentRef = documentRef
        this.deviceInfo = deviceInfo
        this.widgetElement = document.createElement('div')
        this.widgetMiniElement = document.createElement('div')
        this.deviceId = this.deviceInfo.deviceId
        if(deviceInfo.shDeviceType == 'TapoSmartBulb'){
            this.updateBulbElement()
            this.deviceType = SmartDeviceElement.DEVICE_TYPE_SMART_BULB

            // let hueSlider = this.widgetElement.querySelector('#hueSlider')
            // let valSlider = this.widgetElement.querySelector('#valSlider')
            let briSlider = this.widgetElement.querySelector('#briSlider')
        
            // hueSlider.addEventListener('change', () => {
            //     this.updateDevice()
            // })
            // valSlider.addEventListener('change',  () => {
            //     this.updateDevice()
            // })
            briSlider.addEventListener('change',  () => {
                this.updateDevice()
            })

            let briMiniSlider = this.widgetMiniElement.querySelector('#bri-slider')
            briMiniSlider.addEventListener('change',  () => {
                APIClient.rpc_updateDevice(this.deviceId, {'bri': this.widgetMiniElement.querySelector('#bri-slider').value})
            })

            let onOffMini = this.widgetMiniElement.querySelector('#onOff')
            onOffMini.addEventListener('click',  () => {
               const resp = APIClient.rpc_updateDevice(this.deviceId, {'isOn': !this.deviceInfo.isOn})
               resp.then((resp) => (console.log("updated bulb", resp)))
            })
        }else{
            this.updateMotionSensorElmement()
            this.deviceType = SmartDeviceElement.DEVICE_TYPE_MOTION_SENSOR
        }
    }

    refreshElement(deviceInfo){
        this.deviceInfo = deviceInfo
        if(this.deviceType = SmartDeviceElement.DEVICE_TYPE_MOTION_SENSOR){
            this.updateMotionSensorElmement()
        }else{
            this.updateBulbElement()
        }
    }

    updateDevice(){
        let properties = {}
        console.log("device type: ", this.deviceType)
        if([SmartDeviceElement.DEVICE_TYPE_SMART_BULB, SmartDeviceElement.DEVICE_TYPE_SMART_STRIP].includes(this.deviceType)){
            let hue = 0 //this.widgetElement.querySelector('#hueSlider').value
            let val = 0 //this.widgetElement.querySelector('#valSlider').value
            let bri = this.widgetElement.querySelector('#briSlider').value
            properties = {
                hue: hue,
                val: val,
                bri: bri,
                isOn: this.deviceInfo.isOn
            }
        }
        APIClient.rpc_updateDevice(this.deviceId, properties)
    }

    updateBulbElement(){
        this.widgetElement.innerHTML = `
        <div class="widget" id="widget-bulb-${this.deviceInfo.deviceId}">
            <img src="" alt="">
            <h3 id="itemName">${this.deviceInfo.name}</h3>
            <button id="optionButton">Options</button>
            <p class='hidden'>hue</p>
            <input class='hidden' type="range" name="" id="hueSlider" minValue="0" maxValue="360" value="${this.deviceInfo.hue}">
            <p class='hidden'>sat</p>
            <input class='hidden' type="range" name="" id="valSlider" minValue="0" maxValue="100" value="${this.deviceInfo.sat}">
            <p>bri</p>
            <input type="range" name="" id="briSlider" minValue="0" maxValue="100" value="${this.deviceInfo.bri}">
        </div>
        `

        this.widgetMiniElement.innerHTML = `
        <div class="device-group" id="device-${this.deviceInfo.deviceId}-group">
            <img src="" alt="">
            <p>${this.deviceInfo.name}</p>
            <input type="range" name="" id="bri-slider" minValue="0" maxValue="100" value="${this.deviceInfo.bri}">
            <button id="onOff">On/Off</button>
        </div>
        `
    }

    updateMotionSensorElmement(){
        this.widgetElement.innerHTML = `
        <div class="widget" id="widget-motion-sensor-${this.deviceInfo.deviceId}">
            <img src="" alt="">
            <h3 id="itemName">${this.deviceInfo.name}</h3>
            <button id="optionButton">Options</button>
            <p>Lumosity: ${this.deviceInfo.lumosity}</p>
            <p>Presence: ${this.deviceInfo.presence}</p>
        </div>
        `

        this.widgetMiniElement.innerHTML = `
        <div class="device-group" id="device-${this.deviceInfo.deviceId}-group">
            <img src="" alt="">
            <p>${this.deviceInfo.name}</p>
            <p>Lumosity: ${this.deviceInfo.lumosity}</p>
            <p>Presence: ${this.deviceInfo.presence}</p>
        </div>
        `
    }
}

