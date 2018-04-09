from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    have_start_time = fields.Boolean(related='product_id.have_start_time', readonly=True)
    start_time = fields.Datetime(string='Start Time')

    @api.one
    @api.constrains('start_time')
    def _check_start_time(self):
        if self.have_start_time:
            now = fields.Datetime.now()
            if not self.start_time:
                raise ValidationError(
                    _("Please enter Start Time"))
            if self.start_time < now:
                raise ValidationError(
                    _("Start Time cannot be before now"))

    @api.onchange('start_time')
    def start_time_change(self):
        if self.have_start_time:
            if self.start_time:
                now = fields.Datetime.now()
                if self.start_time < now:
                    self.start_time = now


    @api.multi
    def _prepare_invoice_line(self, qty):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        res = {}
        account = self.product_id.property_account_income_id or self.product_id.categ_id.property_account_income_categ_id
        if not account:
            raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                (self.product_id.name, self.product_id.id, self.product_id.categ_id.name))

        fpos = self.order_id.fiscal_position_id or self.order_id.partner_id.property_account_position_id
        if fpos:
            account = fpos.map_account(account)

        res = {
            'name': self.name,
            'sequence': self.sequence,
            'origin': self.order_id.name,
            'account_id': account.id,
            'price_unit': self.price_unit,
            'quantity': qty,
            'discount': self.discount,
            'uom_id': self.product_uom.id,
            'product_id': self.product_id.id or False,
            'layout_category_id': self.layout_category_id and self.layout_category_id.id or False,
            'invoice_line_tax_ids': [(6, 0, self.tax_id.ids)],
            'account_analytic_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
        }
        if self.have_start_time:
            res['start_time'] = self.start_time
        return res

