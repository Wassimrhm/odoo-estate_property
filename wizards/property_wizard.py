from odoo import models,fields


class changestate(models.Model):
    _name='property.wizard'
    _description="change the state"

    property_id=fields.Many2one('property',readonly=True)
    state=fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),

    ],
    default='draft',
    required=True
    )
    reason=fields.Char(required=True)

    def action_confirm(self):
        self.property_id.state=self.state
        self.property_id._create_hist('closed',self.state,self.reason)
