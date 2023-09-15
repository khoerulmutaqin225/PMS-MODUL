from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
# from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta
import logging
# from odoo.tools import float_round

_logger = logging.getLogger(__name__)
from collections import OrderedDict


class gas_maintenance_vehicle(models.Model):
    _name = 'gas.maintenance.vehicle'
    _inherit ='mail.thread'
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
                

    currency_id = fields.Many2one('res.currency',related='company_id.currency_id') 
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
    
    
    name = fields.Char(string="No Berita Acara" , default="New" ,track_visibility='onchange')
    no_ba_close = fields.Char(string="No Berita Close" ,track_visibility='onchange')
    vehicle_id = fields.Many2one(
        'vehicle.vehicle',
        string='Vehicle',
        readonly=False,
        domain="[('type', '=', 'mobil')]",  # Tambahkan domain ini
        required=False, default=lambda self: self.env.context.get('gas_default_vehicle_id'),
        index=True, tracking=True, change_default=True  ,track_visibility='onchange')
    
    tanggal_kerusakan = fields.Datetime(string="Tanggal Kerusakan",
                                    required=False,
                                    readonly=False,
                                    select=True,
                                    default=lambda self: fields.datetime.now()
                             ,track_visibility='onchange')   
    
                                                                  
    pelapor = fields.Char(string="Pelapor" ,track_visibility='onchange')
    catatan = fields.Text(string="Catatan" ,track_visibility='onchange')
    status = fields.Selection(
        string='Status',
        selection=[('open', 'Open'),
                   ('progress', 'Progress'), 
                   ('finish', 'Finish') ],
        default='open',
        store=True,
        readonly=False,
        track_visibility='onchange')
    
    @api.constrains('status', 'note_image')
    def _check_status_image(self):
        for record in self:
            if record.status == 'finish' and not record.note_image:
                raise ValidationError("Tidak dapat menetapkan status Master ke 'Selesai'. Jika nota belum di Upload .")
            if record.status == 'finish':
                print("OK")

    @api.constrains('status')
    def _check_status(self):
        for record in self:
            if record.status == 'finish' and self.env['gas.report.line'].search([('group_gas_id', '=', record.id), ('status', '!=', 'finish')]):
                raise ValidationError("Tidak dapat menetapkan status Master ke 'Selesai'. Jika masih ada pekerjaan yang berjalan .")
            if record.status == 'finish':
                # Pengkondisian untuk menghilangkan 1 Indek setelah (/O)
                if record.name and record.name.endswith('/O'):
                    ba_close =  record.name.rsplit('/',1)[0]
                    no_ba_close = ba_close + "/C"
                    record.no_ba_close = no_ba_close
                else:
                    record.no_ba_close = record.name      
            if record.status == 'open':
                ba_close =''
                record.no_ba_close = ba_close

            if record.status == 'progress':
                ba_close =''
                record.no_ba_close = ba_close
              
    
    # standar_lama = fields.Date(string="Tanggal Selesai"  ,track_visibility='onchange')     

    standar_lama = fields.Datetime(string='Tanggal Selesai', compute='_compute_tanggal', store=True, track_visibility='onchange')    
    
    @api.depends('gas_line.start_perbaikan', 'gas_line.finish_perbaikan')
    def _compute_tanggal(self):
        for master in self:
            child_dates = master.gas_line.mapped('finish_perbaikan')
            if child_dates:
                # Pilih tanggal terbesar/terlama
                master.standar_lama = max(child_dates)
                x = max(child_dates)
                print(x)
            else:
                master.standar_lama = False    
    
    biaya_perbaikan = fields.Monetary(string='Estimasi Biaya', store=True, readonly=True, compute='_amount_all' ,track_visibility='onchange')
    gas_line = fields.One2many(
        'gas.report.line', 
        'group_gas_id',
        string="List PErbaikan Sarfas",
        track_visibility='onchange'
    ) 
    
    vendor = fields.Many2one('gas.maintenance.vendor', string='Vendor' ,track_visibility='onchange')   
    
    @api.depends('gas_line.biaya_perbaikan')
    def _amount_all(self):
        for rec in self:
            jumlah = 0.0
            for line in rec.gas_line:
                jumlah+= line.biaya_perbaikan
            currency = rec.currency_id or self.env.company.currency_id                
            rec.update({
                'biaya_perbaikan': currency.round(jumlah)
            })
        

    vehicle_image1 = fields.Binary(string="Foto Open 1",store=True ,track_visibility='onchange')
    vehicle_image2 = fields.Binary(string="Foto Open 2",store=True ,track_visibility='onchange')
    vehicle_image3 = fields.Binary(string="Foto Open 3",store=True ,track_visibility='onchange')
    
    vehicle_image4 = fields.Binary(string="Foto Close 1",store=True ,track_visibility='onchange')
    vehicle_image5 = fields.Binary(string="Foto Close 2",store=True ,track_visibility='onchange')
    vehicle_image6 = fields.Binary(string="Foto Close 3",store=True ,track_visibility='onchange')
    
    note_image = fields.Binary(string="Foto Nota",store=True ,track_visibility='onchange')
    
    discount = fields.Monetary(string='Diskon' ,track_visibility='onchange')
    
    final_price = fields.Monetary(string='Harga Akhir', store=True, readonly=True, compute='_final_price' ,track_visibility='onchange')
    
        
    @api.depends('final_price', 'discount', 'biaya_perbaikan')
    def _final_price(self):
        for record in self:
            if not record.discount:
                record.final_price = 0.0
            else:
                currency = record.currency_id or self.env.company.currency_id  
                final_price   = record.biaya_perbaikan - record.discount
                record.final_price = final_price
            

class gas_maintenance_vendor(models.Model):
    _name = "gas.maintenance.vendor"
    _description ="Gas Maintenance Vendor"

    name = fields.Char(string="Nama Vendor")
    
    number = fields.Char('Telepon')
    
    alamat = fields.Char(string="Alamat")
    
    ktp = fields.Binary('KTP')
    
    accountNumber = fields.Char(string="Nomor Rekening")
    
    NPWP = fields.Binary('NPWP')
    
    

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
    biaya_perbaikan = fields.Float(string="Biaya Perbaikan", default=0.0 )
    uraian_pekerjaan = fields.Text('Uraian Pekerjaan')
    start_perbaikan = fields.Datetime(string="Tanggal Mulai")
    finish_perbaikan = fields.Datetime(string="Tanggal Selesai")

    currency_id = fields.Many2one('res.currency',related='group_gas_id.currency_id')
    
    
    km = fields.Char(string="Kilometer", default="0")    
    
    
    
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
        
    jenis_downtime = fields.Selection(
        string='Jenis Perawatan',
        selection=[
            ('maintenance', 'Maintenance'),
            ('repair ', 'Repair '),
            ('breakdown ', 'Breakdown '),
            ('downtime ', 'Downtime '),
        ], default='maintenance'
    )    
    

    
    