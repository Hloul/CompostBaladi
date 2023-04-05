# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ActivityTag(models.Model):
    _name = "activity.tag"
    _description = "Activity Tag"

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color')
    number = fields.Integer('Number')
