from odoo import models, fields, api, _
import base64
import requests
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta


class Vehicle(models.Model):
    _name = 'vehicle.vehicle'

    def name_get(self):
        res = []
        for loc in self:
            name = loc.name
            type = loc.type
            if type:
                if type == 'kapal':
                    nama_tipe = 'Kapal'
                    res.append((loc.id, '%s%s' % ('[%s] ' % nama_tipe, name)))
                elif type == 'mobil':
                    nama_tipe = 'Mobil'
                    res.append((loc.id, '%s%s' % ('[%s] ' % nama_tipe, name)))
                elif type == 'alat_berat':
                    nama_tipe = 'Alat Berat'
                    res.append((loc.id, '%s%s' % ('[%s] ' % nama_tipe, name)))
            else:
                res.append((loc.id, '%s' % (name)))
        return res

    def _compute_record_count(self):
        record_data = self.env['job.crew'].read_group(
            [('vehicle_id', 'in', self.ids)],
            ['vehicle_id'], ['vehicle_id'])
        result = dict((data['vehicle_id'][0], data['vehicle_id_count']) for data in record_data)
        for vehicle in self:
            vehicle.record_count = result.get(vehicle.id, 0)

    @api.depends('record_id.persentase')
    def _compute_persentase(self):
        for rec in self:
            total_percentage = 0
            total_summary=0.0
            for line in rec.record_id:
                if line.name:
                    total_percentage += line.persentase
                if total_percentage >0:
                    total_summary = (total_percentage/rec.record_count)*100
            rec.persentase = total_summary

    name = fields.Char(string='Name',
        required=False)

    brand = fields.Char(string='Brand',
        required=False)
    
    type = fields.Selection(
        string='Type',
        selection=[('kapal', 'Kapal'),
                   ('mobil', 'Mobil'),
                   ('alat_berat', 'Alat Berat'),],
        default='kapal',
        required=True,
        track_visibility='onchange',
        readonly=False,
    )

    code_vehicle = fields.Char(string="Code Vehicle",
                                 readonly=False,
                                 )

    record_count = fields.Integer(compute='_compute_record_count', string="Record Count")

    color = fields.Integer(string='Color Index')

    record_id = fields.One2many(
        'job.crew', 'vehicle_id',
        string='Job Crew',
        required=False)
    

    persentase = fields.Float(
        string='Persentase (%)',
        store=True,
        compute='_compute_persentase',
        readonly=True
    )

    active = fields.Boolean(
        string='Active',
        default=True,
        required=False)
    
    # Batas tambahan atas
    
    nopol = fields.Char(
        string = 'NO POLISI',
    )
    
    remarks_vehicle = fields.Char(
        string = 'remarks Vehicle',
        required=False
    )
    
    vehicle_image = fields.Binary(string="Image Vehicle",store=True)
    
    company = fields.Many2one('res.company','Armada')
    
    image_url = fields.Char(string="Image URL")

    @api.depends("image_url")
    def get_image_from_url(self):
        """This method mainly use to get image from the url"""
        image = False
        if self.image_url:
            if "http://" in self.image_url or "https://" in self.image_url:
                image = base64.b64encode(requests.get(self.image_url).content)
            else:
                if "file:" in self.image_url:
                    with open(self.image_url.split("file:///")[1], "rb") as file:
                        image = base64.b64encode(file.read())
                if "/home" in self.image_url:
                    with open(self.image_url, "rb") as file:
                        image = base64.b64encode(file.read())
        self.vehicle_image = image

    def write(self, value):
        rec = super(Vehicle, self).write(value)
        for img in self:  #
            if "image_url" in value:
                img.get_image_from_url()
        return rec
    
    # Batas tambahan bawah

