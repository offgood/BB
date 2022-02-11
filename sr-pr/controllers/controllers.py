# -*- coding: utf-8 -*-
# from odoo import http


# class Sr-pr(http.Controller):
#     @http.route('/sr-pr/sr-pr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sr-pr/sr-pr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sr-pr.listing', {
#             'root': '/sr-pr/sr-pr',
#             'objects': http.request.env['sr-pr.sr-pr'].search([]),
#         })

#     @http.route('/sr-pr/sr-pr/objects/<model("sr-pr.sr-pr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sr-pr.object', {
#             'object': obj
#         })
