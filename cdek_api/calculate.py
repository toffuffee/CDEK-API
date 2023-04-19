# import arrow
# import json
# import requests
# from auth import auth
# import config


# URL = config.URL

# def request_header():
#     authen = auth()
#     access_token = ''
#     if authen.get('access_token'):
#         access_token = authen['access_token']  
#         return {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {access_token}'
#         }
#     else:
#         False


# def calculate(from_location,to_location,width,height,length,weigth):
#     url = f"{URL}calculator/tarifflist"
#     print(url)
#     header=request_header()
#     if header:
#         payload = json.dumps({
#                             "type": 2,
#                             "date": ''.join(str(arrow.now().to('UTC')).split('.')[0])+"+0000",
#                             "currency": 1,
#                             "lang": "rus",
#                             "from_location": {
#                                 "code": from_location
#                             },
#                             "to_location": {
#                                 "code": to_location
#                             },
#                             "packages": [
#                                 {
#                                 "height": height,
#                                 "length": length,
#                                 "weight": weigth,
#                                 "width": width
#                                 }
#                             ]
#                             })
        
#         response = requests.request("POST", url, headers=header, data=payload)
        
#         return response.json()
#     else:
#         return []


