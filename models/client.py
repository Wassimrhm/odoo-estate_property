from odoo import models,fields,api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class Client(models.Model):
    _name='client'
    _inherit='owner'
    _description="Client Estate Property"

    