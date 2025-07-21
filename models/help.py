from odoo import models,fields
from dateutil.relativedelta import relativedelta

class Help(models.Model):
    _name = "help"
    _description="estate property help"

    Property_name=fields.Char()
    problem=fields.Text(required=True)
    property_post_code_declared=fields.Integer(required=True)
    detail=fields.Text()
