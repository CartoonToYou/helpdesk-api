# -*- coding: utf-8 -*-
from odoo import http

# class HelpdeskAssignedGroup(http.Controller):
#     @http.route('/helpdesk_assigned_group/helpdesk_assigned_group/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/helpdesk_assigned_group/helpdesk_assigned_group/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('helpdesk_assigned_group.listing', {
#             'root': '/helpdesk_assigned_group/helpdesk_assigned_group',
#             'objects': http.request.env['helpdesk_assigned_group.helpdesk_assigned_group'].search([]),
#         })

#     @http.route('/helpdesk_assigned_group/helpdesk_assigned_group/objects/<model("helpdesk_assigned_group.helpdesk_assigned_group"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('helpdesk_assigned_group.object', {
#             'object': obj
#         })