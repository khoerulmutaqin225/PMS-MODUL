from odoo import models, fields, api, _
import base64
import requests
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta


class mom_request_ajustment(models.Model):
    _name = "mom.request.ajustment"

    name = fields.Date(
        string='Date',
        required=False)
    
    # group = fields.Selection([
    #     ('nlm', 'NLM'),
    #     ('weeklyMeeting', 'Weekly Meeting'),
    #     ('coordination', 'Coordination'),
    # ], string='Group')

class mom_request_bu(models.Model):
    _name = "mom.request.bu"

    name = fields.Char(
        string='Name',
        required=False)
    
    group = fields.Selection([
        ('nlm', 'NLM'),
        ('weeklyMeeting', 'Weekly Meeting'),
        ('coordination', 'Coordination'),
    ], string='Group')
    

class mom_request_divisi(models.Model):
    _name = "mom.request.divisi"

    name = fields.Char(
        string='Name',
        required=False)


class mom_request_line(models.Model):
    _name = "mom.request.line"
    _inherit ='mail.thread'
    
    def show_tree_view(self):
        tree_view_id = self.env['ir.model.data'].xmlid_to_res_id('pms_module.mom_request_tree')
        form_view_id = self.env['ir.model.data'].xmlid_to_res_id('pms_module.mom_request_form')
        # data = self.env['mom.request'].sudo().search([])        

     
        # Create the action server record with the "activity_user_type" field set
        action_user_type = 'user'  # Replace with the appropriate value
        action_server = self.env['ir.actions.server'].create({
            'name': 'Mom Request Pagination',
            'model_id': self.env.ref('pms_module.model_mom_request_line').id,
            'binding_model_id': self.env.ref('pms_module.model_mom_request_line').id,
            'state': 'code',
            'code': 'action=model.show_tree_view()',
            'activity_user_type': action_user_type  # Set this to the appropriate value
        })
                
        domain =[('status' , '=', 'open')]
        result={
            'name': 'Mom Request',
            'type': 'ir.actions.act_window',
            'views':[[tree_view_id, 'tree'],[form_view_id,'form']],
            'target': 'current',
            'res_model': 'mom.request.line',
            'domain': domain,
            'limit': 40
        }
        return result

    name = fields.Char(
        string='Topik',
        required=False,track_visibility='onchange')

    plan = fields.Char(
        string='Plan',
        required=False,track_visibility='onchange')

    status = fields.Selection(
        [
            ("open", "Open"),
            ("on_progress", "On Progress"),
            ("close", "Close"),
        ],
        default="open",
        track_visibility='onchange'
    )

    divisi = fields.Many2many(
        'mom.request.divisi',
        'mom_request_divisi_rel',
        'mom_request_divisi_id',
        'brand_id',
        string='Divisi Ids',track_visibility='onchange')

    businesunit = fields.Many2many(
        'mom.request.bu',
        'mom_request_bu_rel',
        'mom_request_bu_id',
        'brand_id',
        default=lambda self: self.env.context.get('default_businesunit'),
        string='Business Unit', track_visibility='onchange',
        # domain=lambda self:self._get_businesunit_domain()
        )
    

    ajustment = fields.Many2many(
        'mom.request.ajustment',
        'mom_request_ajustment_rel',
        'mom_request_ajustment_id',
        'brand_id',
        default=lambda self: self.env.context.get('default_ajustment'),
        string='Adjustment Target', track_visibility='onchange',
        # domain=lambda self:self._get_ajustment_domain()
        )
    
    # @api.model
    # def _get_businesunit_domain(self):
    #     if self.meetingType == 'NLM':
    #         return [('id', 'in', ['GALANGAN', 'FINANCE', 'TST','GAS','SUPPLY CHAIN'])]
    #     elif self.meetingType == 'weeklyMeeting':
    #         return [('id', 'in', ['FINANCE', 'GAS'])]
    #     elif self.meetingType == 'coordination':
    #         return [('id', 'in', ['GALANGAN'])]
    #     else:
    #         return []    
    
    
                
    pic = fields.Char(
        string='Pic',
        required=False,track_visibility='onchange')

    opendate = fields.Date('Open Date',track_visibility='onchange',default=fields.Date.today())
    deadline = fields.Date('Deadline',track_visibility='onchange')
    active = fields.Boolean(
        string='Active',
        default=False,
        required=False)

    changeDeadline = fields.Integer('Change Deadline', compute='get_deadline', store=True)
    
    @api.onchange('active', 'changeDeadline')
    def get_deadline(self):
        for record in self:
            active = record.active
            if active:
                data = 1
                record.changeDeadline = data
            else:
                data = 2
                record.changeDeadline = data

    closedate = fields.Date('Close Date',track_visibility='onchange')
    
    keterangan = fields.Text('Information', track_visibility='onchange')
    # issue = fields.Char('issue')
    issue = fields.Selection(
        [
            ("urgent", "Urgent"),
            ("major", "Major"),
            ("medium", "Medium"), 
            ("minor", "Minor"), 
            ("info", "Info"), 
        ],
        default="info",
        track_visibility='onchange'
    )
    
    meetingType = fields.Selection(
        string='Meeting Type',
        selection=[('NLM', 'NLM'),
                   ('weeklyMeeting', 'Weekly Meeting'),
                   ('coordination', 'Coordination'),
                   ]
    )
    
    actionPlane = fields.Text('Action Plane')

    @api.onchange('meetingType')
    def onchange_contrat_name(self):
        if self.meetingType:
            if self.meetingType == 'NLM':
                return {'domain': {'businesunit': [('group', '=', 'nlm')]}}
            elif self.meetingType == 'weeklyMeeting':
                return {'domain': {'businesunit': [('group', '=', 'weeklyMeeting')]}}
            elif self.meetingType == 'coordination':
                return {'domain': {'businesunit': [('group', '=', 'coordination')]}}

        # If no meetingType is selected or it doesn't match 'nlm' or 'weeklyMeeting', clear the domain
        return {'domain': {'businesunit': []}}

    


    nilai = fields.Text('Value (%)', track_visibility='onchange')

    # Batas Atas
    @api.onchange('issue', 'businesunit')
    def _check_status_issue(self):
        for record in self:
            data_busines_example = []
            for i in record.businesunit:
                x = i.name
                # Memasukan x kedalam array data_busines_example
                data_busines_example.append(x)

            # Data tanpa
            data = data_busines_example
            new_data = [value for value in data if value != 'NLM']
            print(new_data)
            array_tupple = tuple(new_data)
            data_nlm = self.env['mom.request.bu'].search([('name', 'in', array_tupple)])

            if record.issue == 'major':
                # Update record.businessunit field with data_nlm
                record.write({
                    'businesunit': [(6, 0, data_nlm.ids)]
                })
            elif record.issue == 'medium':
                # Update record.businessunit field with data_nlm
                record.write({
                    'businesunit': [(6, 0, data_nlm.ids)]
                })
            elif record.issue == 'minor':
                # Update record.businessunit field with data_nlm
                record.write({
                    'businesunit': [(6, 0, data_nlm.ids)]
                })
            elif record.issue == 'info':
                # Update record.businessunit field with data_nlm
                record.write({
                    'businesunit': [(6, 0, data_nlm.ids)]
                })

            print(record.businesunit)
            print("Nice")

    @api.constrains('issue', 'businesunit', 'mom_id')
    def _check_status_bussinesunit(self):
        for record in self:
            data_mom = record.mom_id.name
            data_busines_example = []
            for i in record.businesunit:
                x = i.name
                # Memasukan x kedalam array data_busines_example
                data_busines_example.append(x)

            if 'NLM' in data_busines_example:
                # Skip the loop if 'NLM' already exists in businesunit
                continue

            if data_mom in data_busines_example:
                print("OK")
            else:
                print("Harus ada daya Business Unit yang bernilai MOM")
                raise ValidationError("Harus ada daya Scope yang bernilai Related")

            # Data dengan NLM
            nlm = 'NLM'
            print(data_busines_example)
            data_busines_example.append(nlm)
            array_tupple = tuple(data_busines_example)
            data_nlm = self.env['mom.request.bu'].search([('name', 'in', array_tupple)])
            
            # record_data = self.env['mom.request.line'].read_group(
            # [('mom_id', 'in', self.ids)],
            # ['mom_id'], ['mom_id'])
            # result = dict((data['mom_id'][0], data['mom_id_count']) for data in record_data)
            # for Mom in self:
            #     Mom.record_count = result.get(Mom.id, 0)

            if record.issue == 'urgent':
                # Update record.businessunit field with data_nlm
                record.write({
                    'businesunit': [(6, 0, data_nlm.ids)]
                })

            print(record.businesunit)
            print("Nice")
    # Batas Atas

    mom_id = fields.Many2one(
        'mom.request',
        string='MOM ID',
        readonly=True,
        required=False,
        default=lambda self: self.env.context.get('default_mom_id'),
        index=True, tracking=True, change_default=True, track_visibility='onchange')
    
    ajust = fields.Integer('Ajust', compute='get_ajust', store=True)
    
    @api.depends('ajust', 'ajustment')
    def get_ajust(self):
        for record in self:
            if not record.ajustment:
                record.ajust = 0
            else:
                x = len(record.ajustment)
                print(x)
                record.ajust = x
    
    

    


class mom_request(models.Model):
    _name = "mom.request"
    

    name = fields.Char("name")

    issue = fields.Char(
        string="Issue",
    )

    status = fields.Selection(
        [
            ("open", "Open"),
            ("on_progress", "On Progress"),
            ("close", "Close"),
        ],
        default="open",
    )

    issue = fields.Selection(
        [
            ("normal", "Normal"),
            ("medium", "Medium"),
            ("hotIssue", "Hot Issue"), 
        ],
        default="normal",
    )
    
    
    def _compute_record_count(self):
        record_data = self.env['mom.request.line'].read_group(
            [('mom_id', 'in', self.ids)],
            ['mom_id'], ['mom_id'])
        result = dict((data['mom_id'][0], data['mom_id_count']) for data in record_data)
        for Mom in self:
            Mom.record_count = result.get(Mom.id, 0)

    # record_count = fields.Integer(compute='_compute_record_count', string="Record Count")

    record_count = fields.Integer(string="Record Count", compute='_compute_record_count', store=True)
    record_id = fields.One2many(
        'mom.request.line', 'mom_id',
        string='Mom Request',
        required=False)