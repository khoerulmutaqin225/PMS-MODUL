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
    # Tambahan atas

    def name_get(self):
        for rec in self:
            vehicle_id = rec.vehicle_id.display_name
            date_evidence = rec.date_evidence
            date_evidence = date_evidence.strftime("%d %B %Y")
        data= []
        for template in self:
            # template.id tidak akan dibaca
            dto = (template.id, '%s%s%s%s%s%s%s' % (vehicle_id," ","-"," ","(",date_evidence,")"))
            data.append(dto)
        return data 
        
    x_percentage_evidence = fields.Integer('Persentasi (Required 0-100)', store=True,)
    x_moon_evidence = fields.Selection(
        string='Bulan Evidence',
        selection=[('januari', 'Januari'),
                   ('februari', 'Februari'),
                   ('maret', 'Maret'),
                   ('april', 'April'),
                   ('mei', 'Mei'),
                   ('juni', 'Juni'),
                   ('juli', 'Juli'),
                   ('agustus', 'Agustus'),
                   ('septermber', 'September'),
                   ('oktober', 'Oktober'),
                   ('november', 'November'),
                   ('desember', 'Desember'),
                   ]
    )
    
    
    @api.onchange('x_percentage_evidence')
    def get_percentage_evidence(self):
        data = self.x_percentage_evidence
        if not data:
            return data
        else:
            if data < 0:
                raise ValidationError("Nilai tidak boleh kurang dari 0.")
            if data > 100:
                raise ValidationError("Nilai tidak boleh lebih dari 100.")
            else:
                self.x_percentage_evidence = data
    
    
    @api.onchange('date_evidence')
    def get_date_evidence(self):
        data = self.date_evidence
        # ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        if not data:
            return data
        else:            
            dto =  (data.strftime("%B"))
            if dto == 'January':
                data = 'januari'
            elif dto == 'February':
                data = 'februari'
            elif dto == 'March':
                data = 'maret'
            elif dto == 'April':
                data = 'april'
            elif dto == 'May':
                data = 'mei'
            elif dto == 'June':
                data = 'juni'
            elif dto == 'July':
                data = 'juli'
            elif dto == 'August':
                data = 'agustus'
            elif dto == 'September':
                data = 'septermber'
            elif dto == 'October':
                data = 'oktober'
            elif dto == 'November':
                data = 'november'
            elif dto == 'December':
                data = 'Desember'
        self.x_moon_evidence = data
    
    
    # Tambahan bawah