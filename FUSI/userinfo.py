import requests
import DATA.common_globals as cg


def userinfo(fid):
    url = "https://cpapi.footseen.xyz/zone/userInfo/dataCard"
    querystring = {"lang": "1",
                   "os": "h5",
                   "cid": "ftsH5",
                   "webVersion": "1000",
                   "fid": fid,
                   "pageID": "f1834356ff22ff0569ec9d608e521b4a"}
    headers = {"referer": "https://www.footseen.xyz/"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()

    try:
        nick = response['zoneInfo']['nickname']
        country = response['zoneInfo']['addr']
        text = (f'{fid} | {nick}'
                f'\nCOUNTRY : {country}')
    except KeyError:
        text = None

    return text
