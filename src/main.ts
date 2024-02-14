// import {TapoAPIClient} from './tapo/api.js'
// import * as AqaraClient from './aqara/api.js'
// import { AqaraSession } from './aqara/types.js'
// import { generateSession } from './aqara/aqaraCrypto.js'
// import * as fs from 'fs'
// import { AqaraMotionSensor } from 'aqara/devices.js'
// import * as CryptoJS from 'crypto-js'
// import { exec } from 'child_process'

// // import * as TAPO from "tp-link-tapo-connect"

// let tapoTest = async() => {
//     const fileData = fs.readFileSync(fs.openSync("C:\\Users\\foxfe\\Documents\\Projects\\smart-home-manager\\etc\\tapo.properties", "r"))
//     let username:string = ""
//     let password:string = ""

//     fileData.toString("ascii").split('\r\n').forEach(element => {
//         const res = element.split('=')
//         if(res[0] == "username") username = res[1]
//         if(res[0] == "password") password = res[1]
//     });

//     const apiClient = new TapoAPIClient()
//     await apiClient.cloudLogin(username, password)
    
//     let resp = await apiClient.getDevices()
//     // console.log("Device List: ", resp)

//     await apiClient.handshake("192.168.0.142")

//     // const resp  = await TapoClient.handshake("192.168.0.139", accessToken)
//     // console.log("Device handshake: ", resp)
//     // TapoClient.handshake("192.168.0.142")
//     // TapoClient.handshake("192.168.0.166")
//     // TapoClient.handshake("192.168.0.235")
//     // TapoClient.handshake("192.168.0.233")

//     // TapoClient.handshake("192.168.0.233")
//     // .then((resp) => {
//     //     console.log(JSON.stringify(resp))
//     // })
// }
// tapoTest()

// // let tapoConnect = async() => {
// //     const fileData = fs.readFileSync(fs.openSync("C:\\Users\\foxfe\\Documents\\Projects\\smart-home-manager\\etc\\tapo.properties", "r"))
// //     let username:string = ""
// //     let password:string = ""

// //     fileData.toString("ascii").split('\r\n').forEach(element => {
// //         const res = element.split('=')
// //         if(res[0] == "username") username = res[1]
// //         if(res[0] == "password") password = res[1]
// //     });

// //     const cloudToken = await TAPO.cloudLogin(username, password)
// //     const devices = await TAPO.listDevices(cloudToken)

// //     console.log("Cloud Token: ", cloudToken)
// //     console.log("Devices: ", devices)

// //     const deviceToken = await TAPO.loginDevice(username, password, devices[0]); // Performs a mac lookup to determine local IP address
// //     // const deviceToken = await TAPO.loginDeviceByIp(username, password, "192.168.0.142"); 
// //     const getDeviceInfoResponse = await TAPO.getDeviceInfo(deviceToken);
// //     console.log(getDeviceInfoResponse);
// // }
// // tapoConnect()

// let aqaraTest = async () => {
//     const configFilePath = './etc/aqara.properties'

//     const userName:string = "foxfen23@hotmail.com"
//     const authCode:string = "487203"

//     let session:AqaraSession = generateSession(null)
//     // session = await AqaraClient.getAuthCode(userName, session)
//     // session.authCode = authCode
    
//     // console.log("session: ", session)

//     session = {
//         appId: '116919905883855667241b3f',
//         keyId: 'K.1169199058872111104',
//         nonce: '1700274998628',
//         appKey: 'lc4levem8p64n1clkc2pmlwtxsxac81e',
//         sign: '03b565fe2cd273b076612882af1e2d22',
//         time: '1700274998628',
//         accessToken: 'a4bf7ca42be06085718d53f710ab8446',
//         authCode: '927481',
//         refreshToken: 'f7611476492626b7820ce557fc388c9c',
//         openId: '531372067721169568896721842177',
//         expiresIn: '3600',
//         timestamp: 1700274998906
//     }
    
//     // session = await AqaraClient.getAccessToken(userName, session)
//     console.log(session)

//     // const fd = fs.openSync(configFilePath, 'r')
//     // fs.writeSync(fd, `session.expiresIn=${session.expiresIn}`)
//     // fs.writeSync(fd, `session.openId=${session.openId}`)
//     // fs.writeSync(fd, `session.accessToken=${session.accessToken}`)
//     // fs.writeSync(fd, `session.refreshToken=${session.refreshToken}`)
//     // fs.writeSync(fd, `session.timestamp=${session.timestamp}`)
//     // fs.closeSync(fd)

//     let resp = await AqaraClient.getDevices(session)
//     if(resp.length == 0){
//         console.log("Could not find any devices...")
//     }

//     let motionSensor:AqaraMotionSensor = resp[0]
//     await AqaraClient.updateDeviceState(session, motionSensor)

//     console.log("response: ", motionSensor)
// }
// // aqaraTest()

