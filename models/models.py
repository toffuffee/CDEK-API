import datetime
from odoo import models, fields, api
import requests
import json
import logging
from odoo.exceptions import ValidationError



class cdek(models.Model):
    _name = 'cdek'
    _description = 'cdek info'

    name = fields.Char(string="Имя")
    lastname = fields.Char(string="Фамилия")
    number = fields.Text(string="Номер")
    city = fields.Char(string="Город")
    address = fields.Text(string="Адрес")
    house = fields.Text(string="Дом/Квартира")
    postal_code = fields.Text(string="Почтовый индекс")
    delivery = fields.Selection([('courier','Курьер'), ('atPoint','В пункт выдачи')], string="Вид доставки")


class cdeksetting(models.Model):
    _name = 'cdeksetting'
    _description = 'cdek setting'

    user_login = fields.Char(string="Логин")
    user_password = fields.Char(string="Пароль")
    token = fields.Text(string="Токен")
    city_admin = fields.Char(string="Город отправления")
    address_admin = fields.Char(string="Адрес отправляемого магазина")
    type_delivery = fields.Selection([('courier','Курьер'), ('atPoint','В пункт выдачи')], string="Вид отправления")
    postal_code = fields.Char(string="Почтовый индекс")

