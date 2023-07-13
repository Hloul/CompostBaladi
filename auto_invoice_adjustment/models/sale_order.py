from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    adjust_move_id = fields.Many2one('account.move')
    llc_currency_rate = fields.Float(string='LLS currency rate')
    lls_tax_amount = fields.Float(string='LLS Tax Amount')
    lbp_currency_id = fields.Many2one('res.currency', compute='get_lbp_currency')

    def get_lbp_currency(self):
        for rec in self:
            lbp = self.env['res.currency'].search([('name', '=', 'LBP')])
            rec.lbp_currency_id = lbp.id


#    def _create_invoices(self, grouped=False, final=False, date=None):
#        moves = super(SaleOrder, self)._create_invoices(grouped=grouped, final=final, date=date)
#        for move in moves:
#            move.adjust_invoice()
#        return moves
