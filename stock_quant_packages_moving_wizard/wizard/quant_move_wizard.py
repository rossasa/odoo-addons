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

from openerp import models, fields, api
from openerp.exceptions import ValidationError


class StockQuantMove(models.TransientModel):
    _name = 'stock.quant.move'

    pack_move_items = fields.One2many(
        comodel_name='stock.quant.move_items', inverse_name='move_id',
        string='Packs')

    global_dest_loc = fields.Many2one(
        comodel_name='stock.location', string='Destination Location',
        required=True)
    
    is_manual_op = fields.Boolean(string=u"Manual Operation")

    picking_type_id = fields.Many2one('stock.picking.type', 'Picking Type', required=True)

    def default_get(self, cr, uid, fields, context=None):
        res = super(StockQuantMove, self).default_get(
            cr, uid, fields, context=context)
        quants_ids = context.get('active_ids', [])
        if not quants_ids:
            return res
        quant_obj = self.pool['stock.quant']
        quants = quant_obj.browse(cr, uid, quants_ids, context=context)
        items = []
        for quant in quants:
            if not quant.package_id:
                item = {
                    'quant': quant.id,
                    'source_loc': quant.location_id.id,
                    'qty': quant.qty
                }
                items.append(item)
        res.update(pack_move_items=items)
        return res

    @api.multi
    def do_transfer(self):
        self.ensure_one()
        quants = self.pack_move_items.mapped(lambda x: x.quant)
        qty_items = {}
        for item in self.pack_move_items:
            qty_items[item.quant.id] = item
        result = quants.move_to(self.global_dest_loc, self.picking_type_id, qty_items,self.is_manual_op)
        if self.is_manual_op:
            return {
                    'name': 'picking_form',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'stock.picking',
                    'res_id': result[0].picking_id.id
                }
        else :
            return result


class StockQuantMoveItems(models.TransientModel):
    _name = 'stock.quant.move_items'
    _description = 'Picking wizard items'

    move_id = fields.Many2one(
        comodel_name='stock.quant.move', string='Quant move')
    quant = fields.Many2one(
        comodel_name='stock.quant', string='Quant',
        domain=[('package_id', '=', False)])
    source_loc = fields.Many2one(
        comodel_name='stock.location', string='Source Location', required=True)
    dest_loc = fields.Many2one(
        comodel_name='stock.location', string='Destination Location')
    
    qty = fields.Float(string='Quantity', required=True)

    @api.one
    @api.onchange('quant')
    def onchange_quant(self):
        self.source_loc = self.quant.location_id

    @api.one
    @api.constrains('qty')
    def _check_description(self):
        if self.qty > self.quant.qty:
            raise ValidationError("Fields qty must be letter than initial quant quantity")
