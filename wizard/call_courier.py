from odoo import models, fields, api
import logging
from odoo import http
from odoo.http import request
from requests import post
import requests
import json

from ..controllers.cdek_api import auth, request_header, all_cities, all_regions, get_cities_list, calculate, sendtoCourier, deleteRequestCourier


class CallCourier(models.TransientModel):
    _name = 'callcourier'

    intake_date = fields.Date(string="Дата ожидания курьера")
    intake_time_from = fields.Char(string="Время начала ожидания курьера")
    intake_time_to = fields.Char(string="Время окончания ожидания курьера")
    comment = fields.Text(string="Комментарий курьеру")
    need_call = fields.Boolean(string="Нужен звонок курьера")

    def getDefaultTracks(self):
        models_ids = self.env.context.get('active_id')
        sale_order = self.env['sale.order'].browse(models_ids)
        calc = sale_order.calculate_result
        logging.info(calc)


    def sendCourier(self):
        models_ids = self.env.context.get('active_id')
        sale_order = self.env['sale.order'].browse(models_ids)

        products = sale_order.order_line.mapped('product_id')
        
        Cdek_settings = http.request.env['cdeksetting'].search([],limit=1)
        login = Cdek_settings.user_login
        password = Cdek_settings.user_password
        url = Cdek_settings.token
        city_admin = Cdek_settings.city_admin
        postal_code_admin = Cdek_settings.postal_code
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
        

        send_to_courier = sendtoCourier(self.comment, self.intake_time_to, self.intake_time_from, self.intake_date, self.need_call, postal_code_admin, address_sender, city_admin, max_length, sum_width, max_height, sum_weight, url, login, password)
        sale_order.uuid_request_courier = send_to_courier['entity']['uuid']
        sale_order.courier_sended = True
        logging.info(send_to_courier)



