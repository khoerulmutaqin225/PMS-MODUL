from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta
import logging
_logger = logging.getLogger(__name__)
from collections import OrderedDict


class gas_maintenance_vehicle(models.Model):
    _name = 'gas.maintenance.vehicle'
    _description = 'Gas Maintenance Vehicle'
    # "Gas Maintenance Vendor"

    @api.onchange('vehicle_id')
    def _get_company(self):
        for record in self:
            if not record.vehicle_id:
                return {}
            else:
                # function query untuk mendeteksi nama perusahan yang sedang login
                x = self.env["res.company"].browse(self.env.company.id)
                self.company_id = x
                

        
    company_id = fields.Many2one(
        'res.company',
        compute='_get_company',
        string='Company Id',
    )    

    @api.model
    def create(self, values):
        res = super(gas_maintenance_vehicle,self).create(values)
        for rec in res:
            nama = rec.name
            if nama == 'New':
                names = self.env['ir.sequence'].next_by_code('gas.maintenance.vehicle')
                rec.update({'name':names})
        return res
    

    
            
    def open_records(self):
        ctx = dict(self._context)
        ctx.update({'search_gas_default_vehicle_id': self.id})
        action = self.env['ir.actions.act_window'].for_xml_id('pms_module', 'act_job_crew_3_record_all')
        return dict(action, context=ctx)
    
    
    name = fields.Char(string="No Berita Acara" , default="New")
    vehicle_id = fields.Many2one(
        'vehicle.vehicle',
        string='Vehicle',
        readonly=False,
        required=False, default=lambda self: self.env.context.get('gas_default_vehicle_id'),
        index=True, tracking=True, change_default=True)
    
    tanggal_kerusakan = fields.Date(string="Tanggal Kerusakan",
                                    required=False,
                                    readonly=False,
                                    select=True,
                                    default=lambda self: fields.datetime.now()
                                    )      
    
                                                                  
    pelapor = fields.Char(string="Pelapor")
    catatan = fields.Text(string="Catatan")
    status = fields.Selection(
        string='Status',
        selection=[('open', 'Open'),
                   ('progress', 'Progress'), 
                   ('finish', 'Finish') ],
        default='open',
        store=True,
        readonly=False,
    )
    
        
    jenis_downtime = fields.Selection(
        string='Jenis Perawatan',
        selection=[
            ('maintenance', 'Maintenance'),
            ('repair ', 'Repair '),
            ('breakdown ', 'Breakdown '),
        ],
    )    

    standar_lama = fields.Date(string="Tanggal Selesai" )      
    
    biaya_perbaikan = fields.Char(string="Estimasi Biaya")

    gas_line = fields.One2many(
        'gas.report.line', 
        'group_gas_id',
        string="List PErbaikan Sarfas",
        track_visibility='onchange'
    ) 
    


class gas_maintenance_vendor(models.Model):
    _name = "gas.maintenance.vendor"
    _description ="Gas Maintenance Vendor"

    name = fields.Char(string="Nama Vendor")

class gas_maintenance_vehicle_line(models.Model):
    _name = "gas.report.line"
    _description="Gas Report Line"

    @api.depends('start_perbaikan', 'finish_perbaikan')
    def _compute_date_difference(self):
        duration = 0
        for record in self:
            if record.start_perbaikan and record.finish_perbaikan:
                dt_1 = fields.Datetime.from_string(record.start_perbaikan)
                dt_2 = fields.Datetime.from_string(record.finish_perbaikan)
                # duration = (dt_2 - dt_1).days
                duration = (dt_2 - dt_1).total_seconds()
                record.update({'lama_perbaikan':duration})
            else:
                record.update({'lama_perbaikan':duration})                
    

    lama_perbaikan = fields.Integer(
        'Lama Perbaikan',
        compute='_compute_date_difference',
        store=True,
    )
    
    
    name = fields.Char(string="Nama Sarfas")
    jenis_sarfas = fields.Char(string="Jenis Sarfas")
    biaya_perbaikan = fields.Char(string="Biaya Perbaikan")
    uraian_pekerjaan = fields.Text('Uraian Pekerjaan')
    start_perbaikan = fields.Datetime(string="Tanggal Mulai")
    finish_perbaikan = fields.Datetime(string="Tanggal Selesai")
    
    
    
    km = fields.Char(string="Kilometer")    
    vendor = fields.Many2one('gas.maintenance.vendor', string='Vendor')
    
    
    
    status = fields.Selection(
        string='Status',
        selection=[('open', 'Open'),
                   ('progress', 'Progress'), 
                   ('finish', 'Finish') ],
        default='open',
        store=True,
        readonly=False,
    )
    
    group_gas_id = fields.Many2one(
        'gas.maintenance.vehicle',
        string='group_gas_id',
        readonly=True
    )
    

    
    