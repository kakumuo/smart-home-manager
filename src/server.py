import subprocess
import threading
from flask import Flask, request, render_template

from aqara.aqdevice import AqaraDevice, AqaraMotionSensor
from aqara.client import AqaraClient
from aqara.session import AqaraSession

from tapo import ApiClient
from atapo.tpdevice import TapoDevice, TapoSmartBulb
from device.automation import SmartHomeAutomation, SmartHomeAutomationJsonEncoder
from device.smartDevice import SmartDevice, DeviceProperty, SmartDeviceJsonEncoder
from atapo.client import TapoClient

import time
import configparser
import json

class SHServer:
    app = Flask(__name__)
    serverConfig = configparser.ConfigParser()
    devicePropertiesConfig = configparser.ConfigParser()
    autosPropertiesConfig = configparser.ConfigParser()

    """AQARA DETIALS"""
    aqaraClient:AqaraClient 
    aqaraSession:AqaraSession 
    aqaraDevices:list[AqaraDevice]
    aqaraAuthDuration:str = ""
    aqaraUsername:str = ""
    propertiesFilePath:str = "./etc/config.properties"
    devicePropertiesFilePath:str = "./etc/devices.properties"
    autosPropertiesFilePath:str = "./etc/autos.properties"

    """ TAPO DETAILS"""
    tapoClient:TapoClient
    tapoDevices:list[TapoSmartBulb]

    """ Smart Home Automations """
    shAutomations:list[SmartHomeAutomation] = []

    deviceList:list[SmartDevice] = []

    @app.route('/')
    def route_index():
        return render_template('index.html')

    @app.route('/devices')
    def route_getDeviceList():
        if request.method == "GET":
            output = json.dumps(SHServer.deviceList, cls=SmartDeviceJsonEncoder)
            print(f"Response from /devices: {output}")
            return output

    
    @app.route('/devices/<deviceId>', methods=["GET", "POST"])
    def route_deviceById(deviceId):
        def findDevice(id:int, list:list[SmartDevice]) -> SmartDevice:
            for d in list:
                if d.deviceId.value == id:
                    return d
            return None

        output = "{}"
        targetDevice:SmartDevice = findDevice(int(deviceId), SHServer.deviceList)
        if targetDevice is None:
            return output
        elif request.method == "POST":
            deviceJson:dict = request.get_json()
            print("Updateing device - Json: ", deviceJson)
            if isinstance(targetDevice, TapoSmartBulb):
                SHServer.tapoClient.updateDevice(targetDevice, deviceJson)

        output = json.dumps(targetDevice, cls=SmartDeviceJsonEncoder)
        return output
        
    
    @app.route('/settings/get_properties')
    def route_getSettingsProperties():
        configDict = {section: dict(SHServer.serverConfig[section]) for section in SHServer.serverConfig.sections()}
        jsonOutput = json.dumps(configDict)
        # print("/settings/get_properties - ", jsonOutput)
        return jsonOutput

    
    """ ************** Aqara ************** """
    @app.route('/aqara/generate_auth_code')
    def route_generateAuthCode():
        duration:str = request.args.get('duration',"1h")
        SHServer.aqaraSession = SHServer.aqaraClient.getAuthCode(SHServer.aqaraUsername, SHServer.aqaraSession, 0, duration)
        return "{}"
    
    @app.route('/aqara/generate_access_token')
    def route_generateAccessToken():
        authCode:str = request.args.get('authCode',None)
        SHServer.updateAqaraToken(authCode)
        print(f"new access token; {SHServer.aqaraSession.accessToken}")
        return "{}"
    
    
    @app.route("/rocketmq", methods=["POST"])
    def rocketMqListen():
        if request.method == "POST":
            body:dict = request.get_json()

            sensor:AqaraMotionSensor = SHServer.aqaraDevices[0]
            for detail in body['data']:
                sensor.updateDeviceState(detail)
            """
            {
                "data": [
                    {
                    "attach": "broker-a",
                    "model": "lumi.motion.agl001",
                    "resourceId": "0.4.85",
                    "statusCode": 0,
                    "subjectId": "lumi1.54ef4452dbea",
                    "time": "1704643345440",
                    "triggerSource": {
                        "time": "1704643345",
                        "type": 10
                    },
                    "value": "33"
                    }
                ],
                "msgId": "AC1424B6001E18B4AAC222574A145FA11",
                "msgType": "resource_report",
                "openId": "531372067721169568896721842177",
                "time": "1704643345954"
            }
            """

            return {}
        else:
            return {'status': 'invalid method'}


    """ ************* TAPO *************** """

    """ ********* Automations ************ """
    @app.route("/automations", methods=["GET"])
    def getAutomations():
        output = json.dumps(SHServer.shAutomations,  cls=SmartHomeAutomationJsonEncoder)
        print("response from /automations: ", output)
        return output
    
    @app.route("/automations/<automationId>", methods=["GET"])
    def getAutomation(automationId):
        targetAuto:SmartHomeAutomation = None
        for automation in SHServer.shAutomations:
            if str(automation.automationId) == automationId:
                targetAuto = automation
                break
        output = json.dumps(targetAuto,  cls=SmartHomeAutomationJsonEncoder)
        print(f"response from /automations/{automationId}: ", output)
        return output
    
    @app.route("/automations/<automationId>/<toggle>", methods=["POST"])
    def toggleAutomation(automationId, toggle):
        targetAuto:SmartHomeAutomation = None
        for automation in SHServer.shAutomations:
            if str(automation.automationId) == automationId:
                targetAuto = automation
                break

        targetAuto.isRunning = toggle != 'disable'
        return json.dumps(targetAuto, cls=SmartHomeAutomationJsonEncoder)

    """ ************* General ************ """ 
    def loadProperties(filepath:str):
        SHServer.serverConfig.read(filepath)

        SHServer.aqaraSession.appId = SHServer.serverConfig.get('Aqara', 'appId')
        SHServer.aqaraSession.keyId = SHServer.serverConfig.get('Aqara', 'keyId')
        SHServer.aqaraSession.appKey = SHServer.serverConfig.get('Aqara', 'appKey')
        SHServer.aqaraSession.accessToken = SHServer.serverConfig.get('Aqara', 'accessToken')
        SHServer.aqaraSession.refreshToken = SHServer.serverConfig.get('Aqara', 'refreshToken')
        SHServer.aqaraSession.expiresIn = SHServer.serverConfig.get('Aqara', 'expiresIn')
        SHServer.aqaraSession.timestamp = SHServer.serverConfig.get('Aqara', 'timestamp')
        SHServer.aqaraUsername = SHServer.serverConfig.get('Aqara', 'username')

    def saveProperties(filepath:str):

        if not SHServer.serverConfig.has_section('Aqara'):
            SHServer.serverConfig.add_section('Aqara')
        if not SHServer.serverConfig.has_section('Tapo'):
            SHServer.serverConfig.add_section('Tapo')

        SHServer.serverConfig.set('Aqara', 'appId', SHServer.aqaraSession.appId)
        SHServer.serverConfig.set('Aqara', 'keyId', SHServer.aqaraSession.keyId)
        SHServer.serverConfig.set('Aqara', 'appKey', SHServer.aqaraSession.appKey)
        SHServer.serverConfig.set('Aqara', 'accessToken', str(SHServer.aqaraSession.accessToken))
        SHServer.serverConfig.set('Aqara', 'refreshToken', str(SHServer.aqaraSession.refreshToken))
        SHServer.serverConfig.set('Aqara', 'expiresIn', str(SHServer.aqaraSession.expiresIn))
        SHServer.serverConfig.set('Aqara', 'timestamp', str(SHServer.aqaraSession.timestamp))

        SHServer.serverConfig.set('Aqara', 'queueServer', str(SHServer.aqaraSession.queueServer))
        SHServer.serverConfig.set('Aqara', 'queueTopic', str(SHServer.aqaraSession.queueTopic))
        SHServer.serverConfig.set('Aqara', 'queueAccessKey', str(SHServer.aqaraSession.queueAccessKey))
        SHServer.serverConfig.set('Aqara', 'queueSecret', str(SHServer.aqaraSession.queueSecret))
        SHServer.serverConfig.set('Aqara', 'queueBrokerName', str(SHServer.aqaraSession.queueBrokerName))
    
        with open(filepath, 'w') as configfile:
            SHServer.serverConfig.write(configfile)
            
    def loadDeviceProperties(filepath:str):
        SHServer.devicePropertiesConfig.read(filepath)

    def saveDeviceProperties(filepath:str):
        pass

    def updateAqaraToken(authCode:str):
        if authCode == "" or authCode == None:
            print("refreshing token")
            SHServer.aqaraSession = SHServer.aqaraClient.refreshToken(SHServer.aqaraSession)
        else:
            print("getting token")
            SHServer.aqaraSession.authCode = authCode
            SHServer.aqaraSession = SHServer.aqaraClient.getAccessToken(SHServer.aqaraUsername, SHServer.aqaraSession)
        SHServer.saveProperties(SHServer.propertiesFilePath)
        
        pass
        
    def startServer():
        # init aquara client and session
        SHServer.aqaraClient = AqaraClient()
        SHServer.aqaraSession = AqaraSession.generateSession(None)
        SHServer.loadProperties(SHServer.propertiesFilePath)

        # refresh auth token on server start
        if round(time.time() * 1000) - float(SHServer.aqaraSession.timestamp) > float(SHServer.aqaraSession.expiresIn):
            SHServer.updateAqaraToken(None)

        # load aqara and tapo device properties
        SHServer.loadDeviceProperties(SHServer.devicePropertiesFilePath)

        # load initial aqara device state
        SHServer.aqaraDevices = SHServer.aqaraClient.getDevices(SHServer.aqaraSession)
        for aqaraDevice in SHServer.aqaraDevices:
            SHServer.aqaraClient.updateDeviceState(SHServer.aqaraSession, aqaraDevice)
        
        SHServer.tapoClient = TapoClient(SHServer.serverConfig.get('Tapo', 'username'), SHServer.serverConfig.get('Tapo', 'password'))
        SHServer.tapoClient.doLogin()
        SHServer.tapoDevices = []
        for ipAddress, deviceInfo in SHServer.devicePropertiesConfig['Tapo'].items():
            if SHServer.tapoDevices is None:
                SHServer.tapoDevices = []

            deviceInfoJson = json.loads(deviceInfo)
            device = SHServer.tapoClient.createDevice(ipAddress, deviceInfoJson['deviceType'])
            SHServer.tapoDevices.append(device)

        if SHServer.aqaraDevices is not None:
            SHServer.deviceList += SHServer.aqaraDevices
        if SHServer.tapoDevices is not None:
            SHServer.deviceList += SHServer.tapoDevices

            
        presenceAutomation:SHServer.PresenceAutomation = SHServer.PresenceAutomation("Presence Automation", SHServer.deviceList)
    
        # start aqara message listener process
        command:str = " ".join([
            "java"
            , "-jar"
            , "C:\\Users\\foxfe\\Documents\\Projects\\smart-home-manager\\lib\\rmqtest\\rmqtest.jar"
            , "http://127.0.0.1:5000/rocketmq"
        ])
        subprocess.Popen(command)

        SHServer.shAutomations.append(presenceAutomation)
        SHServer.app.run(debug=True, use_reloader=False)


    class PresenceAutomation (SmartHomeAutomation):
        def __init__(self, name, deviceList):
            super(SHServer.PresenceAutomation, self).__init__(name, deviceList)
            self.motionSensor:AqaraMotionSensor = None
            self.bulbs:list[TapoSmartBulb] = []

            for device in deviceList:
                if isinstance(device, AqaraMotionSensor):
                    self.motionSensor = device
                elif isinstance(device, TapoSmartBulb):
                    self.bulbs.append(device)
        
            self.motionSensor.addListener('presence', self.run)
            self.motionSensor.addListener('zone1Presence', self.run)
            self.motionSensor.addListener('zone2Presence', self.run)
            self.motionSensor.addListener('zone3Presence', self.run)

        def doUpdate(self, property:DeviceProperty):
            if not self.isRunning:
                return
            
            self.log(f"Detected property change {property.name} - {property.value}")
        
            for bulb in self.bulbs:
                if bulb.isOn.value != self.motionSensor.presence.value:
                    bulb.updateDevice({'isOn': self.motionSensor.presence.value})