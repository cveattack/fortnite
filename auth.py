import os
import time
import requests
import datetime
import webbrowser
import platform
import json
import time

class endpoints:
    token = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
    redirect = "https://www.epicgames.com/id/login?redirectUrl=https%3A//www.epicgames.com/id/login%3FredirectUrl%3Dhttps%253A%252F%252Fwww.epicgames.com%252Fid%252Fapi%252Fredirect%253FclientId%253Dec684b8c687f479fadea3cb2ad83f5c6%2526responseType%253Dcode"
    pc_client = "ZWM2ODRiOGM2ODdmNDc5ZmFkZWEzY2IyYWQ4M2Y1YzY6ZTFmMzFjMjExZjI4NDEzMTg2MjYyZDM3YTEzZmM4NGQ"
    ios_client = "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE"
    exchange = "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/exchange"
    switchtoken = "OThmN2U0MmMyZTNhNGY4NmE3NGViNDNmYmI0MWVkMzk6MGEyNDQ5YTItMDAxYS00NTFlLWFmZWMtM2U4MTI5MDFjNGQ3"
    iostoken = "MzQ0NmNkNzI2OTRjNGE0NDg1ZDgxYjc3YWRiYjIxNDE6OTIwOWQ0YTVlMjVhNDU3ZmI5YjA3NDg5ZDMxM2I0MWE="

class account:
    name:str = None
    id:str = None
    secret:str = None
    deviceid:str = None
    authcode:str = None
    token:str = None
    accesstoken:str = None
    _authlink:str = None
    _devicecode1:str = None
	
class auth:
    def __init__(self) -> None:
        self.account = account()
        self.session = requests.session()
        self.session.headers = {'User-Agent':f'komaruontop/1.0 {platform.system()}/{platform.version()}'}

    def getauthlink(self) -> str:
        with self.session.post(
            "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"basic {endpoints.switchtoken}",
            },
            data={
                "grant_type": "client_credentials",
            },
        ) as request:
            data = request.json()

        self.account.accesstoken = data["access_token"]
        devicecode = self.createdevicecode()
        self.account._devicecode1 = devicecode[1]
        return f"https://www.epicgames.com/activate?userCode={devicecode[0]}"

    def wait_for_device_code_completion(self) -> None:
        while True:
            with self.session.post(
                "https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
                headers={
                    "Authorization": f"basic {endpoints.switchtoken}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={"grant_type": "device_code", "device_code": self.account._devicecode1},
            ) as request:
                token = request.json()

                if request.status_code == 200:
                    break
                else:
                    if (
                        token["errorCode"]
                        == "errors.com.epicgames.account.oauth.authorization_pending"
                    ):
                        pass
                    elif token["errorCode"] == "errors.com.epicgames.not_found":
                        pass
                    else:
                        print(json.dumps(token, sort_keys=False, indent=4))

                time.sleep(5)

        with self.session.get(
            url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/exchange",
            headers={"Authorization": f"bearer {token['access_token']}"},
        ) as request:
            exchange = request.json()

        with self.session.post(
            url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
            headers={
                "Authorization": f"basic {endpoints.iostoken}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "exchange_code",
                "exchange_code": exchange["code"],
            },
        ) as request:
            auth_information = request.json()

            self.account.token = auth_information['access_token']
            self.account.id = auth_information['account_id']
            self.account.name = auth_information['displayName']

    def getaccountmetadata(self) -> dict:
        with self.session.get(
            f'https://account-public-service-prod03.ol.epicgames.com/account/api/public/account/displayName/{self.account.name}',
            headers={"Authorization": f"bearer {self.account.token}"}
        ) as r:
            data = r.json()
        return data

    def createdevicecode(self) -> tuple[str,str]:
        with self.session.post(
            'https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/deviceAuthorization',
            headers={
                "Authorization": f"bearer {self.account.accesstoken}",
                "Content-Type": "application/x-www-form-urlencoded",
            },

        ) as r:
            data = r.json()
        return data["user_code"], data["device_code"]