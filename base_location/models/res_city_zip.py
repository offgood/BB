# Copyright 2016 Nicolas Bessi, Camptocamp SA
# Copyright 2018 Aitor Bouzas <aitor.bouzas@adaptivecity.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from operator import index
from odoo import api, fields, models


class ResCityZip(models.Model):
    """City/locations completion object"""

    _name = "res.city.zip"
    _description = __doc__
    _order = "name asc"
    _rec_name = "display_name"

    details = fields.Char( "Details", required=True,index=True)
    name = fields.Char("ZIP", required=True,index=True)
    city_id = fields.Many2one(
        "res.city",
        "City",
        required=True,
        auto_join=True,
        ondelete="cascade",
        index=True
    )
    state_id = fields.Many2one(related="city_id.state_id")
    country_id = fields.Many2one(related="city_id.country_id")
    display_name = fields.Char(
        compute="_compute_new_display_name", store=True
    )

    _sql_constraints = [
        (
            "name_city_uniq",
            "UNIQUE(details, name, city_id)",
            "You already have a zip with that code in the same city. "
            "The zip code must be unique within it's city",
        )
    ]

    @api.depends("name", "details", "city_id", "city_id.state_id", "city_id.country_id")
    def _compute_new_display_name(self): #ตรวจทั้งหมดว่ามีไหม กันError 
        for rec in self:
            name = []
            if rec.details:
                name.append(rec.details)
            if rec.name:
                name.append(rec.name)
            if rec.city_id.name:
                name.append(rec.city_id.name)
            if rec.city_id.state_id:
                name.append(rec.city_id.state_id.name)
            if rec.city_id.country_id:
                name.append(rec.city_id.country_id.name)
            rec.display_name = ", ".join(name)
