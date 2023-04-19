# import requests
# import json

# from auth import auth
# import config
# URL = config.URL

# class CDEKCities():
#     def request_header(self):
#         authen = auth()
#         access_token = ''
#         if authen.get('access_token'):
#             access_token = authen['access_token']  
#             return {
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {access_token}'
#             }
#         else:
#             False


#     def get_cities_list(self,city):
#         url = f"{URL}location/cities?city={city}"
#         print(url)
#         header=self.request_header()
#         if header:
#             response = requests.request("GET", url, headers=header)
#             return response.json()
#         else:
#             return []

        
#     def all_cities(self):
#         url = f"{URL}location/cities/?country_codes=RU"
#         header=self.request_header()
#         if header:
#             response = requests.request("GET", url, headers=header)
#             print(response)
#             return response.json()
#         else:
#             return []

#     def all_regions(self):
#         url = f"{URL}location/regions/?country_codes=RU"
#         header=self.request_header()
#         if header:
#             response = requests.request("GET", url, headers=header)
#             return response.json()
#         else:
#             return []