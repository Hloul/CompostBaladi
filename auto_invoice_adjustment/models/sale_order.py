from odoo import fields, models, api


#class SaleOrder(models.Model):
#    _inherit = 'sale.order'
#
#    def _create_invoices(self, grouped=False, final=False, date=None):
#        moves = super(SaleOrder, self)._create_invoices(grouped=grouped, final=final, date=date)
#        for move in moves:
#            move.adjust_invoice()
#        return moves
