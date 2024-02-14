import * as crypto from "crypto";
const APPID = "116919905883855667241b3f";
const KEYID = "K.1169199058872111104";
const APPKEY = "lc4levem8p64n1clkc2pmlwtxsxac81e";
export const generateSession = (oldSession) => {
    let appId = APPID;
    let token = oldSession === null || oldSession === void 0 ? void 0 : oldSession.accessToken;
    let keyId = KEYID;
    let appKey = APPKEY;
    let time = Math.round(new Date().getTime());
    let nonce = Math.round(new Date().getTime());
    // console.log("generate session: session details: ", oldSession)
    var preSign = "";
    if (token != null && token != "" && token != undefined) {
        preSign = "Accesstoken=" + token + "&";
    }
    preSign = preSign + "Appid=" + appId + "&" + "Keyid=" + keyId + "&" + "Nonce=" + nonce + "&" + "Time=" + time + appKey;
    console.log("presign: ", preSign);
    let hash = crypto.createHash('md5');
    hash.update(preSign.toLowerCase());
    let sign = hash.digest().toString('hex');
    // console.log(`generated sign: ${sign}`)
    let session;
    if (oldSession != null) {
        session = oldSession;
        session.nonce = nonce.toString();
        session.time = time.toString();
        session.sign = sign;
        session.accessToken = token;
    }
    else {
        session = {
            appId: APPID,
            keyId: KEYID,
            nonce: nonce.toString(),
            appKey: APPKEY,
            sign: sign,
            time: time.toString(),
            accessToken: token
        };
    }
    return session;
};
//# sourceMappingURL=aqaraCrypto.js.map