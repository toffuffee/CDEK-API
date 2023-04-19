from odoo import fields, models

class ProductPropetries(models.Model):
    _inherit = "product.template"

    height_prod = fields.Integer(string="Высота(см)")
    length_prod = fields.Integer(string="Длина(см)")
    width_prod = fields.Integer(string="Ширина(см)")
    weight_prod = fields.Integer(string="Вес(гр)")