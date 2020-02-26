# -*- coding: utf-8 -*-
from odoo import http

# class CustomFieldSchedule(http.Controller):
#     @http.route('/custom_field_schedule/custom_field_schedule/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_field_schedule/custom_field_schedule/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_field_schedule.listing', {
#             'root': '/custom_field_schedule/custom_field_schedule',
#             'objects': http.request.env['custom_field_schedule.custom_field_schedule'].search([]),
#         })

#     @http.route('/custom_field_schedule/custom_field_schedule/objects/<model("custom_field_schedule.custom_field_schedule"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_field_schedule.object', {
#             'object': obj
#         })