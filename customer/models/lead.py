from odoo import models, fields, api
# รายละเอียด งานที่ลูกค้าสั่ง
class Leaddetails(models.Model):
    _name = 'customer.lead'
    _description = 'Lead Details'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _rec_name = 'lead_name'
    lead_name = fields.Char(string='Lead Name', required=True, track_visibility='onchange')
    
    #เดี๋ยวดึงรายละเอียด บริษัทออกมา
    company_id = fields.Many2one('customer.organize', string='บริษัท/หน่วยงาน', track_visibility='onchange', required=True)

    address = fields.Text(string='ที่อยู่', related='company_id.address', readonly=False, track_visibility='onchange', required=True)
    province = fields.Char(string='จังหวัด', related='company_id.province', readonly=False, track_visibility='onchange', required=True)
    district = fields.Char(string='เขต', related='company_id.district', readonly=False, track_visibility='onchange', required=True)
    sub_district = fields.Char(string='แขวง', related='company_id.sub_district', readonly=False, track_visibility='onchange', required=True)
    
    
    e_mail = fields.Char(string='อีเมล์', related='company_id.e_mail', readonly=False,track_visibility='onchange', required=True)
    mobile_phone = fields.Char(string='เบอร์มือถือ', related='company_id.mobile_phone', readonly=False,track_visibility='onchange')
    phone = fields.Char(string='เบอร์โทรศัพท์', related='company_id.phone',track_visibility='onchange', readonly=False, required=True)
    fax = fields.Char(string='แฟกซ์', related='company_id.fax', track_visibility='onchange' ,readonly=False)
    line_id = fields.Char(string='Line ID', related='company_id.line_id',track_visibility='onchange', readonly=False)

    contacts_id = fields.Many2one('customer.customers',string='ชื่อลูกค้า', track_visibility='onchange')
    t_name = fields.Many2one('customer.customers.titelname', related='contacts_id.t_name',string='คำนำหน้า', track_visibility='onchange',required=True, readonly=False)
    
    job_position = fields.Many2one('customer.lead.typeposition', string='ประเภท', track_visibility='onchange', required=True)
    souce_id = fields.Many2one('customer.lead.soucelead', string='ติดต่อจาก', required=True, track_visibility='onchange')
    
   
    
    #ส่วนท้าย
    sale_team_id = fields.Many2one('customer.salesteam',string='ทีม', track_visibility='onchange')
    user_id = fields.Many2one('res.users', string='ผู้สร้าง', readonly=True, track_visibility='onchange',tracking=True, default=lambda self: self.env.user)
    note = fields.Text(string='บันทึก', track_visibility='onchange')


    
#ประเภทงาน
class TypePosition(models.Model):
    _name = 'customer.lead.typeposition'
    _description = 'Type Position Lead'
    _rec_name = 'typejob_name'
    
    typejob_name = fields.Char(string='ประเภท')
    
    
#ติดต่อมาทางไหน
class Soucerlead(models.Model):
    _name = 'customer.lead.soucelead'
    _description = 'Souce Lead'
    _rec_name = 'soucer_name'
    
    soucer_name = fields.Char(string='ติดต่อจาก')



    

        
    