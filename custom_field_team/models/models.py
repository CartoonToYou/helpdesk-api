# -*- coding: utf-8 -*-

from odoo import models, fields, api

class custom_field_team(models.Model):
  _inherit = 'helpdesk.ticket.team'
#     _name = 'custom_field_team.custom_field_team'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100