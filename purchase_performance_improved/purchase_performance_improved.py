# -*- coding: utf8 -*-
#
# Copyright (C) 2015 NDP Systèmes (<http://www.ndp-systemes.fr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv


class Purchase(osv.osv):

    def _amount_all_improved(self, cr, uid, ids, field_name, arg, context=None):
        result = self.pool.get('purchase.order')._amount_all(cr, uid, ids, field_name, arg, context=context)
        return result

    def _get_order_improved(self, cr, uid, ids, context=None):
        result = self.pool.get('purchase.order')._get_order(cr, uid, ids, context=context)
        return result

    _columns = {
        'amount_untaxed': fields.function(_amount_all_improved, digits_compute=dp.get_precision('Account'), string='Untaxed Amount',
                                          store={
            'purchase.order.line': (_get_order_improved, ['product_qty', 'date_planned', 'taxes_id',
                                                          'product_uom', 'product_id', 'move_ids', 'price_unit',
                                                          'order_id', 'account_analytic_id',
                                                          'company_id', 'state', 'invoice_lines', 'invoiced',
                                                          'partner_id', 'date_order', 'procurement_ids'], 10),
        }, multi="sums", help="The amount without tax", track_visibility='always'),
        'amount_tax': fields.function(_amount_all_improved, digits_compute=dp.get_precision('Account'), string='Taxes',
                                      store={
            'purchase.order.line': (_get_order_improved, ['product_qty', 'date_planned', 'taxes_id',
                                                          'product_uom', 'product_id', 'move_ids', 'price_unit',
                                                          'order_id', 'account_analytic_id',
                                                          'company_id', 'state', 'invoice_lines', 'invoiced',
                                                          'partner_id', 'date_order', 'procurement_ids'], 10),
        }, multi="sums", help="The tax amount"),
        'amount_total': fields.function(_amount_all_improved, digits_compute=dp.get_precision('Account'), string='Total',
                                        store={
            'purchase.order.line': (_get_order_improved, ['product_qty', 'date_planned', 'taxes_id',
                                                          'product_uom', 'product_id', 'move_ids', 'price_unit',
                                                          'order_id', 'account_analytic_id',
                                                          'company_id', 'state', 'invoice_lines', 'invoiced',
                                                          'partner_id', 'date_order', 'procurement_ids'], 10),
        }, multi="sums", help="The total amount")
    }
    _inherit = ['purchase.order']
    _description = "Purchase Order"
    _order = 'date_order desc, id desc'
