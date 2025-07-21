from odoo import models,fields,api


class AccountMmove(models.Model):
    _inherit='account.move'

    def action_do_something(self):
        print("####################################")
