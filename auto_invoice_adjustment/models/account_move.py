from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    adjust_move_id = fields.Many2one('account.move')
    llc_currency_rate = fields.Float(string='LLS currency rate')
    lls_tax_amount = fields.Float(string='LLS Tax Amount')
    lbp_currency_id = fields.Many2one('res.currency', compute='get_lbp_currency')

    def get_lbp_currency(self):
        for rec in self:
            lbp = self.env['res.currency'].search([('name', '=', 'LBP')])
            rec.lbp_currency_id = lbp.id

    def adjust_invoice(self):
        lbp = self.env['res.currency'].search([('name', '=', 'LBP')])
        if (self.move_type == 'out_invoice' or self.move_type == 'out_refund') and self.currency_id.id != lbp.id:
            lls = self.env['res.currency'].search([('name', '=', 'LLS')])
            receivable_line = self.line_ids.filtered(lambda l: l.display_type == 'payment_term')
            tax_line = self.line_ids.filtered(lambda l: l.display_type == 'tax')
            if tax_line: 
               tax = self.env['account.tax'].search([('name','=',tax_line.name + ' @ Sayrafa')])
            if receivable_line and tax_line:
                receivable_account = receivable_line.account_id
                tax_line = tax_line[0]
                tax_account = tax_line.account_id
                original_tax = tax_line.credit or tax_line.debit
                original_tax_amount_currency = tax_line.amount_currency
                # adjust line 1
                lines = [(0, 0, {
                    'name': 'Remove VAT USD',
                    'account_id': receivable_account.id,
                    'tax_ids': [(6, 0, tax.ids)],
                    'credit': tax_line.credit if self.move_type == 'out_invoice' else 0,
                    'debit': tax_line.debit if self.move_type == 'out_refund' else 0,
                    'currency_id': self.currency_id.id,
                    'amount_currency': original_tax_amount_currency,
                    'partner_id': self.partner_id.id,
                })]
                # adjust line 2
                lls_tax_amount_conversion_rate = self.env['res.currency']._get_conversion_rate(
                    self.currency_id, lls, self.env.company, self.invoice_date or self.date
                )
                lls_tax_amount = lls_tax_amount_conversion_rate * original_tax_amount_currency
                new_tax_amount_conversion_rate = self.env['res.currency']._get_conversion_rate(
                    lbp, self.env.company.currency_id, self.env.company, self.invoice_date or self.date
                )
                new_tax_amount = lls_tax_amount * new_tax_amount_conversion_rate
                self.llc_currency_rate = lls_tax_amount_conversion_rate
                self.lls_tax_amount = abs(lls_tax_amount)
                lines.append((0, 0, {
                    'name': 'Put VAT in LBP',
                    'account_id': receivable_account.id,
                    'tax_ids': [(6, 0, tax.ids)],
                    'credit': new_tax_amount if self.move_type == 'out_refund' else 0,
                    'debit': -new_tax_amount if self.move_type == 'out_invoice' else 0,
                    'currency_id': lbp.id,
                    'partner_id': self.partner_id.id,
                    'amount_currency': -lls_tax_amount
                }))
                adjust_move = self.env['account.move'].with_context(check_move_validity=False, adjust=True).create({
                    'partner_id': self.partner_id.id,
                    'ref': 'adjust VAT for ' + self.name,
                    'invoice_date': self.invoice_date,
                    'date': self.date,
                    'move_type': 'entry',
                    'line_ids': lines,
                })
                self.write({
                    'adjust_move_id': adjust_move.id
                })
        if (self.move_type == 'in_invoice' or self.move_type == 'in_refund') and self.currency_id.id != lbp.id:
            lls = self.env['res.currency'].search([('name', '=', 'LLS')])
            payable_line = self.line_ids.filtered(lambda l: l.display_type == 'payment_term')
            tax_line = self.line_ids.filtered(lambda l: l.display_type == 'tax')
            if tax_line: 
                tax = self.env['account.tax'].search([('name','=',tax_line.name + ' @ Sayrafa')])
            if payable_line and tax_line:
                payable_account = payable_line.account_id
                tax_line = tax_line[0]
                tax_account = tax_line.account_id
                original_tax = tax_line.credit or tax_line.debit
                original_tax_amount_currency = tax_line.amount_currency
                # adjust line 1
                lines = [(0, 0, {
                    'name': 'Remove VAT USD',
                    'account_id': payable_account.id,
                    'tax_ids': [(6, 0, tax.ids)],
                    'credit': 0,
                    'debit': original_tax,
                    'credit': tax_line.credit if self.move_type == 'in_refund' else 0,
                    'debit': tax_line.debit if self.move_type == 'in_invoice' else 0,
                    'currency_id': self.currency_id.id,
                    'amount_currency': original_tax_amount_currency,
                    'partner_id': self.partner_id.id,
                })]
                # adjust line 2
                lls_tax_amount_conversion_rate = self.env['res.currency']._get_conversion_rate(
                    self.currency_id, lls, self.env.company, self.invoice_date or self.date
                )
                lls_tax_amount = lls_tax_amount_conversion_rate * original_tax_amount_currency
                new_tax_amount_conversion_rate = self.env['res.currency']._get_conversion_rate(
                    lbp, self.env.company.currency_id, self.env.company, self.invoice_date or self.date
                )
                new_tax_amount = lls_tax_amount * new_tax_amount_conversion_rate
                self.llc_currency_rate = lls_tax_amount_conversion_rate
                self.lls_tax_amount = abs(lls_tax_amount)
                lines.append((0, 0, {
                    'name': 'Put VAT in LBP',
                    'account_id': payable_account.id,
                    'tax_ids': [(6, 0, tax.ids)],
                    'credit': new_tax_amount if self.move_type == 'in_invoice' else 0,
                    'debit': -new_tax_amount if self.move_type == 'in_refund' else 0,
                    'currency_id': lbp.id,
                    'partner_id': self.partner_id.id,
                    'amount_currency': -lls_tax_amount
                }))
                adjust_move = self.env['account.move'].with_context(check_move_validity=False, adjust=True).create({
                    'partner_id': self.partner_id.id,
                    'ref': 'adjust VAT for ' + self.name,
                    'invoice_date': self.invoice_date,
                    'date': self.date,
                    'move_type': 'entry',
                    'line_ids': lines,
                })
                self.write({
                    'adjust_move_id': adjust_move.id
                })


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('partner_id')
    def _inverse_partner_id(self):
        if self.env.context.get('adjust'):
            return
        res = super(AccountMoveLine, self)._inverse_partner_id()
        return res

    @api.onchange('amount_currency', 'currency_id')
    def _inverse_amount_currency(self):
        if self.env.context.get('adjust'):
            return
        res = super(AccountMoveLine, self)._inverse_amount_currency()
        return res

    @api.onchange('debit')
    def _inverse_debit(self):
        if self.env.context.get('adjust'):
            return
        res = super(AccountMoveLine, self)._inverse_debit()
        return res

    @api.onchange('credit')
    def _inverse_credit(self):
        if self.env.context.get('adjust'):
            return
        res = super(AccountMoveLine, self)._inverse_credit()
        return res

    @api.onchange('account_id')
    def _inverse_account_id(self):
        if self.env.context.get('adjust'):
            return
        res = super(AccountMoveLine, self)._inverse_account_id()
        return res
