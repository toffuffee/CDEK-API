from odoo import fields, models

class Delivery(models.Model):
    _inherit = 'delivery.carrier'

    def rate_shipment(self, order):
        ''' Compute the price of the order shipment

        :param order: record of sale.order
        :return dict: {'success': boolean,
                       'price': a float,
                       'error_message': a string containing an error message,
                       'warning_message': a string containing a warning message}
                       # TODO maybe the currency code?
        '''
        result = super().rate_shipment(order=order)
        if self.name == "СДЕК - Курьер" and result['price']:
            result['price'] = order.calc("Курьер")
        if self.name == "СДЕК - В пункт выдачи" and result['price']:
            result['price'] = order.calc("В пункт выдачи")

        
        return result

class ChooseDelivery(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    def button_confirm(self):
        super().button_confirm()
        if self.carrier_id.name == "СДЕК - Курьер":
            self.display_price = self.order_id.calc("Курьер")
        if self.carrier_id.name == "СДЕК - В пункт выдачи":
            self.display_price = self.order_id.calc("В пункт выдачи")