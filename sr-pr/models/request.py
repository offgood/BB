#-*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
from datetime import datetime, timedelta
#Create Function Convert img to base64
_logger = logging.getLogger(__name__)
# รายละเอียด ลูกค้า ชื่อ-นามสกุล
class Requestdetails(models.Model):
    _name = 'sr_pr.request'
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = 'Request Details'
    
    @api.model
    def _default_note(self):
        return self.env['ir.config_parameter'].sudo().get_param('account.use_invoice_terms') and self.env.company.invoice_terms or ''

    
    #ID Group
    partner_id = fields.Many2one('res.partner', string='Customer Name',tracking=True)
    company_id = fields.Many2one('res.company', string='Customer Name',stracking=True)
    owner_id = fields.Many2one('res.users', string='Request By', required=True, default=lambda self: self.env.user)
    project_id = fields.Many2one('project.project', 'Project', required=True)
    order_line = fields.One2many('sr.orderline', 'ref_id', string='Order Lines', copy=True, auto_join=True)
    teamlead_id = fields.Many2one('res.users', 'Team Leader',  copy=False, track_visibility='onchange', required=True)
    team_id = fields.Many2one('crm.team', string='Sales Team', required=True, tracking=True)
    request_type = fields.Selection([('SR', 'Sale Request'), ('PR', 'Purchase Request')], default='SR', required=True, tracking=True)
    name = fields.Char(string='Ref:', copy=False, index=True)
    #description Group
    
    tel = fields.Char(string='Tel',readonly=False)
    description = fields.Text(string='หมายเหตุ')
    payment_con = fields.Char(string='เงื่อนไขการชำระเงิน')
    Capacity = fields.Text(string='Capacity')
    sequence = fields.Integer(string='Sequence', default=10)
    rec_name = fields.Char(string='Received Name')
    request_date = fields.Date(string='Requested Date', default=datetime.today(), index=True, help="Date on which sales requests is created.")
    delivery_date = fields.Date(string='Delivery Date')
    desired_date = fields.Text(string='Desired Date')
    due_date = fields.Date(string='Due Date')
    note = fields.Text('Terms and conditions', default=_default_note)
    Po = fields.Char(string='PO')
    rev = fields.Integer(string='Rev', index=True, default=0)
    delivery_site = fields.Char(string='ระบุสถานที่')
    #service Group
    install_cost = fields.Char(string='ค่าติดตั้งและวัสดุสิ้นเปลือง')
    training_cost = fields.Char(string='ค่าอบรม')
    warranty_cost = fields.Char(string='Warranty Cost')
    war_mc = fields.Char(string='WAR-MC')
    warranty_time = fields.Char(string='Warranty time')

    #สถานะ
    
    address = fields.Selection([
        ('office', 'สำนักงานใหญ่'),
        ('store', 'สโตร์'),
        ('site', 'หน้างาน'),
        ],string='Delivery to',track_visibility='onchange', tracking=True)
    status = fields.Selection([
        ('รอใบเสนอราคา', 'รอใบเสนอราคา'),
        ('หาคู่เทียบ', 'หาคู่เทียบ'),
        ('ต่อรองราคา', 'ต่อรองราคา'),
        ('ต่อรองเงื่อนไข', 'ต่อรองเงื่อนไข'),
        ('PO รออนุมัติ', 'PO รออนุมัติ'),
        ('อยู่ระหว่างทำสัญญา', 'อยู่ระหว่างทำสัญญา'),
        ('รอส่งของ', 'รอส่งของ'),
        ('จบงาน', 'จบงาน'),
        ], default="select",track_visibility='onchange', string="Status")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('wait', 'Waiting for approval'),
        ('approve', 'Approve'),
        ('submit', 'In progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], default="draft", track_visibility='onchange', string='State')
    
    def action_draft(self):
        self.state = 'draft'
    
    def action_wait(self):
        self.state = 'wait'
        
    def action_approve(self):
        self.state = 'approve'

    def action_submit(self):
        self.state = 'submit'
    
    def escalate_order(self):
        self.ensure_one()
        template = self.env['ir.model.data'].get_object('sr-pr.request', 'email_template_request_approval_mail')
        self.env['mail.template'].browse(template.id).send_mail(self.id,force_send=True)
        return True
    
    def action_ref(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sr-pr.req_action_ref_new")
        n = 1
        # self.reference_new = self.reference_new + n
        # ref_name = self.name
        action['context'] = {
            # 'search_default_opportunity_id': self.id,
            # 'default_opportunity_id': self.id,
            # 'search_default_partner_id': self.partner_id.id,
            'default_name': self.name,
            'default_partner_id': self.partner_id.id,
            'default_team_id': self.team_id.id,
            'default_rev': self.rev + n,
            'default_project_id': self.project_id.id,
            'default_teamlead_id': self.teamlead_id.id,
            'default_company_id': self.company_id.id,
            'default_owner_id': self.owner_id.id,
            'default_order_line': self.order_line.ids,
            'default_request_type': self.request_type,
            'default_address': self.address,
            'default_delivery_site': self.delivery_site,
            'default_tel': self.tel,
            'default_delivery_date': self.delivery_date,
            'default_due_date': self.due_date,
            'default_payment_con': self.payment_con,
            'default_request_type': self.request_type,
            'default_description': self.description,
            'default_Capacity': self.Capacity,
            'default_rec_name': self.rec_name,
            'default_Po': self.Po,
            'default_status': self.status,
            'default_state': self.state,
            'default_install_cost': self.install_cost,
            'default_training_cost': self.training_cost,
            'default_warranty_cost': self.warranty_cost,
            'default_war_mc': self.war_mc,
            'default_warranty_time': self.warranty_time,
            
        }
        return action
        
    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'
        
        
    @api.onchange('partner_id','company_id')
    def _compute_address(self):
        if self.company_id:
            tel_company = self.company_id.phone
            self.tel = tel_company
        elif self.partner_id:
            tel_partner = self.partner_id.phone
            self.tel = tel_partner
        else:
            self.tel = ''

    @api.onchange('team_id')
    def _compute_team(self):
        if self.team_id:
            manager = self.team_id.user_id
            self.teamlead_id = manager
        else:
            self.team_id = ''
            self.teamlead_id = ''
            
            
    @api.model
    def create(self , vals):
        if vals.get('rev') == 0: 
            if not vals.get('note'):
                vals['note'] = 'New Request'
            if vals.get('request_type') == ('SR'):
                vals['name'] = self.env.company.name[0]+'SR'+self.env['ir.sequence'].next_by_code('sr_pr.request.name')+vals['name']
            elif vals.get('request_type') == ('PR'):
                vals['name'] = self.env.company.name[0]+'PR'+self.env['ir.sequence'].next_by_code('sr_pr.request.name')+vals['name']
            res = super(Requestdetails, self).create(vals)
            return res
        else:
            res = super(Requestdetails, self).create(vals)
            return res
