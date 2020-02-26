# -*- coding: utf-8 -*-

from odoo import models, fields, api

class custom_field_schedule(models.Model):
    _inherit = 'maintenance.request'
    end_date = fields.Date(string="End Date")