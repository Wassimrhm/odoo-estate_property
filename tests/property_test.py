from odoo.tests.common import TransactionCase
from odoo import fields

class testProperty(TransactionCase):

    def setUp(self,*args,**kwargs):
        super().setUp()
        self.property_01_record=self.env['property'].create({
            'ref':'P100',
            'name':'property6',
            'postcode':'321',
            'dateavailability':fields.date.today(),
            'bedrooms':4,
            'expected_price':4000
        })
    
    def test_01_check_property_values(self):
        property_id= self.property_01_record
        self.assertRecordValues(property_id,expected_values=[{            
            'ref':'P100',
            'name':'property6',
            'postcode':'321',
            'dateavailability':fields.date.today(),
            'bedrooms':4,
            'expected_price':4000}])