from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
# from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta
import logging
# from odoo.tools import float_round
import io
from PIL import Image
import base64

_logger = logging.getLogger(__name__)
from collections import OrderedDict


class gas_maintenance_vehicle(models.Model):
    _name = 'gas.maintenance.vehicle'
    _inherit = 'mail.thread'
    _description = 'Gas Maintenance Vehicle'

    def unlink(self):
        alloc_to_unlink = self.env["gas.maintenance.vehicle"].search([('id', '=', self.id)])
        for record in self:
            if record.state != 'draft':
                raise ValidationError("Rubah dahulu menjadi draft .")
        data = super(gas_maintenance_vehicle, self).unlink()
        return data
    
    state = fields.Selection(
        string='State',
        selection=[
            ('draft', 'Draft'),
            ('approved', 'Approved'),
            ('done', 'Done'),
        ],
        default='approved',
        store=True,
        readonly=False,
        track_visibility='onchange')

    def action_draft(self):
        self.write({'state': 'draft'})

    def buttonCorpLog(self):
        corlog = self.env["res.users"].search([('name', '=', 'HAKIM')])
        pic_bu = self.env["res.users"].search([('name', '=', 'SYARIFAH HUZAIFAH')])
        bu_seu = self.env["res.users"].search([('name', '=', 'FAJAR GUMILANG')])
        company_id = self.env.company.id
        self.write({'state': 'done'})
        #[5] PT ARMADA SAMUDRA GLOBAL
        #[6] PT BAHTERA NUSANTARA INTERNASIONAL
        #[7] PT BAROKAH GEMILANG PERKASA
        # if (company_id in [5, 6, 7]):
        if company_id:
            return self.write({
                'sign_corlog': corlog.sign_x,
                'pic_seu': pic_bu.sign_x,
                'bu_seu':bu_seu.sign_x,
            })
        # elif (company_id == 41):
        #     return self.write({
        #         'sign_corlog': corlog.sign_x,
        #         'sign_bisnis_pic': pic_bu_bgp_02.sign_x,
        #     })
        else:
            return self.write({
                'sign_corlog': corlog.sign_x,
                'sign_bisnis_pic': False,
            })
    sign_corlog = fields.Binary('Logistik')
    pic_seu     = fields.Binary('PIC BU')
    bu_seu      = fields.Binary('Anggota BU')

    # "Gas Maintenance Vendor"
    @api.depends('vehicle_image1', 'vehicle_image2', 'vehicle_image3', 'vehicle_image4', 'vehicle_image5',
                 'vehicle_image6', 'note_image')
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
    
    vehicle_image1 = fields.Binary("Foto Open 1", compute='_compute_image_64', inverse='_set_image_64', store=True ,track_visibility='onchange')
    vehicle_image2 = fields.Binary("Foto Open 2", compute='_compute_image_64', inverse='_set_image_64', store=True, track_visibility='onchange')
    vehicle_image3 = fields.Binary("Foto Open 3", compute='_compute_image_64', inverse='_set_image_64', store=True, track_visibility='onchange')
    vehicle_image4 = fields.Binary("Foto Close 1", compute='_compute_image_64', inverse='_set_image_64', store=True, track_visibility='onchange')
    vehicle_image5 = fields.Binary("Foto CLose 2", compute='_compute_image_64', inverse='_set_image_64', store=True, track_visibility='onchange')
    vehicle_image6 = fields.Binary("Foto Close 3", compute='_compute_image_64', inverse='_set_image_64', store=True, track_visibility='onchange')
    note_image = fields.Binary("Foto Nota 1", compute='_compute_image_64', inverse='_set_image_64', store=True, track_visibility='onchange')

    note_image1 = fields.Binary(string="Foto Nota 5",store=True ,track_visibility='onchange')
    note_image2 = fields.Binary(string="Foto Nota 2",store=True ,track_visibility='onchange')
    note_image3 = fields.Binary(string="Foto Nota 3",store=True ,track_visibility='onchange')
    note_image4 = fields.Binary(string="Foto Nota 4",store=True ,track_visibility='onchange')
    @api.onchange('vehicle_id')
    def _get_company(self):
        for record in self:
            if not record.vehicle_id:
                return {}
            else:
                # function query untuk mendeteksi nama perusahan yang sedang login
                x = self.env["res.company"].browse(self.env.company.id)
                self.company_id = x
                

    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    company_id = fields.Many2one(
        'res.company',
        compute='_get_company',
        string='Company Id',
    )
    
       
    corporate_select = fields.Many2one('gas.maintenance.corporate', string='Perusahaan' ,track_visibility='onchange')

    @api.onchange('corporate', 'corporate_select')
    def get_price(self):
        rec_corp = self.corporate
        data =  self.env['gas.maintenance.corporate'].search([('key', '=', rec_corp)])
        if data:
            self.corporate_select = data
        else:
            print("Data Kosong")
            self.corporate_select = False
            print("Data Kosong")
    
    
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
        ('BANUA SANGGAM JAYA GAS','PT. BANUA SANGGAM JAYA GAS'),
        ('NIAGA ENERGI PERKASA','PT. NIAGA ENERGI PERKASA'),
        ('ENERGI BENUA ETAM','PT. ENERGI BENUA ETAM'),
        ('SUKSES MAJU ENERGI','PT. SUKSES MAJU ENERGI'),
    ], string='corporate', required=True, default=None)

    ppn = fields.Float(string='PPN (10 %)', default=0.0, compute='get_price_pph_ppn',)
    pph = fields.Float(string='PPH (2 %)', default=0.0, compute='get_price_pph_ppn',)

    pph_check = fields.Boolean(default=False, string='PPH (2 %)')
    ppn_check = fields.Boolean(default=False, string='PPN (10 %)')
    
    @api.onchange('pph_check','ppn_check','ppn','pph')
    def get_price_pph_ppn(self):
        if not self.ppn_check and not self.pph_check :
            self.pph = 0.0
            self.ppn = 0.0
        elif self.ppn_check and not self.pph_check:
            self.ppn = round((self.biaya_perbaikan * 0.1),  2)
            self.pph = 0.0
        elif not self.ppn_check and self.pph_check:
            self.pph = round((self.biaya_perbaikan * 0.02), 2)
            self.ppn = 0.0
        else:
            self.ppn = round((self.biaya_perbaikan * 0.1),  2)
            self.pph = round((self.biaya_perbaikan * 0.02), 2)    

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

    # fungsi untuk mengambil data dari field nama,perusahaan,bulan dan tahun dan memanggil function converse
    global converse

    def converse(no, corp, month, year):
        data = corp
        # nama Agen dan wilayahnya
        agen = {
            # "Wilayah" : "Code Wilayah"
            "PASER ENERGY ABADI":"PSR",
            "DHIRABRATA GAS NUSANTARA":"TGG",
            "TAKA ENERGY NUSANTARA":"PAM",
            "GEMILANG ENERGY NUSANTARA":"SMD",
            "GEMILANG KARYA ENERGI":"BTG",
            "BERKAH ETAM NUSANTARA":"PDN",
            "BAROKAH GEMILANG PERKASA":"BPN",
            "ANUGERAH SANGATTA ENERGI":"SGA",
            "SEGAH PRIMA GAS":"BRU",
            "SANGKULIRANG ENERGI UTAMA":"SGA",
            "SINERGI JAYA ENERGI":"BPN",
            "BANUA SANGGAM JAYA GAS":"BRU",
            "NIAGA ENERGI PERKASA":"MLK",
            "ENERGI BENUA ETAM":"SMD",
            "SUKSES MAJU ENERGI":"PDN",
        }
        agen = agen[corp]

        increment = '%03d' % no
        short = switch(data)
        data = increment + '/' + short + '/GAS/'+ agen + '/' + str(month) + '/' + str(year) + "/O"
        print(data)
        return data

    global intToRoman

    def intToRoman(num):
        dict = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X",
                11: "XI", 12: "XII", 13: "XIII", 14: "XIV", 15: "XV", 16: "XVI", 17: "XVII", 18: "XVIII", 19: "XIX",
                20: "XX",
                21: "XXI", 22: "XXII", 23: "XXIII", 24: "XXIV", 25: "XXV", 26: "XXVI", 27: "XXVII", 28: "XXVIII",
                29: "XXIX", 30: "XXX", 30: "XXXI"}
        data = (dict[num])
        return data

    @api.model
    def create(self, values):
        data = values
        res = super(gas_maintenance_vehicle, self).create(values)
        for rec in res:
            nama = rec.name
            data = ''
            # untuk cek apakah  ada  vendor telah di isi jika tidak maka akan error karena belum memilih vendor
            for dict_vendor in rec.gas_vendor_transfer_line:
                if dict_vendor.number == False:
                    raise ValidationError(("Vendor wajib di isi"))
            if nama == 'New':
                perusahaan = rec.corporate
                increment =  self.env['gas.maintenance.vehicle'].search([('corporate', '=', rec.corporate)])
                length  = len(increment)
                no = 0
                if length == 1:
                    no = 1
                else:
                    dto_length = length - 2
                    last_record = increment[dto_length].name
                    data = last_record
                    data = data.split("/",1)
                    key = int(data[0]) 
                    print ("Value Data : ", data)
                    no = int(data[0])
                    no += 1                     
                bulan = rec.create_date.month
                bulan = intToRoman(bulan)
                year = rec.create_date.year
                names = converse(no,perusahaan,bulan,year)
                # Check Duplicate
                rec.update({'name': names})
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
    tanggal_kerusakan = fields.Date(string="Tanggal Kerusakan",
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
              
    

    standar_lama = fields.Datetime(string='Tanggal Selesai', compute='_compute_tanggal', store=True, track_visibility='onchange')    
    
    @api.depends('gas_line.start_perbaikan', 'gas_line.finish_perbaikan')
    def _compute_tanggal(self):
        virtual_data = []
        for master in self:
            for rec in master.gas_line:
                data = rec.finish_perbaikan
                if data and data != False:
                    virtual_data.append(data)
                else:
                    print("No Data")
        virtual_data.sort(reverse=True)
        print(virtual_data)
        if virtual_data:
            result = virtual_data[0]
            master.update({'standar_lama': result})
        else:
            master.update({'standar_lama': False})
        

                 
    
    biaya_perbaikan = fields.Monetary(string='Estimasi Biaya', store=True, readonly=True, compute='_amount_all' ,track_visibility='onchange')
    gas_line = fields.One2many(
        'gas.report.line',
        'group_gas_id',
        string="List PErbaikan Sarfas",
        track_visibility='onchange'
    ) 
    
    # gas.maintenance.vendor
    gas_vendor_transfer_line = fields.One2many(
        'gas.maintenance.vendor.transfer',
        'group_vendor_transfer_gas_id',
        string="List Vendor",
        track_visibility='onchange'
    )
    

    vendor = fields.Many2one('gas.maintenance.vendor', string='Vendor')

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
    


    discount = fields.Float(string='Diskon', track_visibility='onchange', default=0.0)
    afterDiscount = fields.Float(string='Diskon' , default=0.0)
    final_price = fields.Monetary(string='Harga Akhir', store=True, readonly=True, compute='_final_price',
                                  track_visibility='onchange')

    @api.depends('final_price', 'discount', 'biaya_perbaikan', 'ppn', 'pph', 'afterDiscount', 'pph_check', 'ppn_check')
    def _final_price(self):
        for record in self:
            if not record.discount:
                data = record.biaya_perbaikan
                record.final_price = data + record.pph + record.ppn
                record.afterDiscount = data

            else:
                currency = record.currency_id or self.env.company.currency_id
                final_price   = record.biaya_perbaikan - record.discount
                record.afterDiscount = final_price
                record.final_price = final_price + record.pph + record.ppn

    def debug_gas(self):
        print("Hello World")

        data = self.env['gas.maintenance.vehicle'].search([('id', '=', self.id)])
        name = []
        brand = []
        pelapor = []
        status = []
        vendor = []
        corporate = []
        tanggal_kerusakan = []
        standar_lama = []
        biaya_perbaikan = []
        discount = []
        final_price = []
        no_ba_close = []
        kop_surat = []
        ttd = []

        pph = []
        ppn = []
        afterDiscount = []
        cuy = [1, 2, 3, 4]
        text_value = []
        foto = []
        foto2 = []

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
            'afterDiscount': afterDiscount,
            'ppn': ppn,
            'pph': pph,
            'cuy': cuy,
            'text_value': text_value,
            'foto': foto,
            'foto2': foto2,
        }
        nama = []
        jenis_sarfas = []
        uraian_pekerjaan = []
        line_biaya_perbaikan = []
        code = []
        vol = []
        sat = []
        supply = []

        dict_list = {
            'id': id,
            'nama': nama,
            'jenis_sarfas': jenis_sarfas,
            'uraian_pekerjaan': uraian_pekerjaan,
            'line_biaya_perbaikan': line_biaya_perbaikan,
            'code': code,
            'vol': vol,
            'sat': sat,
            'supply': supply
        }

        for line in data:
            rec_name = line.name
            rec_brand = line.brand
            rec_pelapor = line.pelapor
            rec_status = line.status
            rec_vendor = line.vendor.name.upper()
            rec_vendor = "BENGKEL " + rec_vendor
            rec_corporate = line.corporate
            rec_tanggal_kerusakan = line.tanggal_kerusakan
            rec_standar_lama = line.standar_lama
            rec_vehicle_image1 = line.vehicle_image1
            rec_vehicle_image2 = line.vehicle_image2
            rec_vehicle_image3 = line.vehicle_image3
            rec_vehicle_image4 = line.vehicle_image4
            rec_vehicle_image5 = line.vehicle_image5
            rec_vehicle_image6 = line.vehicle_image6
            rec_note_image = line.note_image
            rec_ktp = line.vendor.ktp
            rec_no_rec = line.vendor.accountNumber
            rec_npwp = line.vendor.NPWP
            foto.append(rec_vehicle_image1)
            foto.append(rec_vehicle_image2)
            foto.append(rec_vehicle_image3)
            foto.append(rec_vehicle_image4)
            foto.append(rec_vehicle_image5)
            foto.append(rec_vehicle_image6)

            foto2.append(rec_note_image)
            foto2.append(rec_ktp)
            foto2.append(rec_no_rec)
            foto2.append(rec_npwp)

            rec_biaya_perbaikan = "Rp. " + str(f"{int(line.biaya_perbaikan):,}")
            rec_discount = "Rp. " + str(f"{int(line.discount):,}")
            rec_afterDiscount = "Rp. " + str(f"{int(line.afterDiscount):,}")
            rec_ppn = "Rp. " + str(f"{int(line.ppn):,}")
            rec_pph = "Rp. " + str(f"{int(line.pph):,}")
            Text_sample = "Pada hari jumat, 01 september 2023 kami memberitahukan bahwa akan dilakukan perbaikan roda belakang bocor pada skid Hino 500 KT 8061 RN Di bengkel JAYA MANDIRI yang berlokasi di Jln. Kawasan Rt. 06, Gg. Keluarga, Kel. Jawa, Kec. Sanga - Sanga, Kutai Kartenegara, Kaltim . Dengan gambar sebagai berikut :"
            Katas = "\t{}".format(Text_sample)
            text_value.append(Katas)

            rec_final_price = "Rp. " + str(f"{int(line.final_price):,}")
            rec_no_ba_close = line.no_ba_close
            # Foto pertamina + seu
            kop_surat_1 = self.corporate_select.kop_surat_1
            # Foto pertamina + seu
            kop_surat_2 = self.corporate_select.kop_surat_2
            # Foto pertamina + seu
            kop_surat_2_copy = self.corporate_select.kop_surat_2
            # Foto Kosong
            kop_surat_3 = self.corporate_select.kop_surat_3
            # ttd
            ttd_1 = self.pic_seu
            ttd_2 = self.sign_corlog
            ttd_3 = self.bu_seu

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
            afterDiscount.append(rec_afterDiscount)
            ppn.append(rec_ppn)
            pph.append(rec_pph)

            final_price.append(rec_final_price)
            no_ba_close.append(rec_no_ba_close)

            for list in line.gas_line:
                rec_nama = list.name
                rec_jenis_sarfas = list.jenis_sarfas
                rec_uraian_pekerjaan = list.uraian_pekerjaan
                rec_line_biaya_perbaikan = "Rp. " + str(f"{int(list.biaya_perbaikan):,}")
                code = 'NULL'
                vol = 1
                sat = "UNIT"
                supply = "SGT"

                # append
                nama.append(rec_nama)
                jenis_sarfas.append(rec_jenis_sarfas)
                uraian_pekerjaan.append(rec_uraian_pekerjaan)
                line_biaya_perbaikan.append(rec_line_biaya_perbaikan)

        # print(data_list[0][0])
        # print("test")
        data = {
            'form': self.read()[0],
            'data_list': data_list,
            'dict_list': dict_list,
        }
        return self.env.ref('pms_module.actions_print_gas_maintenance_vehicle').report_action(self, data=data)


class gas_maintenance_corporate(models.Model):
    _name = "gas.maintenance.corporate"
    _description ="Gas Maintenance Corporate"

    name = fields.Char(string="Nama corporate")
    key = fields.Char(string="Key Corporate")
    
    kop_surat_1 = fields.Binary("Kop Surat 1" )
    kop_surat_2 = fields.Binary("Kop Surat 2")
    kop_surat_3 = fields.Binary("Kop Surat 3")
    
    


class gas_maintenance_vendor_transfer(models.Model):
    _name = "gas.maintenance.vendor.transfer"
    _inherit = 'mail.thread'
    _description ="Gas Maintenance Vendor Transfer"
    
    group_vendor_transfer_gas_id = fields.Many2one(
        'gas.maintenance.vehicle',
        string='ID',
    )    
    
    name = fields.Many2one(
        'gas.maintenance.vendor',
        string='Nama Vendor',
    )    
    
    number = fields.Char('Telepon' , track_visibility='onchange', related='name.number', )

    alamat = fields.Char(string="Alamat", track_visibility='onchange' , related='name.alamat', )

    accountNumber = fields.Char(string="Nomor Rekening" , track_visibility='onchange' , related='name.accountNumber', )
    bankName = fields.Char('Nama Bank' , related='name.bankName', )
    
    ownerBank = fields.Char('Nama Pemilik' , related='name.ownerBank', )
    
 
    photoAcountBank = fields.Binary("Foto Buku Rekening" , related='name.photoAcountBank', )
    ktp = fields.Binary("Foto Ktp" , related='name.ktp', )
    NPWP = fields.Binary("Foto NPWP" , related='name.NPWP', )
    

class gas_maintenance_vendor(models.Model):
    _name = "gas.maintenance.vendor"
    _inherit = 'mail.thread'
    _description ="Gas Maintenance Vendor"
    name = fields.Char(string="Nama Vendor", track_visibility='onchange')

    number = fields.Char('Telepon' , track_visibility='onchange')

    alamat = fields.Char(string="Alamat", track_visibility='onchange')

    accountNumber = fields.Char(string="Nomor Rekening" , track_visibility='onchange')
    bankName = fields.Char('Nama Bank')
    
    ownerBank = fields.Char('Nama Pemilik')
    
 
    photoAcountBank = fields.Binary("Foto Buku Rekening")
    ktp = fields.Binary("Foto Ktp")
    NPWP = fields.Binary("Foto NPWP")
    
    group_vendor_gas_id = fields.Many2one(
        'gas.maintenance.vehicle',
        string='group_gas_vendor_id',
        readonly=True
    )    

class gas_maintenance_vehicle_line(models.Model):
    _name = "gas.report.line"
    _inherit = 'mail.thread'
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
                record.update({'lama_perbaikan': duration})
            else:
                record.update({'lama_perbaikan': duration})

    lama_perbaikan = fields.Integer(
        'Lama Perbaikan',
        compute='_compute_date_difference',
        store=True,
    )
    
    
    @api.onchange('name', 'name_selection')
    def get_name_sarfas(self):
        data = self.name_selection
        if not data:
            print("Tidak ada data")
            self.name = False
        else:
            print("Ada data")
            self.name = data
    
    @api.onchange('jenis_sarfas', 'jenis_sarfas_selection')
    def get_jenis_sarfas_sarfas(self):
        data = self.jenis_sarfas_selection
        if not data:
            print("Tidak ada data")
            self.jenis_sarfas = False
        else:
            print("Ada data")
            self.jenis_sarfas = data
            
    name = fields.Char(string="Nama Sarfas")
    
    
    # name_selection = fields.Selection([
    #     ('Engine', 'Engine'),
    #     ('Clutch', 'Clutch'),
    #     ('Gearbox', 'Gearbox'),
    #     ('Control', 'Control'),
    #     ('Accelerator', 'Accelerator'),
    #     ('Frame', 'Frame'),
    #     ('Suspension', 'Suspension'),
    #     ('Front Axle', 'Front Axle'),
    #     ('Rear Axle', 'Rear Axle'),
    #     ('Wheels', 'Wheels'),
    #     ('Propeller Shaft', 'Propeller Shaft'),
    #     ('Brakes', 'Brakes'),
    #     ('Steering', 'Steering'),
    #     ('Fuel System', 'Fuel System'),
    #     ('Exhaust System', 'Exhaust System'),
    #     ('Radiator', 'Radiator'),
    #     ('Electricals', 'Electricals'),
    #     ('Emblem', 'Emblem'),
    #     ('Body', 'Body'),
    #     ('Load Body', 'Load Body'),
    # ], string="Nama Sarfas Selection")
    name_selection = fields.Char('Nama Sarfas')  
    
    jenis_sarfas_selection = fields.Selection([
        ('Engine', 'Engine'),
        ('Clutch', 'Clutch'),
        ('Gearbox', 'Gearbox'),
        ('Control', 'Control'),
        ('Accelerator', 'Accelerator'),
        ('Frame', 'Frame'),
        ('Suspension', 'Suspension'),
        ('Front Axle', 'Front Axle'),
        ('Rear Axle', 'Rear Axle'),
        ('Wheels', 'Wheels'),
        ('Propeller Shaft', 'Propeller Shaft'),
        ('Brakes', 'Brakes'),
        ('Steering', 'Steering'),
        ('Fuel System', 'Fuel System'),
        ('Exhaust System', 'Exhaust System'),
        ('Radiator', 'Radiator'),
        ('Electricals', 'Electricals'),
        ('Emblem', 'Emblem'),
        ('Body', 'Body'),
        ('Load Body', 'Load Body'),
    ], string="Jenis Sarfas Selection")
        
    jenis_sarfas = fields.Char(string="Jenis Sarfas")
    biaya_perbaikan = fields.Float(string="Biaya Perbaikan", default=0.0)
    uraian_pekerjaan = fields.Text('Uraian Pekerjaan')
    start_perbaikan = fields.Datetime(string="Tanggal Mulai")
    finish_perbaikan = fields.Datetime(string="Tanggal Selesai")

    currency_id = fields.Many2one('res.currency',related='group_gas_id.currency_id')
    
    
    km = fields.Char(string="Kilometer", default="0")    
    
    
    
    status = fields.Selection(
        string='Status',
        selection=[('open', 'Open'),
                   ('progress', 'Progress'),
                   ('finish', 'Finish')],
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
    ], string='Perusahaan' , required=True, related="group_gas_id.corporate")

    tanggal_kerusakan = fields.Date('Tanggal Downtime',  related="group_gas_id.tanggal_kerusakan", readonly=True, store=True )

    pelapor = fields.Char('Pelapor',  related="group_gas_id.pelapor", readonly=True, store=True )

    vehicle_id = fields.Many2one(
        'vehicle.vehicle',
        string='Vehicle',
        related="group_gas_id.vehicle_id")
    
    # vehicle_id = fields.Char('NO POLISI',  related="group_gas_id.vehicle_id", readonly=True, store=True )
    
    brand = fields.Char('Jenis Kendaraan',  related="group_gas_id.brand", readonly=True, store=True )
    vendor = fields.Many2one('gas.maintenance.vendor', string='Vendor' ,track_visibility='onchange', related="group_gas_id.vendor")
    jenis_downtime = fields.Selection(
        string='Jenis Perawatan',
        selection=[
            ('maintenance', 'Maintenance'),
            ('repair ', 'Repair '),
            ('breakdown ', 'Breakdown '),
            ('downtime ', 'Downtime '),
        ], default='maintenance'
    )    
