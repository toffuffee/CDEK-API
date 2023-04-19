from odoo import models, fields, api
import logging
from odoo import http
from odoo.http import request
from requests import post
import requests
import json

from ..controllers.cdek_api import auth, request_header, all_cities, all_regions, get_cities_list, calculate, sendtoCourier, cdekFinal, deleteRequest, deleteRequestCourier

class SaleOrder(models.Model):
    _inherit = "sale.order"
    # delivery_type_get = fields.Selection(
    #     [("courier", "Курьер"), ("atPoint", "В пункт выдачи")], string="Получение", default="atPoint"
    # )

    calculate_result = fields.Integer(string="Стоимость доставки(руб)", readonly=True)
    uuid_request = fields.Char(string="Идентификатор заказа СДЕК", readonly=True)
    uuid_request_courier = fields.Char(string="Идентификатор вызова курьера", readonly=True)
    cdek_sended = fields.Boolean(string="Заказ зарегестрирован", readonly=True, default=False)
    courier_sended = fields.Boolean(string="Курьер вызван", readonly=True, default=False)

    # @api.depends('order_line.price_unit', 'order_line.tax_id', 'order_line.discount', 'order_line.product_uom_qty')
    # def _compute_amount_delivery(self):
    #     result = super()._compute_amount_delivery() 
    #     logging.info("lalalal")
    #     for order in self:
    #         order.amount_delivery = order.calc()
            

    def sendCdek(self):
        products = self.order_line.mapped('product_id')

        sale_name = self.name
        # Тип доставки, адрес и город получателя
        # type_get = dict(self._fields['delivery_type_get'].selection).get(self.delivery_type_get)
        for partner in self.partner_id:
            addres_get = partner.street
            city_get = partner.city
            recipient_name = partner.name
            recipient_phone = partner.phone
            postal_code_get = partner.zip

        # Тип доставки, адрес и город отправителя (токены и прочее)
        Cdek_settings = http.request.env['cdeksetting'].search([],limit=1)
        login = Cdek_settings.user_login
        password = Cdek_settings.user_password
        url = Cdek_settings.token
        city_admin = Cdek_settings.city_admin
        postal_code_admin = Cdek_settings.postal_code
        type_send = dict(Cdek_settings._fields['type_delivery'].selection).get(Cdek_settings.type_delivery)
        address_sender = Cdek_settings.address_admin

        tariff_code = 0
        sum_weight = 0
        sum_width = 0
        max_height = 0
        max_length = 0

        items = list(map(lambda x:  {
			        "ware_key" : x.id,
			        "payment" : {
				        "value" : x.price_subtotal
			        },
			        "name" : x.name,
			        "cost" : x.price_unit,
			        "amount" : int(x.product_uom_qty),
			        "weight" : x.product_id.weight_prod,
			        "url" : "www.item.ru"
		        }, self.order_line))

        new_items = list(filter(lambda x: x['name'] != 'СДЕК - Курьер' and x['name'] != 'СДЕК - В пункт выдачи', items))

        for product in products:
                sum_weight += product.weight_prod
                sum_width += product.width_prod

                if product.height_prod > max_height:
                    max_height = product.height_prod

                if product.length_prod > max_length:
                    max_length = product.length_prod

        for product in product:
            if product.name == "СДЕК - Курьер":
                type_get = "Курьер"
            if product.name == "СДЕК - В пункт выдачи":
                type_get = "В пункт выдачи"
        
        calc_sum = self.calc(type_get)

        if type_send == "В пункт выдачи" and type_get == "В пункт выдачи":
            tariff_code = 136
            send_to_sdek = cdekFinal(sale_name, postal_code_get, recipient_phone, recipient_name, postal_code_admin, sum_weight, max_length, sum_width, max_height, tariff_code, address_sender, addres_get, calc_sum, city_admin, city_get, url, login, password, new_items)
            self.uuid_request = send_to_sdek['entity']['uuid']
            self.cdek_sended = True
            logging.info(send_to_sdek)

        if type_send == "В пункт выдачи" and type_get == "Курьер":
            tariff_code = 137
            send_to_sdek = cdekFinal(sale_name, postal_code_get, recipient_phone, recipient_name, postal_code_admin, sum_weight, max_length, sum_width, max_height, tariff_code, address_sender, addres_get, calc_sum, city_admin, city_get, url, login, password, new_items)
            self.uuid_request = send_to_sdek['entity']['uuid']
            self.cdek_sended = True
            logging.info(send_to_sdek)

        if type_send == "Курьер" and type_get == "В пункт выдачи":
            tariff_code = 138
            send_to_sdek = cdekFinal(sale_name, postal_code_get, recipient_phone, recipient_name, postal_code_admin, sum_weight, max_length, sum_width, max_height, tariff_code, address_sender, addres_get, calc_sum, city_admin, city_get, url, login, password, new_items)
            self.uuid_request = send_to_sdek['entity']['uuid']
            self.cdek_sended = True
            logging.info(send_to_sdek)

        if type_send == "Курьер" and type_get == "Курьер":
            tariff_code = 139
            send_to_sdek = cdekFinal(sale_name, postal_code_get, recipient_phone, recipient_name, postal_code_admin, sum_weight, max_length, sum_width, max_height, tariff_code, address_sender, addres_get, calc_sum, city_admin, city_get, url, login, password, new_items)
            self.uuid_request = send_to_sdek['entity']['uuid']
            self.cdek_sended = True
            logging.info(send_to_sdek)

        



    def calc(self, type_get):
        products = self.order_line.mapped('product_id')

        #Адрес и город получателя
        for partner in self.partner_id:
            addres_get = partner.street
            city_get = partner.city

        # type_get = dict(self._fields['delivery_type_get'].selection).get(self.delivery_type_get)

        Cdek_settings = http.request.env['cdeksetting'].search([],limit=1)
        login = Cdek_settings.user_login
        password = Cdek_settings.user_password
        url = Cdek_settings.token
        city_admin = Cdek_settings.city_admin
        type_send = dict(Cdek_settings._fields['type_delivery'].selection).get(Cdek_settings.type_delivery)
        address_sender = Cdek_settings.address_admin

        sum_weight = 0
        sum_width = 0
        max_height = 0
        max_length = 0

        for product in products:
            sum_weight += product.weight_prod
            sum_width += product.width_prod
        
            if product.height_prod > max_height:
                max_height = product.height_prod

            if product.length_prod > max_length:
                max_length = product.length_prod

        # for product in product:
        #     if product.name == "СДЕК - Курьер":
        #         type_get = "Курьер"
        #     if product.name == "СДЕК - В пункт выдачи":
        #         type_get = "В пункт выдачи"

        if type_send == "В пункт выдачи" and type_get == "В пункт выдачи":
            tariff_code = 136
            calculator = calculate(tariff_code, city_get, city_admin, addres_get, address_sender, sum_width, max_height, max_length, sum_weight, url, login, password)
            logging.info(calculator)

        if type_send == "В пункт выдачи" and type_get == "Курьер":
            tariff_code = 137
            calculator = calculate(tariff_code, city_get, city_admin, addres_get, address_sender, sum_width, max_height, max_length, sum_weight, url, login, password)
            logging.info(calculator)

        if type_send == "Курьер" and type_get == "В пункт выдачи":
            tariff_code = 138
            calculator = calculate(tariff_code, city_get, city_admin, addres_get, address_sender, sum_width, max_height, max_length, sum_weight, url, login, password)
            logging.info(calculator)

        if type_send == "Курьер" and type_get == "Курьер":
            tariff_code = 139
            calculator = calculate(tariff_code, city_get, city_admin, addres_get, address_sender, sum_width, max_height, max_length, sum_weight, url, login, password)
            logging.info(calculator)

        if calculator.get('total_sum'):
            self.calculate_result = calculator['total_sum']
        else:
            self.calculate_result = 0
        return self.calculate_result



    def deleteCdek(self):
        Cdek_settings = http.request.env['cdeksetting'].search([],limit=1)
        login = Cdek_settings.user_login
        password = Cdek_settings.user_password
        url = Cdek_settings.token

        uuid = self.uuid_request

        delete = deleteRequest(uuid, url, login, password)
        self.uuid_request = ""
        self.cdek_sended = False
        logging.info(delete)


    def deleteCourier(self):
        Cdek_settings = http.request.env['cdeksetting'].search([],limit=1)
        login = Cdek_settings.user_login
        password = Cdek_settings.user_password
        url = Cdek_settings.token

        uuid = self.uuid_request_courier

        delete = deleteRequestCourier(uuid, url, login, password)
        self.uuid_request_courier = ""
        self.courier_sended = False
        logging.info(delete)


    
    