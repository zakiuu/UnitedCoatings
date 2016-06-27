# -*- coding: utf-8 -*-
#
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Codewr (<http://www.codewr.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from openerp import api
from openerp import fields
from openerp import models


class SaleShop(models.Model):

    """
    Create new model representing different shops for a company
    where the warehouse, invoice address, and shipping address
    are specified.
    """

    _name = 'sale.shop'
    _description = 'Sales shop'

    name = fields.Char(string='Name',
                       required=True,
                       copy=False,
                       select=True)

    warehouse_id = fields.Many2one(string='Warehouse',
                                   comodel_name='stock.warehouse',
                                   required=True,
                                   copy=False,
                                   select=True)

    company_id = fields.Many2one(string='Company',
                                 default=lambda self: self.env['res.company'].
                                                      _company_default_get('justice.case'))

    invoice_address_id = fields.Many2one(string='Invoice Address',
                                         comodel_name='res.partner',
                                         required=True,
                                         copy=False,
                                         select=True)

    shipping_address_id = fields.Many2one(string='Shipping Address',
                                          comodel_name='res.partner',
                                          required=True,
                                          copy=False,
                                          select=True)

    _sql_constraints = [('uniq_shop_name', 'unique(name)', 'Shop name must be unique'),
                        ('unique_warehouse_id', 'unique(warehouse_id)', 'Warehouse must be affected to only one shop')]

    @api.onchange('warehouse_id')
    def _onchange_warehouse_id(self):
        self.shipping_address_id = self.warehouse_id.partner_id.id


class SaleOrder(models.Model):

    """
    Inherit the sale.order object to add the shop attribute
    """

    _inherit = 'sale.order'

    shop_id = fields.Many2one(string='Shop',
                              comodel_name='sale.shop')

    @api.onchange('shop_id')
    def _onchange_shop_id(self):
        self.warehouse_id = self.shop_id.warehouse_id.id

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        vals = super(SaleOrder, self)._prepare_invoice(cr, uid, order, lines, context)
        vals.update({'shop_id': order.shop_id.id})
        return vals


class AccountInvoice(models.Model):

    """
    Inherit the account.invoice object to add the shop to the invoice
    """

    _inherit = 'account.invoice'

    shop_id = fields.Many2one(string='Shop', comodel_name='sale.shop')

    invoice_address_id = fields.Many2one(string='Invoice Address',
                                         related='shop_id.invoice_address_id')


class StockPicking(models.Model):
    """
    Inherit the stock.picking model to override the method
    responsible in creating the invoice object
    """

    _inherit = 'stock.picking'

    def _get_invoice_vals(self, cr, uid, key, inv_type, journal_id, move, context=None):
        """
            Override the function to add shop_id attribute to the returned vals
        """
        vals = super(StockPicking, self)._get_invoice_vals(cr, uid, key, inv_type, journal_id, move, context)
        shop = self.pool.get('sale.shop').search(
            cr, uid, [('warehouse_id', '=', move.picking_id.picking_type_id.warehouse_id.id)])

        vals.update({'shop_id': shop[0]})
        return vals

