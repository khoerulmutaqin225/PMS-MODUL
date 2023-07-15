from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta
import logging
_logger = logging.getLogger(__name__)

class gas_maintenance_vehicle(models.Model):
    _name = 'gas.maintenance.vehicle'
    
    def open_records(self):
        ctx = dict(self._context)
        ctx.update({'search_gas_default_vehicle_id': self.id})
        action = self.env['ir.actions.act_window'].for_xml_id('pms_module', 'act_job_crew_3_record_all')
        return dict(action, context=ctx)
    
    
    no_ba_o = fields.Char(string="No Berita Acara")
    tanggal_kerusakan = fields.Date(string="Tanggal Kerusakan")
    pelapor = fields.Char(string="Pelapor")
    vehicle_id = fields.Many2one(
        'vehicle.vehicle',
        string='Vehicle',
        readonly=True,
        required=False, default=lambda self: self.env.context.get('gas_default_vehicle_id'),
        index=True, tracking=True, change_default=True)
    catatan = fields.Char(string="Catatan")
    status = fields.Selection(
        string='Status',
        selection=[('open', 'Open'),
                   ('progress', 'Progress'), 
                   ('finish', 'Finish') ],
        default='open',
        store=True,
        readonly=True,
    )