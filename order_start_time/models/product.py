# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    have_start_time = fields.Boolean(required=True, default=False,
        string='Have Start Time',
        help="This product have Start Time")
    