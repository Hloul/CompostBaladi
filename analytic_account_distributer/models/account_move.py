from odoo import models, fields, api, _


class AccountMoveLines(models.Model):
    _inherit = 'account.move.line'

    def _get_analytic_distribution(self):
        for record in self:
            analytic_plans = self.env['account.analytic.plan'].search([])
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
                            if str(key) not in record.analytic_distribution:
                                print('key not in analytic_distribution')
                                values = record.analytic_distribution
                                values[str(key)] = value
                                record.write({
                                    'analytic_distribution': values
                                })
