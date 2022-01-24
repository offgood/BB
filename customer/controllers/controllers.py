# -*- coding: utf-8 -*-
# from odoo import http


# class Customer(http.Controller):
#     @http.route('/customer/customer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customer/customer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('customer.listing', {
#             'root': '/customer/customer',
#             'objects': http.request.env['customer.customer'].search([]),
#         })

#     @http.route('/customer/customer/objects/<model("customer.customer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customer.object', {
#             'object': obj
#         })
