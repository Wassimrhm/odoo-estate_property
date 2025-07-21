from odoo import models,fields,api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_id = fields.Many2one('property')
    price = fields.Float(compute='_compute_price', store=True)
    # price=fields.Float(related='property_id.selling_price')

    @api.depends('property_id')
    def _compute_price(self):
        for partner in self:
            partner.price = partner.property_id.selling_price if partner.property_id else 0.0