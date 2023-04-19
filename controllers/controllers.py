# # -*- coding: utf-8 -*-
import base64
import logging
from odoo import http
from odoo.http import request
from requests import post
import requests
import json

from .cdek_api import auth, request_header, all_cities, all_regions, get_cities_list, cdekFinal

class CdekMain(http.Controller):
    @http.route('/', auth='public', website=True)
    def index(self, **kw):
        Cdeks = http.request.env['cdek']
        return request.render('cdek.main_page',{
            'cdeks': Cdeks.search([])
        })


# class CdekSettings(http.Controller):
#     @http.route('/cdek-settings', auth='public', website=True)
#     def cdektoken(self, **kw):

#         Cdek_settings = http.request.env['cdeksetting'].search([],limit=1)

#         login = Cdek_settings.user_login
#         password = Cdek_settings.user_password
#         url = Cdek_settings.token
#         city_admin = Cdek_settings.city_admin

#         authentification = auth(url ,login, password)
#         requestheader = request_header(url ,login, password)
#         allregions = all_regions(url ,login, password)
#         getcitieslist = get_cities_list(city_admin, url ,login, password)
#         allcities = all_cities(url, login, password)
#         cdek = cdekFinal()

#         logging.info(authentification)




class AddCdek(http.Controller):
    @http.route('/add_cdek', type='http', auth='public', website=True,method="POST")
    def cdek_webform(self, **kw):
        return http.request.render('cdek.create_cdek', {})

    @http.route('/create/cdek', type='http', auth='public', website=True)
    def create_cder(self, **post):
        logging.info(f'==============================={post}')
        values = {'name':post['name'],'lastname':post['lastname'],'delivery':post['delivery'],'number':post['number'], 'house':post['house'], 'city':post['city'], 'address':post['address'], 'postal_code':post['postal_code']}
        request.env['cdek'].sudo().create(values)
        return request.render('cdek.devilery_thanks', {})