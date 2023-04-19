# -*- coding: utf-8 -*-

import requests
import json
import logging
import datetime

def auth(URL, CLIENT_ID, CLIENT_SECRET):
    url = f"{URL}/oauth/token?parameters&grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
    payload = ""
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()



def request_header(URL, CLIENT_ID, CLIENT_SECRET):
    authen = auth(URL, CLIENT_ID, CLIENT_SECRET)
    access_token = ''
    if authen.get('access_token'):
        access_token = authen['access_token']  
        return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
        }
    else:
        False

# Калькулятор. Расчет по коду тарифа
def calculate(tarrif_code, city_get, city_admin, addres_get, addres_sender,width,height,length,weigth, URL, CLIENT_ID, CLIENT_SECRET):
    url = f"{URL}calculator/tariff"
    header=request_header(URL, CLIENT_ID, CLIENT_SECRET)
    if header:
        payload = json.dumps({
                            "type": 1,
                            "currency": 1,
                            "tariff_code": tarrif_code,
                            "from_location": {
		                        "country_code" : "RU",
		                        "city" : city_admin,
		                        "address" : addres_sender,
                            },
                            "to_location": {
		                        "country_code" : "RU",
		                        "city" : city_get,
		                        "address" : addres_get
                            },
                            "packages": [
                                {
                                "height": height,
                                "length": length,
                                "weight": weigth,
                                "width": width
                                },
                            ]
                            })
        
        response = requests.request("POST", url, headers=header, data=payload)
        return response.json()
    else:
        return []



def get_cities_list(city, URL, CLIENT_ID, CLIENT_SECRET):
    url = f"{URL}location/cities?city={city}"
    logging.info(url)
    header = request_header(URL, CLIENT_ID, CLIENT_SECRET)
    if header:
        response = requests.request("GET", url, headers=header)
        return response.json()
    else:
        return []
    
# Удаление заказа СДЕК
def deleteRequest(uuid, URL, CLIENT_ID, CLIENT_SECRET):
    url = f"{URL}orders/{uuid}"
    header=request_header(URL, CLIENT_ID, CLIENT_SECRET)
    if header:
        response = requests.request("DELETE", url, headers=header)
        return response.json()
    else:
        return []

# Удаление заказа курьера СДЕК
def deleteRequestCourier(uuid, URL, CLIENT_ID, CLIENT_SECRET):
    url = f"{URL}intakes/{uuid}"
    header=request_header(URL, CLIENT_ID, CLIENT_SECRET)
    if header:
        response = requests.request("DELETE", url, headers=header)
        return response.json()
    else:
        return []

        
def all_cities(URL, CLIENT_ID, CLIENT_SECRET):
    url = f"{URL}location/cities/?country_codes=RU"
    header = request_header(URL, CLIENT_ID, CLIENT_SECRET)
    if header:
        response = requests.request("GET", url, headers=header)
        print(response)
        return response.json()
    else:
        return []


def all_regions(URL, CLIENT_ID, CLIENT_SECRET):
    url = f"{URL}location/regions/?country_codes=RU"
    header = request_header(URL, CLIENT_ID, CLIENT_SECRET)
    if header:
        response = requests.request("GET", url, headers=header)
        return response.json()
    else:
        return []


# Регистрация заказа
def cdekFinal(sale_name, postal_code_get, recipient_phone, recipient_name, postal_code, weight, length, width, height, tariff_code, addres_sender, addres_get, calc_sum, city_admin, city_get, URL, CLIENT_ID, CLIENT_SECRET, items):
    url = f"{URL}orders"
    header=request_header(URL, CLIENT_ID, CLIENT_SECRET)
    if header:
        payload = json.dumps({
	        "comment" : "Новый заказ",
	        "delivery_recipient_cost" : {
		        "value" : calc_sum,
	        },

	        "from_location" : {
		        "postal_code" : postal_code,
		        "country_code" : "RU",
		        "city" : city_admin,
		        "address" : addres_sender,
	        },

	        "to_location" : {
		        "postal_code" : postal_code_get,
		        "country_code" : "RU",
		        "city" : city_get,
		        "address" : addres_get
	        },

	        "packages" : [ {
		        "number" : sale_name,
		        "comment" : "Упаковка",
		        "height" : height,
		        "items" : items,
	            "length" : length,
	            "weight" : weight,
	            "width" : width
	        } ],

	        "recipient" : {
		        "name" : recipient_name,
		        "phones" : [ {
		            "number" : recipient_phone,
	            } ]
	        },

	        "sender" : {
		        "name" : "Гершман Гурген Ангарович"
	        },
	        "tariff_code" : tariff_code
        })
        
        response = requests.request("POST", url, headers=header, data=payload)
        logging.info(payload)
        return response.json()
    else:
        return []

# Регистрация заявки на вызов курьера
def sendtoCourier(comment, intake_time_to, intake_time_from, intake_date, need_call, postal_code, address, city, length, width, height, weight, URL, CLIENT_ID, CLIENT_SECRET):
    url = f"{URL}intakes"
    header=request_header(URL, CLIENT_ID, CLIENT_SECRET)
    intake_date_inner_format = datetime.datetime.strptime(str(intake_date), "%Y-%m-%d").strftime("%Y-%m-%d")
    if header:
        payload = json.dumps({
            "intake_date": intake_date_inner_format,
            "intake_time_from": intake_time_from,
            "intake_time_to": intake_time_to,
            "name": "Консолидированный груз",
            'weight': weight,
            'length': length,
            'width': width,
            'height': height,
            "comment": comment,
            "sender": {
                "company": "Компания",
                "name": "Иванов Иван",
                "phones": [
                    {
                    "number": "+79589441654"
                    }
                ]
            },
            "from_location": {
                "postal_code": postal_code,
                "country_code": "RU",
                "city": city,
                "address": address
            },
            "need_call": need_call
            })
        response = requests.request("POST", url, headers=header, data=payload)
        logging.info(intake_date_inner_format)
        return response.json()
    else:
        return []