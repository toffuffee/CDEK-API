# import requests
# import config


# def auth():
#     url = f"{config.URL}/oauth/token?parameters&grant_type=client_credentials&client_id={config.CLIENT_ID}&client_secret={config.CLIENT_SECRET}"
#     payload = ""
#     headers = {}
#     response = requests.request("POST", url, headers=headers, data=payload)
#     return response.json()