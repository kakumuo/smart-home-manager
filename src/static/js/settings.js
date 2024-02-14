import { rpc_call } from "./util.js"
import { APIClient } from "./client.js"

const hostname = '127.0.0.1:5000'
let isConfirmDisabled = false
let settingsState = {
    "Aqara": {
        "appid": "",
        "keyid": "",
        "appkey": "",
        "accesstoken": "",
        "refreshtoken": "",
        "expiresin": "",
        "timestamp": "",
        "username": ""
    },
    "Tapo": {
        "username": "",
        "password": ""
    }
}

/* AQARA */
const authCodeDurationInput = document.querySelector('#aqara-auth-code-duration')
const genAuthCodeBtn = document.querySelector('#aqara-gen-auth-code-btn')
const authCodeInput = document.querySelector('#aqara-auth-code')
const refreshAccessTokenBtn = document.querySelector('#aqara-gen-access-token-btn')

const aqaraEmail = document.querySelector('#aqara-email')
const aqaraAppId = document.querySelector('#aqara-appid')
const aqaraKeyId = document.querySelector('#aqara-keyid')
const aqaraAppKey = document.querySelector('#aqara-appkey')


/* TAPO */
const tapoUsername = document.querySelector('#tapo-username')
const tapoPassword = document.querySelector('#tapo-password')

/* GENERAL */
const cancelBtn = document.querySelector('#cancel-btn')
const applyBtn = document.querySelector('#apply-btn')



function validateSettingsState(){
    const isSame = aqaraEmail.value == settingsState['Aqara']['username']
        & aqaraAppId.value == settingsState['Aqara']['appid']
        & aqaraKeyId.value == settingsState['Aqara']['keyid']
        & aqaraAppKey.value == settingsState['Aqara']['appkey']
        & tapoUsername.value == settingsState['Tapo']['username']
        & tapoPassword.value == settingsState['Tapo']['password']


    if(!isSame){
        isConfirmDisabled = false
        cancelBtn.disabled = false
        applyBtn.disabled = false
    }else if (!isConfirmDisabled){
        cancelBtn.disabled = true
        applyBtn.disabled = true
        isConfirmDisabled = true
    }
}

function updateSettings() {
    aqaraEmail.value = settingsState['Aqara']['username']
    aqaraAppId.value = settingsState['Aqara']['appid']
    aqaraKeyId.value = settingsState['Aqara']['keyid']
    aqaraAppKey.value = settingsState['Aqara']['appkey']

    tapoUsername.value = settingsState['Tapo']['username']
    tapoPassword.value = settingsState['Tapo']['password']
}


[aqaraEmail, aqaraAppId, aqaraKeyId, aqaraAppKey, tapoUsername, tapoPassword].forEach((element) => {
    element.addEventListener('change', () => {
        console.log("detected settings chagne: enabling buttons")
        validateSettingsState()
    })
})



refreshAccessTokenBtn.addEventListener('click', APIClient.rpc_generateAccessToken.bind(authCodeDurationInput.value))
genAuthCodeBtn.addEventListener('click', APIClient.rpc_generateAuthCode.bind(authCodeInput.value))
// get settings details from server
document.addEventListener('DOMContentLoaded', () => {
    APIClient.rpc_getSettings().then((data) =>{
        settingsState = data
        updateSettings()
        validateSettingsState()
    })
})

