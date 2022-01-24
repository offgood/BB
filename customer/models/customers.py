import base64
from odoo import models, fields, api

#Create Function Convert img to base64

# รายละเอียด ลูกค้า ชื่อ-นามสกุล
class Customerdetails(models.Model):
    _name = 'customer.customers'
    _description = 'customers Details'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _rec_name = 'full_name'
    
    company_id = fields.Many2one('customer.organize',string='ชื่อบริษัท/หน่วยงาน', track_visibility='onchange', required=True)
    t_name = fields.Many2one('res.partner.title', string='คำนำหน้า', track_visibility='onchange',required=True)
    full_name = fields.Char(string='ชื่อลูกค้า', track_visibility='onchange', required=True)#แก้เป็นชื่อ เต็ม
    image = fields.Binary(string='รูปภาพ', track_visibility='onchange')
    team_id = fields.Many2one('crm.team',string='ทีม')   
    e_mail = fields.Char(string='อีเมล์', track_visibility='onchange', required=True)
    mobile_phone = fields.Char(string='เบอร์มือถือ', track_visibility='onchange')
    phone = fields.Char(string='เบอร์โทรศัพท์', track_visibility='onchange', required=True)
    job_position = fields.Char(string='ตำแหน่ง', track_visibility='onchange',required=True)
    fax = fields.Char(string='แฟกซ์', track_visibility='onchange')
    line_id = fields.Char(string='Line ID', track_visibility='onchange')
    
    user_id = fields.Many2one('res.users', string='ผู้สร้าง', track_visibility='onchange',tracking=True, readonly=True, default=lambda self: self.env.user)
