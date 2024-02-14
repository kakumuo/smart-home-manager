/*
-------------------------------------- Step 1: splicing header parameters --------------------------------------
Accesstoken=532cad73c5493193d63d367016b98b27&Appid=4e693d54d75db580a56d1263&Keyid=k.78784564654feda454557&Nonce=C6wuzd0Qguxzelhb&Time=1618914078668

-------------------------------------- Step 2: Splicing appKey parameters --------------------------------------
Accesstoken=532cad73c5493193d63d367016b98b27&Appid=4e693d54d75db580a56d1263&Keyid=k.78784564654feda454557&Nonce=C6wuzd0Qguxzelhb&Time=1618914078668gU7Qtxi4dWnYAdmudyxni52bWZ58b8uN

-------------------------------------- Step 3: Lowercase the string ------------------------------------------
accesstoken=532cad73c5493193d63d367016b98b27&appid=4e693d54d75db580a56d1263&keyid=k.78784564654feda454557&nonce=c6wuzd0qguxzelhb&time=1618914078668gu7qtxi4dwnyadmudyxni52bwz58b8un

-------------------------------------- Step 4: MD5 32-bit encryption ----------------------------------------
bfd8dd0e7c108353e6740d81e05982d8
*/
import * as CryptoJS from "crypto-js";
import * as crypto from "crypto";
let params = "Accesstoken=532cad73c5493193d63d367016b98b27&Appid=4e693d54d75db580a56d1263&Keyid=k.78784564654feda454557&Nonce=C6wuzd0Qguxzelhb&Time=1618914078668gU7Qtxi4dWnYAdmudyxni52bWZ58b8uN";
const arr = ['base64', 'base64url', 'binary', 'hex'];
arr.forEach(element => {
    let hash = crypto.createHash('md5');
    hash.update(params.toLowerCase());
    console.log(`output - ${element}: ${hash.digest(element)}`);
});
console.log(`cryptojs - ${CryptoJS.MD5(params.toLowerCase()).toString()}`);
//# sourceMappingURL=test.js.map