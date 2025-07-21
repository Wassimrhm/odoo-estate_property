from odoo import models,fields,api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class Bedroom(models.Model):
    _name = "bedroom"
    _description="estate property bedroom"

    name=fields.Char(required=True,size=30)
    size=fields.Float()
    
