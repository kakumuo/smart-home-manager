import math
import random
from aqara.aqdevice import AqaraMotionSensor
from aqara.client import AqaraClient
from aqara.session import AqaraSession
from aqara.queue import AqaraQueueClient
import time


import subprocess
import json
import threading


from tapo import ApiClient
from atapo.tpdevice import TapoSmartBulb
from atapo.client import TapoClient
import asyncio

import configparser

from device.automation import AutomationTask, SmartHomeAutomation, TaskLink, UpdateTaskAction

def aqaraTest():

    # serverConfig = configparser.ConfigParser()
    # serverConfig.read("etc\\config.properties")

    # aqaraSession:AqaraSession = AqaraSession.generateSession(None)
    # aqaraSession.appId =        serverConfig.get('Aqara', 'appId')
    # aqaraSession.keyId =        serverConfig.get('Aqara', 'keyId')
    # aqaraSession.appKey =       serverConfig.get('Aqara', 'appKey')
    # aqaraSession.accessToken =  serverConfig.get('Aqara', 'accessToken')
    # aqaraSession.refreshToken = serverConfig.get('Aqara', 'refreshToken')
    # aqaraSession.expiresIn =    serverConfig.get('Aqara', 'expiresIn')
    # aqaraSession.timestamp =    serverConfig.get('Aqara', 'timestamp')
    # aqaraUsername =             serverConfig.get('Aqara', 'username')

    # aqaraSession.queueAccessKey = serverConfig.get('Aqara', 'queueAccessKey')
    # aqaraSession.queueBrokerName = serverConfig.get('Aqara', 'queueBrokerName')
    # aqaraSession.queueSecret = serverConfig.get('Aqara', 'queueSecret')
    # aqaraSession.queueServer = serverConfig.get('Aqara', 'queueServer')
    # aqaraSession.queueTopic = serverConfig.get('Aqara', 'queueTopic')


    # client = AqaraClient()
    # # session = client.getAuthCode(userName, session)
    # aqaraSession = client.refreshToken(aqaraSession)
    # deviceList = client.getDevices(aqaraSession)

    # motionSensorDevice:AqaraMotionSensor = deviceList[0]

    # queueClient = AqaraQueueClient(aqaraSession)
    # queueClient.addDevice(motionSensorDevice)
    # queueClient.start()

#     queueTopic = 116919905883855667241b3f
# queueAccessKey = K.1169199058872111104
# queueSecret = lc4levem8p64n1clkc2pmlwtxsxac81e
    
    # Run your command here
    command:str = " ".join([
        "lib\\rocketmq-all-5.1.4-bin-release\\bin\\mqadmin.cmd",
        "consumeMessage" ,
        "-b broker-a",
        "-g {}".format("116919905883855667241b3f"),
        "-t {}".format("116919905883855667241b3f"),
        "-n {}".format("uspro-opdmq-broker1.aqara.com:9876"),
        "-s {}".format(round(time.time() * 1000)) 
    ])
    print(command)
    # command = "lib\\rocketmq-all-5.1.4-bin-release\\bin\\mqadmin.cmd consumeMessage -b broker-a -g 116919905883855667241b3f -t 116919905883855667241b3f -n uspro-opdmq-broker1.aqara.com:9876 -i 2"
    # print(command)
    command_output = subprocess.check_output(command, universal_newlines=True)
    print(command_output)

aqaraTest()

async def tapoTest():
    # Read the properties file
    file_path = 'etc/config.properties'  # Update with your file path
    ip_address = "192.168.0.166"

    testConfig = configparser.ConfigParser()
    testConfig.read(file_path)

    username = testConfig.get('Tapo', 'username')
    password = testConfig.get('Tapo', 'password')

    client = ApiClient(username, password)
    device = await client.l510(ip_address)
    jsonDetails = await device.get_device_info_json()

    smartBulb:TapoSmartBulb = TapoSmartBulb(jsonDetails)
    print(smartBulb)

    # print(f"device info: {device.get_device_info()}") 

    # print("Turning device off...")
    # await device.off()

    # print("Waiting 2 seconds...")
    # await asyncio.sleep(2)

    # print("Turning device on...")
    # await device.on()

    # device_info = await device.get_device_info()
    # print(f"Device info: {device_info.to_dict()}")

    # device_usage = await device.get_device_usage()
    # print(f"Device usage: {device_usage.to_dict()}")
    pass

# loop = asyncio.get_event_loop()
# loop.run_until_complete(tapoTest())


# def tapoTest2():
#     # Read the properties file
#     file_path = 'etc/config.properties'  # Update with your file path
#     ip_address = "192.168.0.166"

#     testConfig = configparser.ConfigParser()
#     testConfig.read(file_path)

#     username = testConfig.get('Tapo', 'username')
#     password = testConfig.get('Tapo', 'password')

#     tapoClient = TapoClient(username, password)
#     tapoClient.doLogin()
#     tapoClient.getDevices()

#     print(f"Tapo Devices: {tapoClient.devices[0]}")

# tapoTest2()



def configTest():
    filePath = "etc\\devices.properties"
    testConfig = configparser.ConfigParser()
    testConfig.read(filePath)

    for ipAddress, deviceProp in testConfig['Tapo'].items():
        print(ipAddress, deviceProp)

# configTest()
        


# def automationTest():

#     # Read the properties file
#     file_path = 'etc/config.properties'  # Update with your file path
#     ipAddress = "192.168.0.166"
#     deviceType = "L530"

#     ipAddress2 = "192.168.0.142"
#     ipAddress3 = "192.168.0.235"

#     testConfig = configparser.ConfigParser()
#     testConfig.read(file_path)

#     username = testConfig.get('Tapo', 'username')
#     password = testConfig.get('Tapo', 'password')

#     tapoClient = TapoClient(username, password)
#     tapoClient.doLogin()
#     targetBulb1 = tapoClient.createDevice(ipAddress , deviceType)
#     targetBulb2 = tapoClient.createDevice(ipAddress2 , deviceType)
#     targetBulb3 = tapoClient.createDevice(ipAddress3 , deviceType)


#     automationProperties:dict = {
#         "name": "Something",
#         "created": 123456
#     }

#     targetBri = random.randint(10, 30)

#     testAuto:SmartHomeAutomation = SmartHomeAutomation(automationProperties)

#     task1:AutomationTask = AutomationTask(targetBulb1)
#     task1.addAction(UpdateTaskAction('bri', targetBri))
    
#     task2:AutomationTask = AutomationTask(targetBulb2)
#     task2.addAction(UpdateTaskAction('isOn', False))

#     task3:AutomationTask = AutomationTask(targetBulb3)
#     task3.addAction(UpdateTaskAction('bri', targetBri))

#     testAuto.addTask([task2, task3])
#     testAuto.addLink(TaskLink(1, 2))

#     testAuto.setRoot(task1)
#     testAuto.run()

#     pass

# automationTest()


"""
 'avatar': 'bulb', 'brightness': 2, 'color_temp': 2500, 'color_temp_range': [2500, 6500], 'default_states': {'re_power_type': 'always_on', 'state': {'brightness': 2, 'color_temp': 2500, 'hue': 0, 'saturation': 0}, 'type': 'last_states'}, 'device_id': '80235CA0FF2FDFBB1BECEA40CBEB4A952128F998', 'device_on': True, 'dynamic_light_effect_enable': False, 'fw_id': '00000000000000000000000000000000', 'fw_ver': '1.1.0 Build 230721 Rel.224802', 'has_set_location_info': True, 'hue': 0, 'hw_id': 'FDE1C68674D1535B12A042682B192E4E', 'hw_ver': '2.0', 'ip': '192.168.0.142', 'lang': 'en_US', 'latitude': 407159, 'longitude': -740784, 'mac': '78-8C-B5-A9-FD-B5', 'model': 'L530', 'nickname': 'Ym90dG9tIGxhbXA=', 'oem_id': '90171A8CAC7DBD1A9BE64C1449D24A6A', 'overheated': False, 'region': 'America/New_York', 'rssi': -59, 'saturation': 0, 'signal_level': 2, 'specs': '', 'ssid': 'bGlsIGJpc2ggMi40Rw==', 'time_diff': -300, 'type': 'SMART.TAPOBULB'}
"""
# def bulbColorTest():
#     # Read the properties file
#     file_path = 'etc/config.properties'  # Update with your file path
#     ipAddress = "192.168.0.142"
#     deviceType = "L530"

#     testConfig = configparser.ConfigParser()
#     testConfig.read(file_path)

#     username = testConfig.get('Tapo', 'username')
#     password = testConfig.get('Tapo', 'password')

#     tapoClient = TapoClient(username, password)
#     tapoClient.doLogin()
#     # targetBulb1 = tapoClient.createDevice(ipAddress , deviceType)

#     async def test():
#         targetBulb1 = await tapoClient.clientHelper.l510(ipAddress)
#         res = await targetBulb1.off()
#         print("response: ", res)
    
#     loop = asyncio.new_event_loop()
#     loop.run_until_complete(test())

#     pass

# bulbColorTest()