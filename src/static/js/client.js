export class APIClient {
    static hostname = ""
    static deviceList = []
    static settings = {}
    static API_METHOD_GET = 0
    static API_METHOD_POST = 1

    static init(hostname){
        this.hostname = hostname
    }

    static async rpc_getDevice(deviceId){
        const data = await APIClient.rpc_call(`http://${APIClient.hostname}/devices/${deviceId}`)
        console.log(data)
        return data
    }

    static async rpc_getDeviceList(){
        const data = await APIClient.rpc_call(`http://${APIClient.hostname}/devices`)
        this.deviceList = data
        return data
    }

    static async rpc_updateDevice(deviceId, properties){
        console.log("updating properties: ", properties)
        const data = await APIClient.rpc_call(`http://${APIClient.hostname}/devices/${deviceId}`, properties, APIClient.API_METHOD_POST)
        return data
    }

    /* ********** AUTOMATION ************* */
    static async rpc_getAutomationList(){
        const data = await APIClient.rpc_call(`http://${APIClient.hostname}/automations`)
        return data
    }

    static async rpc_getAutomation(automationId){
        const data = await APIClient.rpc_call(`http://${APIClient.hostname}/automations/${automationId}`)
        return data
    }

    static async rpc_enableAutomation(automationId){
        const data = await APIClient.rpc_call(`http://${APIClient.hostname}/automations/${automationId}/enable`, {'test':'test'}, APIClient.API_METHOD_POST)
        return data
    }

    static async rpc_disableAutomation(automationId){
        const data = await APIClient.rpc_call(`http://${APIClient.hostname}/automations/${automationId}/disable`, {'test':'test'}, APIClient.API_METHOD_POST)
        return data
    }

    static async rpc_getAutomationLog(automationId){
        const data = await APIClient.rpc_call(`http://${APIClient.hostname}/automations/${automationId}/getLog`)
        return data
    }


    /* ********** AQARA UTILS ************* */
    static async rpc_generateAuthCode(duration){
        return await APIClient.rpc_call(`http://${APIClient.hostname}/aqara/generate_auth_code?duration=${duration}`)
    }

    static async rpc_generateAccessToken(authCode){
        return await APIClient.rpc_call(`http://${APIClient.hostname}/aqara/generate_access_token?authCode=${authCode}`)
    }

    /* ************** UITL ************** */

    
    static async rpc_getSettings(){
        const data = await APIClient.rpc_call(`http://${APIClient.hostname}/settings/get_properties`)
        APIClient.settings = data
        return data
    }

    static async rpc_call(endpoint, body={}, method=APIClient.API_METHOD_GET){
        try {
            let response = null
            switch(method){
                case APIClient.API_METHOD_GET:
                    response = await fetch(endpoint)
                    break;
                case APIClient.API_METHOD_POST:
                    response = await fetch(endpoint, {
                        body: JSON.stringify(body), 
                        method: "POST", 
                        headers: {
                            'Content-Type': "application/json"
                        }
                    })
                    break;
            }
            
            if(!response.ok){
                throw new Error('Error')
            }
    
            return await response.json()
        }catch(error) {
            console.error('SmartHome RPC Failed -', error)
        }
    }
}