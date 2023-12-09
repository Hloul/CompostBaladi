import logging
from odoo import fields, models, api

_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    company_currency_id2 = fields.Many2one(string='Second Company Currency', related='company_id.currency_id2',
                                          readonly=True)
    conversion_rate = fields.Float(string='Conversion Rate', compute='_compute_conversion_rate')
    debit2 = fields.Monetary(string='Debit2', currency_field='company_currency_id2')
    credit2 = fields.Monetary(string='Credit2', currency_field='company_currency_id2')

    @api.depends('debit', 'credit', 'company_currency_id2', 'currency_id')
    def _compute_conversion_rate(self):
        _logger.info('Compute Run')
        for rec in self:
            rec.debit2 = 0
            rec.credit2 = 0
            if rec.debit and rec.company_currency_id2 and rec.currency_id and (rec.move_id.invoice_date or rec.move_id.date):
                main_currency = self.env.company.currency_id
                from_currency = rec.currency_id
                to_currency = self.env.company.currency_id2
                if from_currency.id == to_currency.id:
                    rec.debit2 = abs(rec.amount_currency)
                else:
                    if main_currency.id == from_currency.id:
                        conversion_rate = self.env['res.currency']._get_conversion_rate(
                            from_currency, to_currency, self.env.company, rec.move_id.invoice_date or rec.move_id.date
                        )
                        rec.debit2 = rec.debit * conversion_rate
                    else:
                        conversion_rate = self.env['res.currency']._get_conversion_rate(
                            main_currency, to_currency, self.env.company, rec.move_id.invoice_date or rec.move_id.date
                        )
                        rec.debit2 = rec.debit * conversion_rate
            _logger.info('debit2 = %s', rec.debit2)
            if rec.credit and rec.company_currency_id2 and rec.currency_id and (rec.move_id.invoice_date or rec.move_id.date):
                main_currency = self.env.company.currency_id
                from_currency = rec.currency_id
                to_currency = self.env.company.currency_id2
                if from_currency.id == to_currency.id:
                    rec.credit2 = abs(rec.amount_currency)
                else:
                    if main_currency.id == from_currency.id:
                        conversion_rate = self.env['res.currency']._get_conversion_rate(
                            from_currency, to_currency, self.env.company, rec.move_id.invoice_date or rec.move_id.date
                        )
                        rec.credit2 = rec.credit * conversion_rate
                    else:
                        conversion_rate = self.env['res.currency']._get_conversion_rate(
                            main_currency, to_currency, self.env.company, rec.move_id.invoice_date or rec.move_id.date
                        )
                        rec.credit2 = rec.credit * conversion_rate
            _logger.info('credit2 = %s', rec.credit2)
