from odoo import models,fields,api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import requests



class Property(models.Model):
    _name = "property"
    _inherit=['mail.thread','mail.activity.mixin']
    _description="Estate Property"

    name=fields.Char(required=True,size=30,tracking=1)
    ref=fields.Char(default='New',readonly=True,tracking=1)
    description=fields.Text()
    postcode=fields.Char(tracking=1)
    creating_date=fields.Date(readonly=True,default=fields.datetime.now())
    date_availability=fields.Date(copy=True, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price=fields.Float(required=True, digits=(0,3),tracking=1)
    selling_price=fields.Float(readonly=True,copy=False,default=3000)
    difference=fields.Float(compute='_compute_difference' , readonly=True)
    bedrooms=fields.Integer(default=2)
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    garden_orientation=fields.Selection(selection=[('north', 'North'), ('south', 'South'), 
                  ('east', 'East'), ('west', 'West')])
    active=fields.Boolean(default=True)
    state=fields.Selection(selection=[
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ],
    required=True,
    copy=False, 
    default="draft"
    )
    owner_id=fields.Many2one('owner')
    tags_ids=fields.Many2many('tag')
    owner_adress=fields.Char(related='owner_id.adress',readonly=False)
    owner_phone=fields.Char(related='owner_id.phone')


    _sql_constraints=[
        ('unique_name','unique("name")','Name is already taken')
    ]

    line_ids=fields.One2many('property.line','property_id')
    expected_selling_date=fields.Date()
    is_late=fields.Boolean()
    



    @api.constrains('bedrooms')
    def check_bedrooms(self):
        for prop in self:
            if prop.bedrooms<=0:
                raise ValidationError('Please add a valid number of bedrooms')
            
    @api.depends('expected_price','selling_price')
    def _compute_difference(self):
        for rec in self:
            rec.difference = rec.expected_price - rec.selling_price

    @api.onchange('expected_price')
    def _onchange_owner_id(self):
        for rec in self:
            print("inside owner id on change method")
            
    def action_draft(self):
        for rec in self:
            rec._create_hist(rec.state,'draft')
            rec.state='draft'

            
    def action_sold(self):
        for rec in self:
            rec._create_hist(rec.state,'sold')
            rec.state='sold'

    def action_pending(self):
        for rec in self:
            rec._create_hist(rec.state,'pending')
            rec.state='pending'

    def action_closed(self):
        for rec in self:
            rec._create_hist(rec.state,'closed')
            rec.state='closed'

    def check_expected_selling_date(self):
        property_ids=self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today() and rec.state != 'sold':
                rec.is_late=True


    def action(self):
        # print(self.env.user.name)      
        # print(self.env.context)      
        # print(self.env.cr)      
        # # print(self.env['owner'].create({}))  
        # [('name','!=','Property1')]
        print(self.env['property'].search([('name','like','property'),('postcode','like','321')])) 

    api.model
    def _create(self, data_list):
        res= super()._create(data_list)   
        if res.ref == 'New'  :
            res.ref=self.env['ir.sequence'].next_by_code('property_seq')
        return res
    
    def _create_hist(self,old_state,new_state,reason=''):
        for rec in self:
            rec.env['property.hist'].create({
                'user_id': self.env.uid,
                'property_id': self.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason':reason,
                'line_ids':[(0,0,{'name':line.name,'area':line.area}) for line in rec.line_ids],
                
                })
            
    def action_open_change_state(self):
        action = self.env['ir.actions.actions']._for_xml_id('estate_module.property_wizard_action')
        action['context']={'default_property_id':self.id}
        return action
    
    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('estate_module.owner_action')
        view_id=self.env.ref('estate_module.owner_view_form').id
        action['res_id']=self.owner_id.id
        action['views']=[[view_id,"form"]]
        return action
    

    def get_properties(self):
        payload=dict({})
        try:
            response=requests.get('http://localhost:8069/v1/properties',data=payload)
            if response.status_code==200:
                print('#######SUCCESSEFUL#####')
        except Exception as err:
            print('#######FAILED#####')
            raise ValidationError(str(err))

    def property_xlsx_report(self):
        return {
            'type':'ir.actions.act_url',
            'url':f'/property/exel/report/{self.env.context.get("active_ids")}',
            'target':'new'
        }
            
    #grad operation(create/read/update/delete)

    # @api.model_create_multi
    # def _create(self, data_list):
    #     return super()._create(data_list)
    
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
    #     return super()._search(domain, offset, limit, order, count, access_rights_uid)
    
    # def _write(self, vals):
    #     return super()._write(vals)
    
    # def unlink(self):
    #     return super().unlink()

class PropertyLines(models.Model):
    _name='property.line'
    _description="bedrooms estate property"

    name=fields.Char()
    description=fields.Char()
    area=fields.Float()
    property_id = fields.Many2one('property')

