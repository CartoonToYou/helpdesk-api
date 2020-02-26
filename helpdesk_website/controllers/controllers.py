# -*- coding: utf-8 -*-
from odoo import http

# class HelpdeskWebsite(http.Controller):
#     @http.route('/helpdesk_website/helpdesk_website/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpdesk_website/helpdesk_website/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpdesk_website.listing', {
#             'root': '/helpdesk_website/helpdesk_website',
#             'objects': http.request.env['helpdesk_website.helpdesk_website'].search([]),
#         })

#     @http.route('/helpdesk_website/helpdesk_website/objects/<model("helpdesk_website.helpdesk_website"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpdesk_website.object', {
#             'object': obj
#         })