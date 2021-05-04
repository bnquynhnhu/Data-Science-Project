import os
basedir = os.path.abspath(os.path.dirname(__file__))

HOST = "https://www.airdna.co"
HOST1 = "https://api.airdna.co"
VERSION_CLIENT = "v1"
CLIENT_TOKEN = "MjkxMTI|8b0178bf0e564cbf96fc75b8518a5375"

myLoginData = {
    'username': 'phutranho@gmail.com',
    'password': 'a1b2c3d4',
    'remember_me': 'true',
    'cache-control': 'no-cache',
    'accept-language': 'fr,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/x-www-form-urlencoded'
}

myLoggedInData = {
    'cache-control': 'no-cache',
    'accept-language': 'fr,en-US;q=0.9,en;q=0.8'
}

pushLoginURL = f"{HOST}/api/{VERSION_CLIENT}/account/login"
pushLoggedinURL = f"{HOST}/api/{VERSION_CLIENT}/account/refresh"
areaLookupURL = f"{HOST1}/{VERSION_CLIENT}/market/area_lookup?"
propertyList = f"{HOST1}/{VERSION_CLIENT}/market/property_list?"
token = ""
