from odoo import fields, models

class Delivery(models.Model):
    _name = 'deliveryget'

    name = fields.Char(string="Доставка")
    