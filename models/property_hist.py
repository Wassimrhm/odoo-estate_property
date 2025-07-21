from odoo import models,fields,api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class PropertyHist(models.Model):
    _name = "property.hist"
    _description="Estate Property History"
    _rec_name='property_id'


    user_id=fields.Many2one('res.users')
    property_id=fields.Many2one('property')
    old_state=fields.Char()
    new_state=fields.Char()
    reason=fields.Char()
    line_ids=fields.One2many('property.hist.line','history_id')

class PropertyHistoryline(models.Model):
    _name="property.hist.line"

    history_id=fields.Many2one('property.hist')
    description=fields.Char()
    name=fields.Char()
    area=fields.Float()