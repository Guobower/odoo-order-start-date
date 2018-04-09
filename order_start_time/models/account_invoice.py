from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    have_start_time = fields.Boolean(related='product_id.have_start_time', readonly=True)
    start_time = fields.Datetime(string='Start Time')


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    def inv_line_characteristic_hashcode(self, invoice_line):
        """Add start Time to hashcode used when the option "Group
        Invoice Lines" is active on the Account Journal"""
        code = super().inv_line_characteristic_hashcode(
            invoice_line
        )
        hashcode = '%s-%s-%s' % (
            code,
            invoice_line.get('start_time', 'False'),
        )
        return hashcode

    @api.model
    def line_get_convert(self, line, part):
        """Copy from invoice to move lines"""
        res = super().line_get_convert(line, part)
        res['start_time'] = line.get('start_time', False)
        return res

    @api.model
    def invoice_line_move_line_get(self):
        """Copy from invoice line to move lines"""
        res = super().invoice_line_move_line_get()
        ailo = self.env['account.invoice.line']
        for move_line_dict in res:
            iline = ailo.browse(move_line_dict['invl_id'])
            move_line_dict['start_time'] = iline.start_time
        return res

    @api.multi
    def action_move_create(self):
        """Check that products with have_start_time have Start Time and invoice have_start_time"""
        for invoice in self:
            for iline in invoice.invoice_line_ids:
                if iline.product_id and iline.product_id.have_start_time:
                    if not iline.start_time:
                        raise UserError(_(
                            "Missing Start Time for invoice "
                            "line with Product '%s' which suppose to have Start Time'.")
                            % (iline.product_id.name))
        return super().action_move_create()

    