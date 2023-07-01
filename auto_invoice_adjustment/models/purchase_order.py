from odoo import fields, models, api


#class PurchaseOrder(models.Model):
#    _inherit = 'purchase.order'
#
#    def action_create_invoice(self):
#        res = super(PurchaseOrder, self).action_create_invoice()
#        for invoice in self.invoice_ids:
#            invoice.adjust_invoice()
#        return res
