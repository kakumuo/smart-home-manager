import * as HTTP from "http";
const getDomainURL = (countryCode) => {
    const domains = {
        "cn": "aiot-coap.aqara.cn",
        "us": "aiot-coap-usa.aqara.com",
        "sk": "coap-kr.aqara.com",
        "ru": "coap-ru.aqara.com",
        "eu": "coap-ger.aqara.com",
        "sg": "coap-sg.aqara.com",
    };
    return `https://${domains[countryCode]}/v3.0/open/api`;
};
const getDomainSDKURL = (countryCode) => {
    const domains = {
        "cn": "open-cn.aqara.com",
        "us": "open-usa.aqara.com",
        "sk": "open-kr.aqara.com",
        "ru": "open-ru.aqara.com",
        "eu": "open-ger.aqara.com",
        "sg": "open-sg.aqara.com",
    };
    return `https://${domains[countryCode]}/v3.0/open/api`;
};
export const doLogin = (countryCode) => {
    let baseURL = getDomainURL(countryCode);
    let data = {
        "intent": "config.auth.getAuthCode",
        "data": {
            "account": "189000123456",
            "accountType": 0,
            "accessTokenValidity": "1h"
        }
    };
    const req = HTTP.request(baseURL, (resp) => {
        resp.on('data', (chunk) => {
            console.log("Received chunk: ", chunk);
        });
        resp.on('end', () => {
            console.log("End of data");
        });
    });
    req.on('error', (err) => {
        console.log(`Received error - code: ${err.name}; message: ${err.message}`);
    });
    req.write(data);
    req.end();
    return "";
};
export const checkError = (errorCode) => {
    const errorMap = {
        '0': 'Success',
        '100': 'Timeout',
        '101': 'Invalid data package',
        '102': 'Data package has altered',
        '103': 'Data package may lose',
        '104': 'Server busy',
        '105': 'Data package has expired',
        '106': 'Invalid sign',
        '107': 'Illegal appKey',
        '108': 'Token has expired',
        '109': 'Token is absence',
        '302': 'Params error',
        '303': 'Request params type error',
        '304': 'Request method not support',
        '305': 'Header Params error',
        '306': 'Request path not open',
        '403': 'Request forbidden',
        '429': 'Too Many Requests',
        '500': 'Service impl error',
        '501': 'Service proxy error',
        '601': 'Device not register',
        '602': 'Device is offline',
        '603': 'Device permission denied',
        '604': 'Illegal device id',
        '605': 'Device info inconsistent',
        '606': 'Device request not support',
        '607': 'Gateway has been bind',
        '608': 'Sub device bind error',
        '609': 'Gateway unbind error',
        '610': 'Subdevice unbind error',
        '611': 'Subdevice not bind',
        '612': 'Gateway request not response',
        '615': 'Not find parent device',
        '636': 'BindKey time out',
        '637': 'Irid not exists',
        '638': 'Sub device not support this operation',
        '639': 'Device cannot mount sub device',
        '640': 'Device five code not found',
        '641': 'Bluetooth device operate with wrong step',
        '642': 'Bluetooth device validate wrong',
        '643': 'Bluetooth info not exist',
        '644': 'Failed validate security code',
        '645': 'App bluetooth device register wrong step',
        '651': 'Gateway not exists',
        '652': 'Gateway limit',
        '655': 'dynamic sequence run failed',
        '656': 'Device not allow bind',
        '657': 'Device group config exist',
        '658': 'This ir device not support copy',
        '664': 'Device function not support',
        '701': 'Position not exist',
        '702': 'Position cannot deleted',
        '703': 'Position name duplication',
        '704': 'Default position create duplication',
        '705': 'Device name duplication',
        '706': 'Device permission denied',
        '707': 'Ifttt permission denied',
        '708': 'Scene permission denied',
        '709': 'Service permission denied',
        '710': 'Position permission denied',
        '712': 'Parent position error',
        '713': 'Position not real position',
        '714': 'Position is not allowed to be deleted',
        '715': 'Position error',
        '716': 'Scene not exist',
        '717': 'Device does not belong to this user',
        '718': 'Data error',
        '719': 'Device no bind user',
        '722': 'Out of position layer',
        '726': 'Device size beyond',
        '727': 'Position size beyond',
        '728': 'Start or end time cannot be empty',
        '729': 'The start time must not be greater than the end time',
        '730': 'Start or end time not a timestamp',
        '731': 'Ifttt not exists',
        '745': 'BindKey not exists',
        '746': 'Gateway not connect cloud',
        '747': 'Device unsupported',
        '748': 'Category model not exists',
        '749': 'Custom Action name duplicate',
        '750': 'Ircode key not exists',
        '751': 'BindKey has been used',
        '753': 'ir device limit',
        '754': 'Custom Action not exist',
        '755': 'subject permission denied',
        '756': 'no permissions',
        '757': 'Device not bind user',
        '758': 'Param length limit',
        '760': 'Action not support',
        '763': 'Trigger not support',
        '768': 'Ifttt name has exists',
        '769': 'Scene name has exists',
        '770': 'Device name has exists',
        '778': 'The device can not unbind',
        '788': 'Condition event Permission denied',
        '789': 'Condition event duplicate name',
        '801': 'Account not register',
        '802': 'Account not login',
        '803': 'User permission denied',
        '804': 'Token failed',
        '805': 'Account has register',
        '807': 'Account format error',
        '810': 'Password incorrect',
        '811': 'AuthCode incorrect',
        '812': 'Account type unsupport',
        '816': 'AuthCode incorrect',
        '817': 'AuthCode send all too often',
        '820': 'AuthCode is invalid',
        '901': 'Upgrade error',
        '902': 'Firmware not exist',
        '903': 'Package not exist',
        '904': 'Firmware already up to date',
        '905': 'Firmware query is empty',
        '906': 'No updatable firmware',
        '907': 'firmware upgrade failed',
        '908': 'Device is being upgrade',
        '909': 'The sub devices gateway is being upgraded',
        '910': 'The gateways sub device are being upgraded',
        '911': 'The sub devices gateway is also upgraded',
        '912': 'Model cant be upgraded with firmware',
        '1003': 'Resource attr illegal',
        '1004': 'Resource value illegal',
        '1006': 'Subject type not support',
        '1007': 'Resource write not support',
        '1008': 'Resource attr not exist',
        '1009': 'Report attr error',
        '1010': 'Report resourceId error',
        '1201': 'Linkage not exist',
        '1202': 'Scene not exist',
        '1203': 'Ifttt execute condition not satisfied',
        '1204': 'linkage no device',
        '1205': 'Scene no device',
        '1206': 'Delete local linkage failed',
        '1207': 'Operation failed',
        '1208': 'Ifttt parameter error',
        '1210': 'This action not definition',
        '1211': 'This trigger not definition',
        '1212': 'Action is empty',
        '1221': 'Ifttt execute failed',
        '1223': 'Ifttt same name',
        '1224': 'scene same name',
        '1226': 'Conditions of configuration is not correct',
        '1227': 'Conditions of configuration is not correct',
        '1228': 'Condition is repeated',
        '1229': 'Conditions of configuration is not correct',
        '1230': 'Action is repeated',
        '1231': 'Actions of configuration is not correct',
        '1232': 'Conditions and Actions of configuration is not correct',
        '1238': 'ifttt is abnormal',
        '1239': 'Conditions of configuration is not correct',
        '1300': 'The data is in operation',
        '2001': 'Get developer list error',
        '2002': 'Appid or Appkey illegal',
        '2003': 'AuthCode incorrect',
        '2004': 'AccessToken incorrect',
        '2005': 'AccessToken expired',
        '2006': 'RefreshToken incorrect',
        '2007': 'RefreshToken expired',
        '2008': 'Permission denied',
        '2009': 'Invalid OpenId',
        '2010': 'Unauthorized user',
        '2011': 'The query result is empty',
        '2012': 'Invalid apply',
        '2013': 'Developer Permission denied',
        '2014': 'Resource Permission denied',
        '2015': 'subscriber faild',
        '2016': 'AccountId has exist',
        '2017': 'Appkey exceeds the limit',
        '2018': 'IP config exceed the limit',
        '2022': 'Application not activated',
    };
    if (errorCode) {
        throw new Error(`Received Error - code: ${errorCode.toString()} => ${errorMap[errorCode]}`);
    }
};
//# sourceMappingURL=api.js.map