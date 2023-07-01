from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    company_currency_id2 = fields.Many2one(string='Second Company Currency', related='company_id.currency_id2',
                                          readonly=True, store=True)
    debit2 = fields.Monetary(string='Debit2', compute='_compute_debit2', currency_field='company_currency_id2',
                             store=True)
    credit2 = fields.Monetary(string='Credit2', compute='_compute_credit2', currency_field='company_currency_id2',
                             store=True)

    @api.depends('debit', 'company_currency_id2', 'currency_id')
    def _compute_debit2(self):
        for rec in self:
            rec.debit2 = False
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

    @api.depends('credit', 'company_currency_id2', 'currency_id')
    def _compute_credit2(self):
        for rec in self:
            rec.credit2 = False
            if rec.company_currency_id2 and rec.credit and rec.currency_id and (rec.move_id.invoice_date or rec.move_id.date):
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

