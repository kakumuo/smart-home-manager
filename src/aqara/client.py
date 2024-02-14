# from session import AqaraSession
from aqara.session import AqaraSession
from aqara.aqdevice import AqaraDevice, AqaraMotionSensor
import aqara.aqdevice

import requests
import time
import json

class AqaraClient:
    TARGET_COUNTRY = 'us'
    API_PATH = 'v3.0/open/api'

    def getDomainSDKURL(self, countryCode):
        domains = {
            "cn": "open-cn.aqara.com",
            "us": "open-usa.aqara.com",
            "sk": "open-kr.aqara.com",
            "ru": "open-ru.aqara.com",
            "eu": "open-ger.aqara.com",
            "sg": "open-sg.aqara.com",
        }

        return domains[countryCode]

    def execEndpoint(self, data, method, cur_session):
        responseData = ""
        hostname = self.getDomainSDKURL(self.TARGET_COUNTRY)
        api_path = self.API_PATH
        session = AqaraSession.generateSession(cur_session)
        
        headers = {
            "Appid": session.appId,
            "Keyid": session.keyId,
            "Nonce": session.nonce,
            "Time": session.time,
            "Sign": session.sign,
            "Content-Type": "application/json"
        }

        if session.accessToken != None and session.accessToken != "":
            headers["AccessToken"] = session.accessToken

        print(f"Data: {json.dumps(data)}")
        print(f"Headers: {json.dumps(headers)}")
        response = requests.request(
            method,
            f"https://{hostname}/{api_path}",
            headers=headers,
            data=json.dumps(data)
        )

        print("Response Status Code:", response.status_code)

        if response.status_code == 200:
            responseData = response.json()
            session_info = {
                "responseData": responseData,
                "session": session
            }
            return session_info
        else:
            # Handle other status codes here if needed
            print("Error:", response.text)
            return None
        
    def getAuthCode(self, emailAddress, session, accountType=0, duration="1h"):
        data = {
            "intent": "config.auth.getAuthCode",
            "data": {
                "account": emailAddress,
                "accountType": accountType,
                "accessTokenValidity": duration
            }
        }

        response = self.execEndpoint(data, 'post', session)

        if 'code' in response['responseData'] and str(response['responseData']['code']) != '0':
            errorMessage = response['responseData']
            print(f'Aqara Session - Received Error: {errorMessage}')
        else:
            response['session'].authCode = response['responseData']['result']['authCode']

        return response['session']
    
    def getAccessToken(self, emailAddress:str, session:AqaraSession, accountType:int = 0):
        data = {
            "intent": "config.auth.getToken",
            "data": {
                "authCode": session.authCode,
                "account": emailAddress,
                "accountType": accountType
            }
        }

        print("get access token data: ", data)

        response = self.execEndpoint(data, 'post', session)

        if 'code' in response['responseData'] and str(response['responseData']['code']) != '0':
            errorMessage = response['responseData']
            print(f'Aqara Session - Received Error: {errorMessage}')
        else:
            response['session'].accessToken = response['responseData']['result']['accessToken']
            response['session'].refreshToken = response['responseData']['result']['refreshToken']
            response['session'].openId = response['responseData']['result']['openId']
            response['session'].expiresIn = response['responseData']['result']['expiresIn']
            response['session'].timestamp = round(time.time() * 1000)

        return response['session']
    

    def refreshToken(self, session):
        data = {
            "intent": "config.auth.refreshToken",
            "data": {
                "refreshToken": session.refreshToken
            }
        }
        print("get access token data: ", data)

        response = self.execEndpoint(data, 'post', session)
        response['session'].accessToken = response['responseData']['result']['accessToken']
        response['session'].refreshToken = response['responseData']['result']['refreshToken']
        response['session'].openId = response['responseData']['result']['openId']
        response['session'].expiresIn = response['responseData']['result']['expiresIn']
        response['session'].timestamp = round(time.time() * 1000)
        return response['session']
    

    def getDevices(self, session, device_id=None) -> list[AqaraDevice]:
        data = {
            "intent": "query.device.info",
            "data": {
                "positionId": "",
                "pageNum": 1,
                "pageSize": 50
            }
        }

        if device_id and device_id != "":
            data['dids'] = [device_id]

        response = self.execEndpoint(data, 'post', session)
        if 'code' in response['responseData'] and str(response['responseData']['code']) != '0':
            errorMessage = response['responseData']
            print(f'Aqara Session - Received Error: {errorMessage}')
            return None
        else:
            device_list = []
            for device_details in response['responseData']['result']['data']:
                device_list.append(self.createDevice(device_details))
            return device_list
    
    def updateDeviceState(self, session, device:AqaraDevice):
        resource_ids = []
        if isinstance(device, AqaraMotionSensor):
            resource_ids = [
                AqaraMotionSensor.MOTION_SENSOR_ILLUMINATION_RID,
                AqaraMotionSensor.MOTION_SENSOR_PRESENCE_STATUS_RID,
                AqaraMotionSensor.MOTION_SENSOR_PRESENCE_Z1_STATUS_RID,
                AqaraMotionSensor.MOTION_SENSOR_PRESENCE_Z2_STATUS_RID,
                AqaraMotionSensor.MOTION_SENSOR_PRESENCE_Z3_STATUS_RID
            ]

        data = {
            "intent": "query.resource.value",
            "data": {
                "resources": [
                    {
                        "subjectId": device.dId.value,
                        "resourceIds": resource_ids
                    }
                ]
            }
        }

        response = self.execEndpoint(data, 'post', session)

        for resource_details in response['responseData']['result']:
            device.updateDeviceState(resource_details)

        return device
    
    def createDevice(self, deviceDetail):
        if deviceDetail['model'].__contains__('motion'):
            return AqaraMotionSensor(deviceDetail)
        return None
    
    def checkError(self, error_code):
        error_map = {
            '0':'Success',
            '100':'Timeout',
            '101':'Invalid data package',
            '102':'Data package has altered',
            '103':'Data package may lose',
            '104':'Server busy',
            '105':'Data package has expired',
            '106':'Invalid sign',
            '107':'Illegal appKey',
            '108':'Token has expired',
            '109':'Token is absence',
            '302':'Params error',
            '303':'Request params type error',
            '304':'Request method not support',
            '305':'Header Params error',
            '306':'Request path not open',
            '403':'Request forbidden',
            '429':'Too Many Requests',
            '500':'Service impl error',
            '501':'Service proxy error',
            '601':'Device not register',
            '602':'Device is offline',
            '603':'Device permission denied',
            '604':'Illegal device id',
            '605':'Device info inconsistent',
            '606':'Device request not support',
            '607':'Gateway has been bind',
            '608':'Sub device bind error',
            '609':'Gateway unbind error',
            '610':'Subdevice unbind error',
            '611':'Subdevice not bind',
            '612':'Gateway request not response',
            '615':'Not find parent device',
            '636':'BindKey time out',
            '637':'Irid not exists',
            '638':'Sub device not support this operation',
            '639':'Device cannot mount sub device',
            '640':'Device five code not found',
            '641':'Bluetooth device operate with wrong step',
            '642':'Bluetooth device validate wrong',
            '643':'Bluetooth info not exist',
            '644':'Failed validate security code',
            '645':'App bluetooth device register wrong step',
            '651':'Gateway not exists',
            '652':'Gateway limit',
            '655':'dynamic sequence run failed',
            '656':'Device not allow bind',
            '657':'Device group config exist',
            '658':'This ir device not support copy',
            '664':'Device function not support',
            '701':'Position not exist',
            '702':'Position cannot deleted',
            '703':'Position name duplication',
            '704':'Default position create duplication',
            '705':'Device name duplication',
            '706':'Device permission denied',
            '707':'Ifttt permission denied',
            '708':'Scene permission denied',
            '709':'Service permission denied',
            '710':'Position permission denied',
            '712':'Parent position error',
            '713':'Position not real position',
            '714':'Position != allowed to be deleted',
            '715':'Position error',
            '716':'Scene not exist',
            '717':'Device does not belong to this user',
            '718':'Data error',
            '719':'Device no bind user',
            '722':'Out of position layer',
            '726':'Device size beyond',
            '727':'Position size beyond',
            '728':'Start or end time cannot be empty',
            '729':'The start time must not be greater than the end time',
            '730':'Start or end time not a timestamp',
            '731':'Ifttt not exists',
            '745':'BindKey not exists',
            '746':'Gateway not connect cloud',
            '747':'Device unsupported',
            '748':'Category model not exists',
            '749':'Custom Action name duplicate',
            '750':'Ircode key not exists',
            '751':'BindKey has been used',
            '753':'ir device limit',
            '754':'Custom Action not exist',
            '755':'subject permission denied',
            '756':'no permissions',
            '757':'Device not bind user',
            '758':'Param length limit',
            '760':'Action not support',
            '763':'Trigger not support',
            '768':'Ifttt name has exists',
            '769':'Scene name has exists',
            '770':'Device name has exists',
            '778':'The device can not unbind',
            '788':'Condition event Permission denied',
            '789':'Condition event duplicate name',
            '801':'Account not register',
            '802':'Account not login',
            '803':'User permission denied',
            '804':'Token failed',
            '805':'Account has register',
            '807':'Account format error',
            '810':'Password incorrect',
            '811':'AuthCode incorrect',
            '812':'Account type unsupport',
            '816':'AuthCode incorrect',
            '817':'AuthCode send all too often',
            '820':'AuthCode is invalid',
            '901':'Upgrade error',
            '902':'Firmware not exist',
            '903':'Package not exist',
            '904':'Firmware already up to date',
            '905':'Firmware query is empty',
            '906':'No updatable firmware',
            '907':'firmware upgrade failed',
            '908':'Device is being upgrade',
            '909':'The sub devices gateway is being upgraded',
            '910':'The gateways sub device are being upgraded',
            '911':'The sub devices gateway is also upgraded',
            '912':'Model cant be upgraded with firmware',
            '1003':'Resource attr illegal',
            '1004':'Resource value illegal',
            '1006':'Subject type not support',
            '1007':'Resource write not support',
            '1008':'Resource attr not exist',
            '1009':'Report attr error',
            '1010':'Report resourceId error',
            '1201':'Linkage not exist',
            '1202':'Scene not exist',
            '1203':'Ifttt execute condition not satisfied',
            '1204':'linkage no device',
            '1205':'Scene no device',
            '1206':'Delete local linkage failed',
            '1207':'Operation failed',
            '1208':'Ifttt parameter error',
            '1210':'This action not definition',
            '1211':'This trigger not definition',
            '1212':'Action is empty',
            '1221':'Ifttt execute failed',
            '1223':'Ifttt same name',
            '1224':'scene same name',
            '1226':'Conditions of configuration != correct',
            '1227':'Conditions of configuration != correct',
            '1228':'Condition is repeated',
            '1229':'Conditions of configuration != correct',
            '1230':'Action is repeated',
            '1231':'Actions of configuration != correct',
            '1232':'Conditions and Actions of configuration != correct',
            '1238':'ifttt is abnormal',
            '1239':'Conditions of configuration != correct',
            '1300':'The data is in operation',
            '2001':'Get developer list error',
            '2002':'Appid or Appkey illegal',
            '2003':'AuthCode incorrect',
            '2004':'AccessToken incorrect',
            '2005':'AccessToken expired',
            '2006':'RefreshToken incorrect',
            '2007':'RefreshToken expired',
            '2008':'Permission denied',
            '2009':'Invalid OpenId',
            '2010':'Unauthorized user',
            '2011':'The query result is empty',
            '2012':'Invalid apply',
            '2013':'Developer Permission denied',
            '2014':'Resource Permission denied',
            '2015':'subscriber faild',
            '2016':'AccountId has exist',
            '2017':'Appkey exceeds the limit',
            '2018':'IP config exceed the limit',
            '2022':'Application not activated',
        }

        if error_code:
            error_message = error_map.get(error_code)
            if error_message:
                raise ValueError(f"Received Error - code: {str(error_code)} => {error_message}")
            else:
                raise ValueError(f"Received unknown error code: {str(error_code)}")


