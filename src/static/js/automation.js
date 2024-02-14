import { APIClient } from "./client.js"

class AutomationElement {
    automationInfo = {"isRunning": "false", "name": "Presence Automation", "logMessages": [{"timestamp": 1234, "message": "test"}], "automationId": 0}
    documentRef = null
    element = null
    logSectionElement = null
    viewLogButton = null
    toggleAutomationButton = null
    automationNameLabel = null

    constructor(automationInfo, documentRef){
        this.automationInfo = automationInfo
        this.documentRef = documentRef
        this.element = document.createElement('div')
        this.element.id = `card-automation-${automationInfo.automationId}`
        this.element.classList.add('card')
        this.element.innerHTML = `
        <h3>${automationInfo.name}</h3>
        <div id="buttonGroup">
            <button id="enable">Disable</button>
            <button id="viewLog">View Log</button>
        </div>
        <section id="automationLogSection">
        </section>
        `
        this.logSectionElement = this.element.querySelector('#automationLogSection')
        this.viewLogButton = this.element.querySelector('#viewLog')
        this.automationNameLabel = this.element.querySelector('h3')
        this.toggleAutomationButton = this.element.querySelector('#enable')

        this.logSectionElement.classList.add('hidden')
        let index = 0

        this.viewLogButton.addEventListener('click', () => {
            this.logSectionElement.classList.toggle('hidden')
        })
        
        this.toggleAutomationButton.addEventListener('click', () => {
            let callbackTarget = this.automationInfo.isRunning ? APIClient.rpc_disableAutomation : APIClient.rpc_enableAutomation
            callbackTarget(this.automationInfo.automationId)
            .then((resp) => {
                this.updateAutomationDetails(resp)
            })
        })
        this.updateAutomationDetails(this.automationInfo)

        // refresh automation information every 2 seconds
        // setInterval(() => {
        //     APIClient.rpc_getAutomation(this.automationInfo.automationId)
        //     .then(
        //         resp => this.updateAutomationDetails(resp)
        //     )
        // }, 1000 * 2);
    }

    updateAutomationDetails(automationInfo){
        this.automationInfo.isRunning = automationInfo.isRunning == 'true'
        this.toggleAutomationButton.textContent = this.automationInfo.isRunning ? 'Disable' : 'Enable'
        this.automationNameLabel.textContent = this.automationInfo.name

        let index = 0
        this.logSectionElement.innerHTML = ''
        for(let message of this.automationInfo.logMessages){
            console.log(message)
            let textElement = document.createElement('p')
            textElement.textContent = `${new Date(message.timestamp * 1000).toISOString().split('T')[0]} | ${message.message}`
            textElement.classList.add(`log-line-${index++}`)
            this.logSectionElement.appendChild(textElement)
        }
    }
}


let automationMain = document.querySelector('#automation-main')
// let autoamtionInfo = {"isRunning": "false", "name": "Presence Automation", "logMessages": [
//     "Some Log Message", "Some other log message"
// ], "automationId": 0}
// let automationElement = new AutomationElement(autoamtionInfo, document)
// automationMain.appendChild(automationElement.element)

async function getAutomationList(){
    const response = await APIClient.rpc_getAutomationList()
    console.log(response)
    for(let automation of response){
        console.log(automation)
        let curDevice = new AutomationElement(automation, document)
        automationMain.appendChild(curDevice.element)
    }
}

document.addEventListener('DOMContentLoaded', () => {
    getAutomationList()
})


