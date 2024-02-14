export async function rpc_call(endpoint, body={}){
    try {
        const response = await fetch(endpoint)

        if(!response.ok){
            throw new Error('Error')
        }

        return await response.json()
    }catch(error) {
        console.error('SmartHome RPC Failed -', error)
    }
}