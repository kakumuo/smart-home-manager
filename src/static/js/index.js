import { SmartDeviceElement } from "./device.js"
import { APIClient } from "./client.js"

const hostname = "127.0.0.1:5000"
const sidebarButtons = document.querySelectorAll('#sidebar > button')
const mainContentPanels = document.querySelectorAll('main')
const overviewMain = document.querySelector('#overview-main')
const sidebarDeviceList = document.querySelector('#sidebar > #device-list')
const title = document.querySelector('h1')

let deviceList = []

APIClient.init(hostname)


sidebarButtons.forEach((button) => {
    button.addEventListener('click', (event) => {
        setCurrentContentPane(button)
    })
})

function setCurrentContentPane(button) {
    if (!button.classList.contains('button-selected')) {
        button.classList.add('button-selected');
    } else { // Exit if the button is already selected
        return;
    }

    for (let sidebarButton of sidebarButtons) {
        if (sidebarButton.classList.contains('button-selected') && sidebarButton !== button) {
            sidebarButton.classList.remove('button-selected');
        }
    }

    let buttonName = button.id.substring(0, button.id.indexOf('-'));
    for (let contentPanel of mainContentPanels) {
        let contentPanelName = contentPanel.id.substring(0, contentPanel.id.indexOf('-'));
        if (contentPanelName === buttonName) {
            contentPanel.classList.remove('hidden');
            title.textContent = buttonName.toUpperCase()
        } else {
            contentPanel.classList.add('hidden');
            console.log(`hiding pane: ${contentPanelName}`)
        }
    }
}

async function getDeviceList(){
    const response = await APIClient.rpc_getDeviceList()
    for(let device of response){
        console.log(device)
        let curDevice = new SmartDeviceElement(device, document)
        overviewMain.appendChild(curDevice.widgetElement) 
        sidebarDeviceList.appendChild(curDevice.widgetMiniElement)
        deviceList.push(curDevice)
    }
}

async function updateDeviceList(){
    const response = await APIClient.rpc_getDeviceList()
    for(let device of response){
        for(let target of deviceList){
            if (target.deviceId == device.deviceId){
                target.refreshElement(device)
                break;
            }
        }
    }
}

// setInterval(() => {
//     updateDeviceList()
// }, 1000 * 3);

document.addEventListener('DOMContentLoaded', () => {
    setCurrentContentPane(sidebarButtons[0])
    getDeviceList()
})

