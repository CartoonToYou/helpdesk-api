# -*- coding: utf-8 -*-

from odoo import models, fields, api

class helpdesk_assigned_group(models.Model):
   #_name = 'helpdesk_assigned_group' if have _name odoo will create new table
  _inherit = 'helpdesk.ticket'

  group_id = fields.Many2one('res.groups', string='Assigned Group', index=True)
