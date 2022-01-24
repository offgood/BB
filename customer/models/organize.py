import logging
from odoo import models, fields, api
# บริษัท
_logger = logging.getLogger(__name__)
class Organizadetails(models.Model):
    _name = 'customer.organize'
    _description = 'Organize Details'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _rec_name = 'company_name'


    company_name = fields.Char(string='ชื่อบริษัท/หน่วยงาน', tracking=True, required=True) 
    logo = fields.Binary(string='', tracking=True)
    
    address = fields.Many2one('res.city.zip',string='เลือกที่อยู่', tracking=True, required=True)
    post_code = fields.Char(string='รหัสไปรษณี', related='address.name', readonly=False, tracking=True)
    district = fields.Char(string='เขต', compute="_compute_sub_string_name_res_city", store=True, readonly=False, tracking=True )
    sub_district = fields.Char(string='แขวง', compute="_compute_sub_string_name_res_city", store=True, readonly=False, tracking=True )
    country_id = fields.Many2one('res.country', ondelete='restrict', related='address.country_id', readonly=False, string='ประเทศ', tracking=True)
    Note_address = fields.Text(string='รายละเอียดที่อยู่', compute="_compute_sub_string_name_res_city", store=True,readonly=False, tracking=True)
    state_id = fields.Many2one(
        "res.country.state", string='จังหวัด', related='address.state_id',readonly=False, tracking=True)

    contacts_id = fields.One2many('customer.customers', 'company_id', tracking=True) 
    
    type_organize = fields.Many2one('customer.organize.typeor', string='ประเภท', tracking=True)
    website = fields.Char(string='เว็บไซต์', tracking=True)
    
    
    e_mail = fields.Char(string='อีเมล์', tracking=True, required=True)
    mobile = fields.Char(string='เบอร์มือถือ', tracking=True)
    phone = fields.Char(string='เบอร์โทรศัพท์', tracking=True, required=True)
    fax = fields.Char(string='แฟกซ์', tracking=True)
    line_id = fields.Char(string='Line ID', tracking=True)
    user_id = fields.Many2one('res.users', string='ผู้สร้าง', readonly=True, tracking=True, default=lambda self: self.env.user)
    
    # Address invoices
    street_invoice = fields.Many2one('res.city.zip','เลือกที่อยู่',tracking=True)
    zip_invoice = fields.Char('รหัสไปรษณี',related='street_invoice.name', tracking=True,change_default=True, compute='_compute_partner_address_values', readonly=False, store=True)
    state_id_invoice = fields.Many2one(
        "res.country.state", string='จังหวัด', related='street_invoice.state_id',tracking=True,readonly=False, store=True)
    country_id_invoice = fields.Many2one(
        'res.country', string='ประเทศ',related='street_invoice.country_id', readonly=False, store=True)
    district_invoice = fields.Char(string='เขต', compute="_compute_sub_string_name_res_city_invoice", store=True, readonly=False, tracking=True)
    sub_district_invoice = fields.Char(string='แขวง', compute="_compute_sub_string_name_res_city_invoice", store=True, readonly=False, tracking=True)
    Note_address_invoice = fields.Text(string='รายละเอียดที่อยู่',compute="_compute_sub_string_name_res_city_invoice", store=True, readonly=False, tracking=True)
     # Address delivery
    street_delivery = fields.Many2one('res.city.zip','เลือกที่อยู่',tracking=True)
    zip_delivery = fields.Char('รหัสไปรษณี',related='street_delivery.name', tracking=True,change_default=True, compute='_compute_partner_address_values', readonly=False, store=True)
    state_id_delivery = fields.Many2one(
        "res.country.state", string='จังหวัด', related='street_delivery.state_id',tracking=True,readonly=False, store=True)
    country_id_delivery = fields.Many2one(
        'res.country', string='ประเทศ',related='street_delivery.country_id', readonly=False, store=True)
    district_delivery = fields.Char(string='เขต', compute="_compute_sub_string_name_res_city_delivery", store=True, readonly=False, tracking=True)
    sub_district_delivery = fields.Char(string='แขวง', compute="_compute_sub_string_name_res_city_delivery", store=True, readonly=False, tracking=True)
    Note_address_delivery  = fields.Text(string='รายละเอียดที่อยู่', compute="_compute_sub_string_name_res_city_delivery", store=True,readonly=False, tracking=True)
    @api.model
    def get_date_to_convert_name(self, leads):
        val = {
                'company_name' : leads.partner_name,
                'address' : leads.tree.id,
                'post_code' : leads.zip,
                'country_id' : leads.country_id.id,
                'state_id' : leads.state_id,
                'e_mail' : leads.email_from,
                'phone' : leads.phone,
                'user_id' : leads.user_id.id,
                'line_id' : leads.line_id,
                'street_invoice' : leads.street_invoice.id,       
                'zip_invoice' : leads.zip_invoice,     
                'state_id_invoice' : leads.state_id_invoice.id,          
                'country_id_invoice' : leads.country_id_invoice.id,           
                'street_delivery' : leads.street_delivery.id,        
                'zip_delivery' : leads.zip_delivery,      
                'state_id_delivery' : leads.state_id_delivery.id,           
                'country_id_delivery' : leads.country_id_delivery.id,
                'website' : leads.website,
                'district' : leads.district,
                'sub_district' : leads.sub_district,
                'district_invoice' : leads.district_invoice,
                'sub_district_invoice' : leads.sub_district_invoice,
                'district_delivery' : leads.district_delivery,
                'sub_district_delivery' : leads.sub_district_delivery,
                'Note_address' : leads.Note_address,
                'Note_address_invoice' : leads.Note_address_invoice,
                'Note_address_delivery' : leads.Note_address_delivery,
                'fax' : leads.fax
            }
        organize_id = self.env['customer.organize'].create(val)
        _logger.info(organize_id)
        if leads.contact_name:
            con = {
                    't_name' : leads.title.id,
                    'full_name' : leads.contact_name,
                    'company_id' : organize_id.id, 
                    'e_mail' : leads.email_from, 
                    'phone' : leads.phone, 
                    'user_id' : leads.user_id.id,  
                    'line_id' : leads.line_id,
                    'job_position' : leads.function
                }
            self.env['customer.customers'].create(con)

    @api.onchange('address')#เอาไว้ substr
    def _compute_sub_string_name_res_city(self):
        if not self.address:
            self.district = ''
            self.sub_district = ''
            self.Note_address = ''

        for rec in self:
            if rec.address:
                address = rec.address.display_name
                str__district = address.split(',')
                if rec.address.details:
                    rec.district = str__district[3]
                    rec.sub_district = str__district[2]
                    rec.Note_address = str__district[0]
                else:
                    rec.district = str__district[2]
                    rec.sub_district = str__district[1]
                    rec.Note_address = ''


    
    @api.onchange('street_invoice')#เอาไว้ substr
    def _compute_sub_string_name_res_city_invoice(self):
        if not self.street_invoice:
            self.district_invoice = ''
            self.sub_district_invoice = ''
            self.Note_address_invoice = ''
        for rec in self:
            if rec.street_invoice:
                address = rec.street_invoice.display_name
                str__district = address.split(',')
                if rec.street_invoice.details:
                    rec.district_invoice = str__district[3]
                    rec.sub_district_invoice = str__district[2]
                    rec.Note_address_invoice = str__district[0]
                else:
                    rec.district_invoice = str__district[2]
                    rec.sub_district_invoice = str__district[1]
                    rec.Note_address_invoice = ''
                
                    
               

    @api.onchange('street_delivery')#เอาไว้ substr
    def _compute_sub_string_name_res_city_delivery(self):
        if not self.street_delivery:
            self.district_delivery = ''
            self.sub_district_delivery = ''
            self.Note_address_delivery = ''
        for rec in self:
            if rec.street_delivery:
                address = rec.street_delivery.display_name
                str__district = address.split(',')
                if rec.street_delivery.details:
                    rec.district_delivery = str__district[3]
                    rec.sub_district_delivery = str__district[2]
                    rec.Note_address_delivery = str__district[0]
                else:
                    rec.district_delivery = str__district[2]
                    rec.sub_district_delivery = str__district[1]
                    rec.Note_address_delivery = ''


   

# ประเภทบริษัท 
class Typedetails(models.Model):
    _name = 'customer.organize.typeor'
    _description = 'Type organize'
    _rec_name = 'name_type'
    name_type = fields.Char()


