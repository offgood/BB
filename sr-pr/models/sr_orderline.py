from pickletools import uint1
from odoo import models, fields, api

class RequestOrderline(models.Model):
    _name = 'sr.orderline'
    _description = 'Request Orderline'
    
    
    product_id = fields.Many2one('product.product', 'Product')
    ref_id = fields.Many2one('sr_pr.request', string='Reference', ondelete='cascade', copy=False)
    unit = fields.Float('Unit',tracking=True)
    name = fields.Text(string='Remark', )
    product_type = fields.Char(string='Model/Series')
    product_template_id = fields.Many2one('product.template',compute='_compute_product_type',tracking=True)
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    
 
