from odoo import models, fields, _,api
from datetime import date, datetime
# from odoo.exceptions import ValidationError
import xlrd
import base64
import os


from odoo import models, fields, api, _
import base64
import requests
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta


class mom_request_bu(models.Model):
    _name = "mom.request.bu"

    name = fields.Char(
        string='Name',
        required=False)

class mom_request_divisi(models.Model):
    _name = "mom.request.divisi"

    name = fields.Char(
        string='Name',
        required=False)


class mom_request_line(models.Model):
    _name = "mom.request.line"
    
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
        required=False)

    plan = fields.Char(
        string='Plan',
        required=False)

    status = fields.Selection(
        [
            ("open", "Open"),
            ("on_progress", "On Progress"),
            ("close", "Close"),
        ],
        default="open",
    )

    divisi = fields.Many2many(
        'mom.request.divisi',
        'mom_request_divisi_rel',
        'mom_request_divisi_id',
        'brand_id',
        string='Divisi Ids')

    businesunit = fields.Many2many(
        'mom.request.bu',
        'mom_request_bu_rel',
        'mom_request_bu_id',
        'brand_id',
        default=lambda self: self.env.context.get('default_x_id'),
        string='Businesunit Ids')
    
    
    @api.constrains('issue')
    def _check_businesunit(self):
        for record in self:
            if record.issue == 'hotIssue':
                record_nlm ={
                    'name' : record.name,
                    'plan' : record.plan,
                    'status' : record.status,
                    'divisi' : record.divisi,
                    'businesunit' : record.businesunit,
                    'pic' : record.pic,
                    'opendate' : record.opendate,
                    'deadline' : record.deadline,
                    'closedate' : record.closedate,
                    'keterangan' : record.keterangan,
                    'issue' : record.issue,
                    'nilai' : record.nilai,
                    'nilai' : record.nilai,
                    'mom_id' : 'NLM',
                }
                self.env['mom.request.line'].sudo().create(record_nlm)
                
    pic = fields.Char(
        string='Pic',
        required=False)

    opendate = fields.Date('Open Date')
    deadline = fields.Date('Deadline')
    closedate = fields.Date('Close Date')
    
    keterangan = fields.Char('Keterangan')
    # issue = fields.Char('issue')
    issue = fields.Selection(
        [
            ("normal", "Normal"),
            ("medium", "Medium"),
            ("hotIssue", "Hot Issue"), 
        ],
        default="normal",
    )
    
    nilai = fields.Char('nilai')
    
    
    mom_id = fields.Many2one(
        'mom.request',
        string='Mom',
        readonly=True,
        required=False,
        default=lambda self: self.env.context.get('default_mom_id'),
        index=True, tracking=True, change_default=True)


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

    record_count = fields.Integer(compute='_compute_record_count', string="Record Count")

    record_id = fields.One2many(
        'mom.request.line', 'mom_id',
        string='Mom Request',
        required=False)
    
    def func_to_approve(self):
        for line in self:
            if line.status == 'open':
                if line.name == 'New':
                    seq = self.env['ir.sequence'].next_by_code('mom.request') or '/'
                    line.name = seq
                line.status = 'on_progress'
    



    