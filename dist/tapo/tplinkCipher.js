import * as crypto from 'crypto';
export class TapoCrypto {
}
TapoCrypto.RSA_CIPHER_ALGORITHM = "rsa";
TapoCrypto.AES_CIPHER_ALGORITHM = 'aes-128-cbc';
TapoCrypto.PASSPHRASE = "top secret";
TapoCrypto.generateKeyPair = () => {
    let RSA_OPTIONS = {
        modulusLength: 1024,
        publicKeyEncoding: {
            type: 'spki',
            format: 'pem'
        },
        privateKeyEncoding: {
            type: 'pkcs1',
            format: 'pem',
            cipher: 'aes-256-cbc',
            passphrase: TapoCrypto.PASSPHRASE
        }
    };
    const keyPair = crypto.generateKeyPairSync(TapoCrypto.RSA_CIPHER_ALGORITHM, RSA_OPTIONS);
    return {
        key: keyPair.publicKey,
        privateKey: keyPair.privateKey,
        iv: crypto.randomBytes(16)
    };
};
TapoCrypto.encrypt = (data, deviceKey) => {
    var cipher = crypto.createCipheriv(TapoCrypto.AES_CIPHER_ALGORITHM, deviceKey.key, deviceKey.iv);
    var ciphertext = cipher.update(Buffer.from(JSON.stringify(data)));
    return Buffer.concat([ciphertext, cipher.final()]).toString('base64');
};
TapoCrypto.decrypt = (data, deviceKey) => {
    var cipher = crypto.createDecipheriv(TapoCrypto.AES_CIPHER_ALGORITHM, deviceKey.key, deviceKey.iv);
    var ciphertext = cipher.update(Buffer.from(data, 'base64'));
    return JSON.parse(Buffer.concat([ciphertext, cipher.final()]).toString());
};
TapoCrypto.readDeviceKey = (pemKey, privateKey) => {
    let keyBytes = Buffer.from(pemKey, 'base64');
    let deviceKey = crypto.privateDecrypt({
        key: privateKey,
        padding: crypto.constants.RSA_PKCS1_PADDING,
        passphrase: TapoCrypto.PASSPHRASE,
    }, keyBytes);
    return deviceKey;
};
TapoCrypto.base64Encode = (data) => {
    return Buffer.from(data).toString('base64');
};
TapoCrypto.base64Decode = (data) => {
    return Buffer.from(data, 'base64').toString();
};
TapoCrypto.shaDigest = (data, hashType = 0) => {
    const targetHash = ['sha1', 'sha256'][hashType];
    var shasum = crypto.createHash(targetHash);
    shasum.update(data);
    return shasum.digest('hex');
};
//# sourceMappingURL=tplinkCipher.js.map