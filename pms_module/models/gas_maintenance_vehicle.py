from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
# from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta
import logging
# from odoo.tools import float_round
# tambahan
import io
from PIL import Image
import base64




class inherite_res_company(models.Model):
    _inherit ='res.company'
    _description = 'res_company'
    
    kop_surat_1 = fields.Binary('Kop Surat 1')
    kop_surat_2 = fields.Binary('Kop Surat 2')
    kop_surat_3 = fields.Binary('Kop Surat 3')
    
    
    
    

class gas_maintenance_vehicle(models.Model):
    _name = 'gas.maintenance.vehicle'
    _inherit ='mail.thread'
    _description = 'Gas Maintenance Vehicle'




    # Batas Atas
    @api.depends('vehicle_image1','vehicle_image2', 'vehicle_image3', 'vehicle_image4', 'vehicle_image5' ,'vehicle_image6' , 'note_image')   
    def _compute_image_64(self):
        for template in self:
            if template.note_image:
                template.note_image = self._compress_image(template.note_image)
            if template.vehicle_image6:
                template.vehicle_image6 = self._compress_image(template.vehicle_image6)
            if template.vehicle_image5:
                template.vehicle_image5 = self._compress_image(template.vehicle_image5)
            if template.vehicle_image4:
                template.vehicle_image4 = self._compress_image(template.vehicle_image4)
            if template.vehicle_image3:
                template.vehicle_image3 = self._compress_image(template.vehicle_image3)
            if template.vehicle_image2:
                template.vehicle_image2 = self._compress_image(template.vehicle_image2)
            if template.vehicle_image1:
                template.vehicle_image1 = self._compress_image(template.vehicle_image1)

    def _set_image_64(self):
        for template in self:
            if template.note_image:
                template.note_image = self._compress_image(template.note_image)
            if template.vehicle_image6:
                template.vehicle_image6 = self._compress_image(template.vehicle_image6)
            if template.vehicle_image5:
                template.vehicle_image5 = self._compress_image(template.vehicle_image5)
            if template.vehicle_image4:
                template.vehicle_image4 = self._compress_image(template.vehicle_image4)
            if template.vehicle_image3:
                template.vehicle_image3 = self._compress_image(template.vehicle_image3)
            if template.vehicle_image2:
                template.vehicle_image2 = self._compress_image(template.vehicle_image2)
            if template.vehicle_image1:
                template.vehicle_image1 = self._compress_image(template.vehicle_image1)

    def _compress_image(self, image_data):
        # Decode the image data from base64
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))

        # Compress the image
        compressed_image = io.BytesIO()
        image.save(compressed_image, format='JPEG', optimize=True, quality=60)

        # Encode the compressed image data to base64
        return base64.b64encode(compressed_image.getvalue())
    
    image_1920     = fields.Binary("Image", compute='_compute_image_64', inverse='_set_image_64', store=True)
    image_1920_2   = fields.Binary("Image 2", compute='_compute_image_64', inverse='_set_image_64', store=True)
    vehicle_image1 = fields.Binary("Foto Open 1", compute='_compute_image_64', inverse='_set_image_64', store=True)
    vehicle_image2 = fields.Binary("Foto Open 2", compute='_compute_image_64', inverse='_set_image_64', store=True)
    vehicle_image3 = fields.Binary("Foto Open 3", compute='_compute_image_64', inverse='_set_image_64', store=True)
    vehicle_image4 = fields.Binary("Foto Open 4", compute='_compute_image_64', inverse='_set_image_64', store=True)
    vehicle_image6 = fields.Binary("Foto Open 5", compute='_compute_image_64', inverse='_set_image_64', store=True)
    note_image     = fields.Binary("Foto Open 6", compute='_compute_image_64', inverse='_set_image_64', store=True)
    
    # vehicle_image1 = fields.Binary( string="Foto Open 1", compute='_compute_image_64',  inverse='_set_image_64', store=True , track_visibility='onchange')
    # vehicle_image2 = fields.Binary( string="Foto Open 2",compute='_compute_image_64',  inverse='_set_image_64', store=True , track_visibility='onchange')
    # vehicle_image3 = fields.Binary( string="Foto Open 3", compute='_compute_image_64',  inverse='_set_image_64', store=True , track_visibility='onchange')
    # vehicle_image4 = fields.Binary( tring="Foto Close 1", compute='_compute_image_64',  inverse='_set_image_64', store=True , track_visibility='onchange')
    # vehicle_image5 = fields.Binary( tring="Foto Close 2", compute='_compute_image_64',  inverse='_set_image_64', store=True , track_visibility='onchange')
    # vehicle_image6 = fields.Binary( tring="Foto Close 3", compute='_compute_image_64',  inverse='_set_image_64', store=True , track_visibility='onchange')
    # note_image     = fields.Binary( string="Foto Nota"  , compute='_compute_image_64',  inverse='_set_image_64', store=True , track_visibility='onchange')
    
    ttd_bu = fields.Binary('Anggota BU')
    pic_bu = fields.Binary('PIC BU')
    corlog = fields.Binary('Logistik')

    
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
       
    corporate = fields.Selection([
        ('GEMILANG KARYA ENERGI', 'PT. GEMILANG KARYA ENERGI'),
        ('DHIRABRATA GAS NUSANTARA', 'PT. DHIRABRATA GAS NUSANTARA'),
        ('SEGAH PRIMA GAS', 'PT. SEGAH PRIMA GAS'),
        ('PASER ENERGY ABADI', 'PT. PASER ENERGY ABADI'),
        ('GEMILANG ENERGY NUSANTARA', 'PT. GEMILANG ENERGY NUSANTARA'),
        ('SANGKULIRANG ENERGI UTAMA', 'PT. SANGKULIRANG ENERGI UTAMA'),
        ('BAROKAH GEMILANG PERKASA', 'PT. BAROKAH GEMILANG PERKASA'),
        ('ANUGERAH SANGATTA ENERGI ', 'PT. ANUGERAH SANGATTA ENERGI '),
        ('BERKAH ETAM NUSANTARA', 'PT. BERKAH ETAM NUSANTARA'),
        ('SINERGI JAYA ENERGI', 'PT. SINERGI JAYA ENERGI'),
        ('ANUGERAH SANGATTA ENERGI', 'PT. ANUGERAH SANGATTA ENERGI'),
        ('TAKA ENERGY NUSANTARA', 'PT. TAKA ENERGY NUSANTARA'),
    ], string='corporate' , required=True, default=None)    
    
    ppn = fields.Float(string='PPN (10 %)' , default=0.0)
    pph = fields.Float(string='PPH (2 %)' , default=0.0)

    global switch
    def switch(data):
        alamat = data
        # Split Awal
        data = (alamat.split())
        # Split Kedua
        data_1 = data[0]
        data_2 = data[1]
        data_3 = data[2]
        data.remove(data[0])
        # Split Ketiga
        data_1 = data_1[0]
        data_2 = data_2[0]
        data_3 = data_3[0]
        data = data_1 + data_2 + data_3
        return data
    
    global converse
    def converse(no, corp, month, year):
        data = corp
        increment = '%03d' % no
        short = switch(data)
        data = increment + '/' +  short + '/GAS/SGT' + '/' + str(month) + '/' + str(year) + "/O"
        print(data)
        return data
    
    global intToRoman
    def intToRoman(num):
        dict = {1: "I",2: "II",3: "III",4: "IV",5: "V",6: "VI",7: "VII",8: "VIII",9: "IX",10: "X",
                11: "XI",12: "XII",13: "XIII",14: "XIV",15: "XV",16: "XVI",17: "XVII",18: "XVIII",19: "XIX",20: "XX",
                21: "XXI",22: "XXII",23: "XXIII",24: "XXIV",25: "XXV",26: "XXVI",27: "XXVII",28: "XXVIII",29: "XXIX",30: "XXX",30: "XXXI"}
        data = (dict[num])
        return data

    
    
    @api.model
    def create(self, values):
        res = super(gas_maintenance_vehicle,self).create(values)
        for rec in res:
            nama = rec.name
            data = ''
            if nama == 'New':
                perusahaan = rec.corporate
                increment =  self.env['gas.maintenance.vehicle'].search([('corporate', '=', rec.corporate)])
                length  = len(increment)
                no = length
                bulan = rec.create_date.month
                bulan = intToRoman(bulan)                
                year = rec.create_date.year                
                names = converse(no,perusahaan,bulan,year)
                rec.update({'name':names})
        return res
    

    
            
    def open_records(self):
        ctx = dict(self._context)
        ctx.update({'search_default_vehicle_id': self.id})
        action = self.env['ir.actions.act_window'].for_xml_id('pms_module', 'act_job_crew_3_record_all')
        return dict(action, context=ctx)
    
    
    name = fields.Char(string="No Berita Acara" , default="New" ,track_visibility='onchange')
    no_ba_close = fields.Char(string="No Berita Close" ,track_visibility='onchange')
    vehicle_id = fields.Many2one(
        'vehicle.vehicle',
        string='Vehicle',
        readonly=False,
        domain="[('type', '=', 'mobil')]",  # Tambahkan domain ini
        required=False, default=lambda self: self.env.context.get('default_vehicle_id'),
        index=True, tracking=True, change_default=True  ,track_visibility='onchange')
    brand = fields.Char('Merek', related='vehicle_id.brand')
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
    
    discount = fields.Float(string='Diskon' , default=0.0)
    
    final_price = fields.Monetary(string='Harga Akhir', store=True, readonly=True, compute='_final_price' ,track_visibility='onchange')
    
        
    @api.depends('final_price', 'discount', 'biaya_perbaikan','ppn','pph')
    def _final_price(self):
        for record in self:
            if not record.discount:
                data = record.biaya_perbaikan
                
                record.final_price = data + record.pph + record.ppn
                
            else:
                currency = record.currency_id or self.env.company.currency_id  
                final_price   = record.biaya_perbaikan - record.discount
                record.final_price = final_price + record.pph + record.ppn
                
    def debug_gas(self):
        print("Hello World")

        data = self.env['gas.maintenance.vehicle'].search([('id', '=', self.id)])
        name                =[]
        brand               =[]
        pelapor             =[]
        status              =[]
        vendor              =[]
        corporate           =[]
        tanggal_kerusakan   =[]
        standar_lama        =[]
        biaya_perbaikan     =[]
        discount            =[]
        final_price         =[]
        no_ba_close         = []
        kop_surat           = []
        ttd                 = []
        
                
        data_list = {
                'id': id,
                'name': name,
                'brand': brand,
                'pelapor': pelapor,
                'status': status,
                'vendor': vendor,
                'corporate': corporate,
                'tanggal_kerusakan': tanggal_kerusakan,
                'standar_lama': standar_lama,
                'biaya_perbaikan': biaya_perbaikan,
                'discount': discount,
                'final_price': final_price,
                'no_ba_close': no_ba_close,
                'kop_surat': kop_surat,
                'ttd': ttd,
            }
        nama                    = []
        jenis_sarfas            = []
        uraian_pekerjaan        = []
        line_biaya_perbaikan    = []
        code   = []
        vol    = []
        sat    = []
        supply = []

        dict_list = {
                'id': id,
                'nama': nama,
                'jenis_sarfas': jenis_sarfas,
                'uraian_pekerjaan': uraian_pekerjaan,
                'line_biaya_perbaikan': line_biaya_perbaikan,
                'code'  : code,
                'vol'   : vol,
                'sat'   : sat,
                'supply': supply
            }
        
        for line in data:
            rec_name                = line.name
            rec_brand               = line.brand
            rec_pelapor             = line.pelapor
            rec_status              = line.status
            rec_vendor              = line.vendor.name.upper()
            rec_vendor              = "BENGKEL " + rec_vendor
            rec_corporate           = line.corporate
            rec_tanggal_kerusakan   = line.tanggal_kerusakan
            rec_standar_lama        = line.standar_lama
            
            rec_biaya_perbaikan     = line.biaya_perbaikan
            rec_discount            = line.discount
            rec_final_price         = line.final_price
            rec_no_ba_close         = line.no_ba_close
            # Foto pertamina + seu
            kop_surat_1 = self.company_id.kop_surat_1
            # Foto pertamina + seu
            kop_surat_2 = self.company_id.kop_surat_2
            # Foto pertamina + seu
            kop_surat_2_copy = self.company_id.kop_surat_2
            # Foto Kosong
            kop_surat_3 = self.company_id.kop_surat_3
            # ttd
            ttd_1 = self.pic_bu
            ttd_2 = self.corlog
            ttd_3 = self.ttd_bu
            
            ttd.append(ttd_1)            
            ttd.append(ttd_2)            
            ttd.append(ttd_3)            
            
            kop_surat.append(kop_surat_1)            
            kop_surat.append(kop_surat_2)            
            kop_surat.append(kop_surat_2_copy)            
            kop_surat.append(kop_surat_3)            

            name.append(rec_name)
            brand.append(rec_brand)
            pelapor.append(rec_pelapor)
            status.append(rec_status)
            vendor.append(rec_vendor)
            corporate.append(rec_corporate)
            tanggal_kerusakan.append(rec_tanggal_kerusakan)
            standar_lama.append(rec_standar_lama)
            biaya_perbaikan.append(rec_biaya_perbaikan)
            discount.append(rec_discount)
            final_price.append(rec_final_price)
            no_ba_close.append(rec_no_ba_close)            
            
            for list in line.gas_line:
                rec_nama = list.name
                rec_jenis_sarfas = list.jenis_sarfas
                rec_uraian_pekerjaan = list.uraian_pekerjaan
                rec_line_biaya_perbaikan = list.biaya_perbaikan
                code = 'NULL'
                vol = 1
                sat     = "UNIT"
                supply  = "SGT"

                # append
                nama.append(rec_nama)
                jenis_sarfas.append(rec_jenis_sarfas)
                uraian_pekerjaan.append(rec_uraian_pekerjaan)
                line_biaya_perbaikan.append(rec_line_biaya_perbaikan) 
                


                    
        # print(data_list[0][0])
        # print("test")
        testt = ["HERU", "LATIFA", "SILVIA"]
        master = ["HERU", "LATIFA", "SILVIA"]                        
        master_data = ["HERU", "LATIFA", "SILVIA"]        
        data={
            'form':self.read()[0],
            'testt': testt,
            'master': master,
            'master_data': master_data,
            'data_list':data_list,
            'dict_list':dict_list,
        }
        return self.env.ref('pms_module.actions_print_gas_maintenance_vehicle').report_action(self, data=data)          

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
        ondelete='cascade',
        readonly=True
    )
    
    no_ba_open =  fields.Char('NO BA (OPEN)' , related= "group_gas_id.name", readonly=True, store=True )
    
    no_ba_close = fields.Char('NO BA (CLOSE)',  related="group_gas_id.no_ba_close", readonly=True, store=True )
    
    corporate = fields.Selection([
        ('GEMILANG KARYA ENERGI', 'PT. GEMILANG KARYA ENERGI'),
        ('DHIRABRATA GAS NUSANTARA', 'PT. DHIRABRATA GAS NUSANTARA'),
        ('SEGAH PRIMA GAS', 'PT. SEGAH PRIMA GAS'),
        ('PASER ENERGY ABADI', 'PT. PASER ENERGY ABADI'),
        ('GEMILANG ENERGY NUSANTARA', 'PT. GEMILANG ENERGY NUSANTARA'),
        ('SANGKULIRANG ENERGI UTAMA', 'PT. SANGKULIRANG ENERGI UTAMA'),
        ('BAROKAH GEMILANG PERKASA', 'PT. BAROKAH GEMILANG PERKASA'),
        ('ANUGERAH SANGATTA ENERGI ', 'PT. ANUGERAH SANGATTA ENERGI '),
        ('BERKAH ETAM NUSANTARA', 'PT. BERKAH ETAM NUSANTARA'),
        ('SINERGI JAYA ENERGI', 'PT. SINERGI JAYA ENERGI'),
        ('ANUGERAH SANGATTA ENERGI', 'PT. ANUGERAH SANGATTA ENERGI'),
        ('TAKA ENERGY NUSANTARA', 'PT. TAKA ENERGY NUSANTARA'),
    ], string='corporate' , required=True, related="group_gas_id.corporate")  
        
    tanggal_kerusakan = fields.Datetime('Tanggal Downtime',  related="group_gas_id.tanggal_kerusakan", readonly=True, store=True )
    
    pelapor = fields.Char('Pelapor',  related="group_gas_id.pelapor", readonly=True, store=True )
    
    vehicle_id = fields.Many2one(
        'vehicle.vehicle',
        string='Vehicle',
        related="group_gas_id.vehicle_id")
    
    # vehicle_id = fields.Char('NO POLISI',  related="group_gas_id.vehicle_id", readonly=True, store=True )
    
    brand = fields.Char('Jenis Kendaraan',  related="group_gas_id.brand", readonly=True, store=True )
    vendor = fields.Many2one('gas.maintenance.vendor', string='Vendor' ,track_visibility='onchange', related="group_gas_id.vendor")   
       
    # vendor = fields.Char('Jenis Kendaraan',  related="group_gas_id.vendor", readonly=True, store=True )
        
    jenis_downtime = fields.Selection(
        string='Jenis Perawatan',
        selection=[
            ('maintenance', 'Maintenance'),
            ('repair ', 'Repair '),
            ('breakdown ', 'Breakdown '),
            ('downtime ', 'Downtime '),
        ], default='maintenance'
    )    
    

    
    