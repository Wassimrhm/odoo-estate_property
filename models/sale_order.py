from odoo import models,fields,api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class SaleOrder(models.Model):
    _inherit='sale.order'

    property_id=fields.Many2one('property')
