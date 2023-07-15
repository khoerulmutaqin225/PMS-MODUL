from odoo import models, fields, api, _
import base64
import requests
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta

class job_crew_evidence(models.Model):
    _name = 'job.crew.evidence'
    
    vehicle_id = fields.Many2one('vehicle.vehicle',string='Vehicle')
    date_evidence = fields.Date(string='Tanggal Evidence')
    file_evidence = fields.Binary(string="Bukti Evidence Excel/PDF",store=True, required=True)
    keterangan = fields.Char(string='Catatan Evidence', required=False)