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
        string='Businesunit Ids',track_visibility='onchange')
    
    
                
    pic = fields.Char(
        string='Pic',
        required=False,track_visibility='onchange')

    opendate = fields.Date('Open Date',track_visibility='onchange')
    deadline = fields.Date('Deadline',track_visibility='onchange')
    closedate = fields.Date('Close Date',track_visibility='onchange')
    
    keterangan = fields.Text('Keterangan',track_visibility='onchange')
    # issue = fields.Char('issue')
    issue = fields.Selection(
        [
            ("normal", "Normal"),
            ("medium", "Medium"),
            ("hotIssue", "Hot Issue"), 
        ],
        default="normal",
        track_visibility='onchange'
    )
    
    nilai = fields.Char('Nilai',track_visibility='onchange')
    
    
    mom_id = fields.Many2one(
        'mom.request',
        string='Mom',
        readonly=True,
        required=False,
        default=lambda self: self.env.context.get('default_mom_id'),
        index=True, tracking=True, change_default=True,track_visibility='onchange')


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