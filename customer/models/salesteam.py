from odoo import models, fields, api
# รายละเอียด ทีม ชื่อทีม สมาชิก หัวหน้า
class Saleteam(models.Model):
    _name = 'customer.salesteam'
    _description = 'Sale Team Member'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _rec_name = 'team_name'
    
    team_name = fields.Char(string="ชื่อทีม", track_visibility='onchange', required=True)
    leader_id = fields.Many2one('res.users',string="หัวหน้าทีม", track_visibility='onchange', required=True)#เชื่อมได้ไหม?
    
    
    members_id = fields.Many2many('res.users', string="ลูกทีม", track_visibility='onchange')
    company_id = fields.Many2one('res.company', string="บริษัท", track_visibility='onchange')
    user_id = fields.Many2one('res.users', string='ผู้สร้าง', track_visibility='onchange', tracking=True, readonly=True, default=lambda self: self.env.user)
   

        
    