from odoo import models,fields,api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class Bedroom(models.Model):
    _name = "building"
    _description="Building record"
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'code'


    name=fields.Char()
    no=fields.Integer(required=True,size=30)
    code=fields.Char()
    description=fields.Text()
    active=fields.Boolean(default=True)
