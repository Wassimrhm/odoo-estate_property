from odoo import models,fields,api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class Owner(models.Model):
    _name = "owner"
    _description="estate property owners"

    name=fields.Char(required=True,size=30)
    phone=fields.Char()
    adress=fields.Char()

    property_ids=fields.One2many('property','owner_id')