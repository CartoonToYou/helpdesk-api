# -*- coding: utf-8 -*-
from odoo import http

# class CustomFieldTeam(http.Controller):
#     @http.route('/custom_field_team/custom_field_team/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_field_team/custom_field_team/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_field_team.listing', {
#             'root': '/custom_field_team/custom_field_team',
#             'objects': http.request.env['custom_field_team.custom_field_team'].search([]),
#         })

#     @http.route('/custom_field_team/custom_field_team/objects/<model("custom_field_team.custom_field_team"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_field_team.object', {
#             'object': obj
#         })