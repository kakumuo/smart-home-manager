from tapo import ApiClient
from atapo.tpdevice import TapoDevice, TapoSmartBulb

import requests
import json
import uuid
import subprocess
import asyncio


class TapoClient :

    def __init__(self, username:str, password:str):
        self.username:str = username
        self.password:str = password
        self.temrinalUuid:str = str(uuid.uuid4())
        self.loginDetails = {}
        self.devices = []
        self.clientHelper:ApiClient = ApiClient(username, password)

    def execEndpoint(self, endpoint, headers, data, method):
        hostname = endpoint

        print(f"Data: {json.dumps(data)}")
        print(f"Headers: {json.dumps(headers)}")
        response = requests.request(
            method,
            f"https://{hostname}",
            headers=headers,
            data=json.dumps(data)
        )

        print("Response Status Code:", response.status_code)

        if response.status_code == 200:
            return response.json()
        else:
            # Handle other status codes here if needed
            print("Error:", response.text)
            return None
    
    def doLogin(self):
        data = {
            "method": "login",
            "params": {
            "appType": "Tapo_Android",
            "cloudUserName": self.username,
            "cloudPassword": self.password,
            "terminalUUID": self.temrinalUuid
            }
        }

        headers = {}
        response = self.execEndpoint('wap.tplinkcloud.com', headers, data, "POST")
        if response is not None:
            self.loginDetails = response
        pass

    def getDevices(self) -> list[TapoDevice]:
        data = {
            "method": "getDeviceList",
            "params": {
                "token": self.loginDetails['result']['token']
            }
        }

        headers = {
            "token": self.loginDetails['result']['token']
        }

        response = self.execEndpoint('wap.tplinkcloud.com', headers, data, "POST")

        # # ping all devices on lowest end of the network so that arp -a command will pick them
        # for i in range(1, 256):
        #     ip_address = f"192.168.0.{i}"
        #     # Ping the IP address with a single ICMP packet and a timeout of 1 second
        #     subprocess.run(f"ping -n 1 -w 1 {ip_address}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


        for device in response['result']['deviceList']:
            if device['deviceType'] != 'SMART.TAPOBULB':
                continue

            deviceName:str = device['deviceName']
            deviceMac:str = device['deviceMac']

            # separate the device mac ex: 11AA22BB33CC -> 11-AA-22-BB-33-CC
            deviceMac = '-'.join([deviceMac[i:i+2] for i in range(0, len(deviceMac), 2)])
                
            # get ip addresses from mac info
            ipAddress = self.getIpFromMac(deviceMac)
            print(f'device: {deviceName}; Source Mac: {deviceMac}; TargetIp: {ipAddress}')
            if(ipAddress):
                device = self.createDevice(ipAddress, deviceName)
                if(device):
                    self.devices.append(device)
        return self.devices

    def getIpFromMac(self, mac_address:str):
        # Execute the system command to fetch ARP table
        arp_table = subprocess.run(['arp', '-av'], capture_output=True, text=True)

        # Parse the ARP table output to find the IP for the given MAC address
        lines = arp_table.stdout.splitlines()
        for line in lines:
            if mac_address.lower() in line.lower():  # Check if MAC address is present in the line
                parts = line.split()
                ip_address = parts[0]  # Extract the IP address
                return ip_address

        return None  # If MAC address not found
    
    
    def createDevice(self, ipAddress:str, deviceType:str):
        async def createDeviceHelper(ipAddress:str, deviceType:str):
            targetDevice = None
            deviceDetails = None
            deviceMap = {
                'L530': self.clientHelper.l510,
                'L930': self.clientHelper.l610,
                'L920': self.clientHelper.l610,
            }
            if deviceType in deviceMap:
                targetDevice =  await deviceMap[deviceType](ipAddress)
                deviceDetails = await targetDevice.get_device_info_json()
                return TapoSmartBulb(deviceDetails, targetDevice)
            return None
        
        loop = asyncio.new_event_loop()
        device = loop.run_until_complete(createDeviceHelper(ipAddress, deviceType))
        return device

    def updateDevice(self, device:TapoSmartBulb, properties:dict):
        async def updateDeviceHelper(device:TapoSmartBulb):
            if 'bri' in properties:
                await device.lightHandler.set_brightness(int(properties['bri']))

            if 'isOn' in properties:
                await device.lightHandler.on() if  properties['isOn'] else device.lightHandler.off()

            deviceInfo  = await device.lightHandler.get_device_info_json()
            device.updateDeviceState(deviceInfo)

        loop = asyncio.new_event_loop()
        loop.run_until_complete(updateDeviceHelper(device))
        pass

    pass