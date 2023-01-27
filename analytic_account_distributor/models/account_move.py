from odoo import models, fields, api, _


class AccountMoveLines(models.Model):
    _inherit = 'account.move.line'

    def _get_analytic_distribution(self):
        for record in self:
            account_analytic_distribution_models = self.env['account.analytic.distribution.model'].search([])
            for account_analytic_distribution_model in account_analytic_distribution_models:
                length = len(account_analytic_distribution_model.account_prefix)
                if record.account_id.code[:length] == account_analytic_distribution_model.account_prefix:
                    analytic_distribution_values = account_analytic_distribution_model.analytic_distribution
                    for key, value in analytic_distribution_values.items():
                        if not record.analytic_distribution:
                            record.write({
                                'analytic_distribution': {
                                    str(key): value
                                }
                            })
                        else:
                            analytic_plan_set = False
                            analytic_plan = self.env['account.analytic.account'].search([('id', '=', key)]).plan_id.id
                            if analytic_plan:
                                analytic_accounts = self.env['account.analytic.account'].search([('plan_id', '=', analytic_plan)])
                                for analytic_account in analytic_accounts:
                                    if str(analytic_account.id) in record.analytic_distribution:
                                        analytic_plan_set = True
                            if str(key) not in record.analytic_distribution and not analytic_plan_set:
                                values = record.analytic_distribution
                                values[str(key)] = value
                                record.write({
                                    'analytic_distribution': values
                                })
