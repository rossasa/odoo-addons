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

from openerp import fields, models, api


class StockComputeAll(models.TransientModel):
    _inherit = 'procurement.order.compute.all'

    compute_all = fields.Boolean(string=u"Traiter l'ensemble des produits", default=True)
    product_ids = fields.Many2many('product.product', string=u"Produits à traiter")

    @api.multi
    def procure_calculation(self):
        proc_obj = self.env['procurement.order']
        for company_id in self.env.user.company_ids.ids:
            proc_obj.with_context(compute_product_ids=self.product_ids.ids, compute_all_products=self.compute_all).\
                _procure_orderpoint_confirm(use_new_cursor=self.env.cr.dbname, company_id=company_id)
        return {}
