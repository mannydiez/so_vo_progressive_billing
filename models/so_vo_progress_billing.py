# -*- coding: utf-8 -*-
 
from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _order_count(self):
        obj = self.env['sale.order']
        for order in self:
            order.variation_order_count = obj.search_count([('sales_order', '=', order.id)])

    is_variation_order = fields.Boolean(string="Is a Variation Order", default=lambda *a: False, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    sales_order = fields.Many2one('sale.order', string="Sales Order", readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    billed = fields.Boolean(string="Billed", store=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    variation_order_count = fields.Integer(compute=_order_count, string="Variation Orders")
    
    @api.multi
    @api.onchange('partner_id')
    def compute_sales_order(self):
        if not self.partner_id:
            return {'domain': {'sales_order': []}}
        domain = {'sales_order': ['&',('partner_id', '=', self.partner_id.id), ('is_variation_order', '=', False), ('state','=','sale')]}
        result = {'domain': domain}
        return result

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'is_variation_order' in vals and vals.get('is_variation_order'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sale.order.vo') or _('New')
            elif 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'sale.order') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or _('New')

        # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            addr = partner.address_get(['delivery', 'invoice'])
            vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
            vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
            vals['pricelist_id'] = vals.setdefault('pricelist_id',
                                                   partner.property_product_pricelist and partner.property_product_pricelist.id)
        result = super(SaleOrder, self).create(vals)
        return result
