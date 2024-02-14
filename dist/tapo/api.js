var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { TapoCrypto } from "./tplinkCipher.js";
import * as HTTPS from "https";
import * as HTTP from 'http';
// another variant is https://n-euw1-wap-gw.tplinkcloud.com
const BASE_URL = 'use1-wap.tplinkcloud.com';
export class TapoAPIClient {
    constructor(email = process.env.TAPO_USERNAME || "", password = process.env.TAPO_PASSWORD || "") {
        this.execEndpoint = (data, requestOptions, requestHeaders, useHTTPS = true) => __awaiter(this, void 0, void 0, function* () {
            return new Promise((resolve, reject) => {
                console.log("UseHttp: ", useHTTPS, " Request: ", requestOptions);
                let responseData = "";
                // // add proxy
                // requestOptions.path = `${useHTTPS ? "https": "http"}://${requestOptions.hostname}${requestOptions.path}`
                // requestOptions.hostname = '127.0.0.1'
                // requestOptions.port = '8888'
                // requestOptions.method = "CONNECT"
                let req;
                const onRequestResponse = (resp) => {
                    resp.on('data', (chunk) => {
                        console.log("Received chunk: ", chunk.toString());
                        responseData += chunk;
                    });
                    resp.on('end', () => {
                        console.log("End of data");
                        resolve(JSON.parse(responseData));
                    });
                    console.log("response headers: ", resp.headers);
                };
                if (useHTTPS)
                    req = HTTPS.request(requestOptions, onRequestResponse);
                else
                    req = HTTP.request(requestOptions, onRequestResponse);
                for (let header in requestHeaders) {
                    req.setHeader(header, requestHeaders[header]);
                }
                console.log(`Data: ${JSON.stringify(data)}`);
                req.write(JSON.stringify(data));
                req.end();
            });
        });
        // execEndpointSecure = async (data:any, requestOptions:HTTPS.RequestOptions, requestHeaders:IncomingHttpHeaders):Promise<any> => {
        //   let deviceKey = this.deviceKey
        //   requestHeaders.cookie = deviceKey.sessionCookie
        //   this.execEndpoint(data, requestOptions, requestHeaders)
        // }
        this.cloudLogin = (email = process.env.TAPO_USERNAME || "", password = process.env.TAPO_PASSWORD || "") => __awaiter(this, void 0, void 0, function* () {
            const request = {
                "method": "login",
                "params": {
                    "appType": "Tapo_Android",
                    "cloudPassword": password,
                    "cloudUserName": email,
                    "terminalUUID": '00-00-00-00-00-00'
                }
            };
            const requestOptions = {
                method: "post",
                hostname: BASE_URL,
                path: "/"
            };
            const requestHeaders = {
                "content-type": "applicaiton/json"
            };
            const response = yield this.execEndpoint(request, requestOptions, requestHeaders);
            console.log("response from cloudLogin(): ", response);
            this.checkError(response);
            this.deviceKey.token = response.result.token;
        });
        this.getDevices = () => __awaiter(this, void 0, void 0, function* () {
            const request = {
                "method": "getDeviceList",
                "params": {
                    "token": this.deviceKey.token
                }
            };
            const requestOptions = {
                method: "post",
                hostname: BASE_URL,
                path: "/"
            };
            const requestHeaders = {
                "content-type": "applicaiton/json"
            };
            const response = yield this.execEndpoint(request, requestOptions, requestHeaders);
            this.checkError(response);
            const devices = new Array();
            response.result.deviceList.forEach((device) => {
                devices.push(device);
            });
            return devices;
        });
        this.handshake = (deviceIp) => __awaiter(this, void 0, void 0, function* () {
            // format key
            const data = {
                "method": "handshake",
                "params": {
                    "key": this.deviceKey.key.toString(),
                    "requestTimeMils": 0
                }
            };
            const requestOptions = {
                method: "post",
                hostname: deviceIp,
                path: "/app"
            };
            const localSeed = new Uint8Array(16).map(() => Math.floor(Math.random() * 256));
            const requestHeaders = {
                "content-type": "applicaiton/json"
            };
            const response = yield this.execEndpoint(data, requestOptions, requestHeaders, false);
            this.checkError(response);
            console.log("handshake response: ", response);
        });
        this.augmentTapoDevice = (deviceInfo) => __awaiter(this, void 0, void 0, function* () {
            if (this.isTapoDevice(deviceInfo.deviceType)) {
                return Object.assign(Object.assign({}, deviceInfo), { alias: TapoCrypto.base64Decode(deviceInfo.alias) });
            }
            else {
                return deviceInfo;
            }
        });
        this.isTapoDevice = (deviceType) => {
            switch (deviceType) {
                case 'SMART.TAPOBULB':
                    return true;
                default: return false;
            }
        };
        this.checkError = (responseData) => {
            const errorCode = responseData["error_code"];
            if (errorCode) {
                switch (errorCode) {
                    case 0: return;
                    case 1010: throw new Error("Invalid public key length");
                    case 1501: throw new Error("Invalid request or credentials");
                    case 1002: throw new Error("Incorrect request");
                    case 1003: throw new Error("JSON format error");
                    case 20601: throw new Error("Incorrect email or password");
                    case 20675: throw new Error("Cloud token expired or invalid");
                    case 9999: throw new Error("Device token expired or invalid");
                    default: throw new Error(`Unexpected Error Code: ${errorCode} (${responseData["msg"]})`);
                }
            }
        };
        this.findLocalDevices = (macAddress) => {
        };
        this.deviceKey = TapoCrypto.generateKeyPair();
        this.deviceKey.sessionCookie = new Map;
    }
}
// export const loginDevice = async (email: string = process.env.TAPO_USERNAME || "", password: string = process.env.TAPO_PASSWORD || "", device: TapoDevice) =>
//   loginDeviceByIp(email, password, device.ip);
// export const loginDeviceByIp = async (email: string = process.env.TAPO_USERNAME || "", password: string = process.env.TAPO_PASSWORD || "", deviceIp: string):Promise<TapoDeviceKey> => {
//   const deviceKey = await handshake(deviceIp);
//   const loginDeviceRequest =
//     {
//       "method": "login_device",
//       "params": {
//           "username": TapoCrypto.base64Encode(TapoCrypto.shaDigest(email)),
//           "password": TapoCrypto.base64Encode(password)
//      }
//   }
//   const loginDeviceResponse =  await securePassthrough(loginDeviceRequest, deviceKey);
//   deviceKey.token = loginDeviceResponse.token;
//   return deviceKey;
// }
// export const turnOn = async (deviceKey: TapoDeviceKey, deviceOn: boolean = true) => {
//   const turnDeviceOnRequest = {
//     "method": "set_device_info",
//     "params":{
//       "device_on": deviceOn,
//     },
//     "requestTimeMils": (new Date()).getTime(),
//     "terminalUUID": "00-00-00-00-00-00"
//   }
//   await securePassthrough(turnDeviceOnRequest, deviceKey)
// }
// export const turnOff = async (deviceKey: TapoDeviceKey) => {
//   return turnOn(deviceKey, false);
// }
// export const setBrightness = async (deviceKey: TapoDeviceKey, brightnessLevel: number = 100) => {
//   const setBrightnessRequest = {
//     "method": "set_device_info",
//     "params":{
//       "brightness": brightnessLevel,
//     },
//     "requestTimeMils": (new Date()).getTime(),
//     "terminalUUID": "00-00-00-00-00-00"
//   }
//   await securePassthrough(setBrightnessRequest, deviceKey)
// }
// export const setColour = async (deviceKey: TapoDeviceKey, colour: string = 'white') => {
//   const params = await ColorUtils.getColor(colour);
//   const setColourRequest = {
//     "method": "set_device_info",
//     params,
//     "requestTimeMils": (new Date()).getTime(),
//     "terminalUUID": "00-00-00-00-00-00"
//   }
//   await securePassthrough(setColourRequest, deviceKey)
// }
// export const getDeviceInfo = async (deviceKey: TapoDeviceKey): Promise<TapoDeviceInfo> => {
//   const statusRequest = {
//     "method": "get_device_info",
//     "requestTimeMils": (new Date()).getTime(),
//     "terminalUUID": "00-00-00-00-00-00"
//   }
//   return augmentTapoDeviceInfo(await securePassthrough(statusRequest, deviceKey))
// }
// export const getEnergyUsage = async (deviceKey: TapoDeviceKey): Promise<TapoDeviceInfo> => {
//   const statusRequest = {
//     "method": "get_energy_usage"
//   }
//   return securePassthrough(statusRequest, deviceKey)
// }
// export const securePassthrough = async (deviceRequest: any, deviceKey: TapoDeviceKey):Promise<any> => {
//   const encryptedRequest = TapoCrypto.encrypt(deviceRequest, deviceKey)
//   const securePassthroughRequest = {
//     "method": "securePassthrough",
//     "params": {
//         "request": encryptedRequest,
//     }
//   }
//   const response = await axios({
//     method: 'post',
//     url: `http://${deviceKey.deviceIp}/app?token=${deviceKey.token}`,
//     data: securePassthroughRequest,
//     headers: {
//       "Cookie": deviceKey.sessionCookie
//     }
//   })
//   this.checkError(response.data);
//   const decryptedResponse = TapoCrypto.decrypt(response.data.result.response, deviceKey);
//   this.checkError(decryptedResponse);
//   return decryptedResponse.result;
// }
// const tplinkCaAxios = (): AxiosInstance => {
//   const httpsAgent = new https.Agent({
//     rejectUnauthorized: true,
//     ca: tplinkCaCert,
//   })
//   return axios.create({ httpsAgent })
// }
// const augmentTapoDeviceInfo = (deviceInfo: TapoDeviceInfo): TapoDeviceInfo => {
//     return {
//       ...deviceInfo,
//       ssid: TapoCrypto.base64Decode(deviceInfo.ssid),
//       nickname: TapoCrypto.base64Decode(deviceInfo.nickname),
//     }
// }
//# sourceMappingURL=api.js.map