import hashlib
import time

class AqaraSession:
    def __init__(self, appId: str, keyId: str, nonce: str, appKey: str, sign: str, time: str, accessToken:str=None):
        self.appId = appId
        self.keyId = keyId
        self.nonce = nonce
        self.appKey = appKey
        self.sign = sign
        self.time = time
        self.accessToken = accessToken
        self.authCode =''
        self.refreshToken =''
        self.openId =''
        self.expiresIn =''
        self.timestamp =0
        self.queueServer = ''
        self.queueTopic = ''
        self.queueAccessKey = ''
        self.queueSecret = ''
        self.queueBrokerName = ''

    def generateSession(old_session):
        APPID = "116919905883855667241b3f"
        KEYID = "K.1169199058872111104"
        APPKEY = "lc4levem8p64n1clkc2pmlwtxsxac81e"

        appId = APPID
        token = old_session.accessToken if old_session else None
        keyId = KEYID
        appKey = APPKEY
        current_time = str(round(time.time() * 1000))  # Convert current time to milliseconds
        nonce = str(round(time.time() * 1000))  # Convert current time to milliseconds

        pre_sign = ""
        if token is not None and token != "":
            pre_sign = f"Accesstoken={token}&"

        pre_sign += f"Appid={appId}&Keyid={keyId}&Nonce={nonce}&Time={current_time}{appKey}"
        print("presign: ", pre_sign)
        
        hash_object = hashlib.md5(pre_sign.lower().encode())
        sign = hash_object.hexdigest()

        if old_session is not None:
            old_session.nonce = nonce
            old_session.time = current_time
            old_session.sign = sign
            old_session.accessToken = token
            session = old_session
        else:
            session = AqaraSession(
                appId=APPID,
                keyId=KEYID,
                nonce=nonce,
                appKey=APPKEY,
                sign=sign,
                time=current_time,
                accessToken=token
            )

        return session
