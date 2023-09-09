from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta


class JobCrew(models.Model):
    _name = "job.crew"

    def refresh(self):
        today = datetime.now().date()
        for rec in self:
            if today > rec.last_update_rh_date:
                rec.update({'status_progress':'inaction','status':'not_updated'})
                if rec.line_jobs:
                    for line in rec.line_jobs:
                        if today > line.last_main_date:
                            line.update({'status_progress': 'inaction', 'status': 'not_updated'})



    def open_records(self):
        ctx = dict(self._context)
        ctx.update({'search_default_vehicle_id': self.id})
        action = self.env['ir.actions.act_window'].for_xml_id('pms_module', 'act_job_crew_2_record_all')
        return dict(action, context=ctx)
    
    def open_gas_records(self):
        ctx = dict(self._context)
        ctx.update({'search_gas_default_vehicle_id': self.id})
        action = self.env['ir.actions.act_window'].for_xml_id('pms_module', 'act_job_crew_3_record_all')
        return dict(action, context=ctx)

    @api.model
    def _process_status(self):
        today = fields.Date.today()
        current_hours = 0
        last_running_hours = 0
        status = 'not_updated'
        for rec in self:
            if rec.current_hours:
                if rec.last_update_rh_date:
                    if rec.last_update_rh_date < today:
                        status = 'not_updated'
                        current_hours = 0
                    elif rec.last_update_rh_date >= today:
                        status = 'updated'
                        last_running_hours = rec.current_hours
            rec.write({'status':status,'current_date':today,'last_running_hours':last_running_hours,'current_hours':current_hours})

    # @api.depends('status','last_update_rh_date','last_running_hours','current_hours')
    # def _compute_update_status_job(self):
    #     today = fields.Date.today()
    #     current_hours = 0
    #     last_running_hours = 0
    #     status = 'not_updated'
    #     for rec in self:
    #         if rec.current_hours:
    #             if rec.last_update_rh_date:
    #                 if rec.last_update_rh_date < today:
    #                     status = 'not_updated'
    #                     last_running_hours = rec.current_hours
    #                     rec.current_hours = 0
    #                 elif rec.last_update_rh_date >= today:
    #                     status = 'updated'
    #                     last_running_hours = rec.current_hours
    #         rec.current_date = today
    #         rec.status = status
    #         rec.last_running_hours = last_running_hours

    @api.depends('status_progress')
    def _change_value_progress(self):
        for rec in self:
            if rec.status_progress == 'completed':
                rec.update({'nilai_progress': 100})
            elif rec.status_progress == 'on_progress':
                nilai_progress = 0
                nilai_progress = rec.nilai_progress_temp
                rec.update({'nilai_progress': nilai_progress})
            else:
                rec.update({'nilai_progress': 0})
                rec.update({'nilai_progress_temp': 0})

    name = fields.Char(
        string='Name',
        required=False)

    vehicle_id = fields.Many2one(
        'vehicle.vehicle',
        string='Vehicle',
        readonly=True,
        required=False, default=lambda self: self.env.context.get('default_vehicle_id'),
        index=True, tracking=True, change_default=True)

    current_date = fields.Date(
        string='Current Date',
        store=True,
        readonly=True
    )

    last_update_rh_date = fields.Date(
        string='Last Update RH Date',
        store=True,
        required=True,
        readonly=False
    )

    current_hours = fields.Integer(
        string='Current Running Hours (h)',
        store=True,
        required=True,
        readonly=False
    )

    last_running_hours = fields.Integer(
        string='Last Running Hours (h)',
        store=True,
        readonly=True
    )

    line_jobs = fields.One2many(
        'job.crew.line', 'group_job_crew_id',
        string="Group Job Crew",
        required=False,
    )

    keterangan = fields.Text(
        string="Remark",
        required=False)

    color = fields.Integer(string='Color Index')

    status = fields.Selection(
        string='Status',
        compute='_compute_update_status_job',
        selection=[('not_updated', 'Not Updated'),
                   ('updated', 'Updated'), ],
        default='not_updated',
        store=True,
        readonly=True,
    )

    nilai_progress = fields.Integer(
        string='Nilai Progress (1-100)',
        store=True,
        compute='_change_value_progress',
        readonly=True
    )

    persentase = fields.Integer(
        string='Persentase (%)',
        store=True,
        readonly=False
    )
    

    nilai_progress_temp = fields.Integer(
        string='Nilai Progress (1-100)',
        readonly=False
    )

    status_progress = fields.Selection(
        string='Status Progress',
        selection=[('inaction', 'Inaction'),
                    ('on_progress', 'On Progress'),
                   ('completed', 'Completed'), ],
        default='inaction',
        store=True,
        required=True
    )
    # Batas tambahan atas
    bobot = fields.Integer(
        string='Bobot (%)',
        store=True,
        readonly=True,
    )
    # Batas tambahan bawah