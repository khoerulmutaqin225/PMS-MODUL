from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta
import logging
_logger = logging.getLogger(__name__)


class JobCrewLine(models.Model):
    _name = 'job.crew.line'

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

    @api.depends('status', 'last_main_date','current_value')
    def _compute_update_status_job(self):
        today = datetime.now().date()
        status = 'not_updated'
        last_value = 0
        for rec in self:
            if rec.current_value:
                if rec.last_main_date:
                    if rec.last_main_date < today:
                        status = 'not_updated'
                    elif rec.last_main_date >= today:
                        status = 'updated'
                        last_value = rec.current_value + rec.interval_value
            rec.current_date = today
            rec.status = status
            rec.last_value = last_value

    name = fields.Char(
        string='Name',
        required=False)

    vehicle_id = fields.Many2one(
        'vehicle.vehicle',
        related="group_job_crew_id.vehicle_id",
        string='Vehicle',
        readonly=True,)

    current_date = fields.Date(
        string='Current Date',
        #compute='_compute_update_status_job',
        store=True,
        readonly=True
    )

    last_main_date = fields.Date(
        string='Last Main Date',
        #compute='_compute_update_status_job',
        store=True,
        readonly=False
    )

    interval_time = fields.Integer(
        string='Interval Time',
        store=True,
        readonly=False
    )

    est_next_due_date = fields.Date(
        string='Est. Next Due Date',
        #compute='_compute_update_status_job',
        store=True,
        readonly=False
    )

    current_value = fields.Integer(
        string='Current Value',
        #compute='_compute_update_status_job',
        store=True,
        readonly=False
    )

    last_value = fields.Integer(
        string='Last Value',
        #compute='_compute_update_status_job',
        store=True,
        readonly=False
    )

    interval_value = fields.Integer(
        string='Interval Value',
        store=True,
        readonly=False
    )

    group_job_crew_id = fields.Many2one(
        'job.crew',
        string='Group Job Crew',
        ondelete="cascade",
        index=True,
        auto_join=True,
    )

    type_time = fields.Selection(
        string='Type Time',
        store=True,
        selection=[('running', 'Running'),
                   ('time_base', 'Day'),],
        readonly=False,
    )

    type_satuan = fields.Selection(
        string='Type Satuan',
        store=True,
        selection=[('hours', 'Hours'),
                   ('kilometer', 'Kilometer'), ],
        readonly=False,
    )

    image_1920 = fields.Binary("Image",store=True)

    keterangan = fields.Text(
        string="Work Description",
        required=False)

    status = fields.Selection(
        string='Status',
        store=True,
        compute='_compute_update_status_job',
        selection=[('not_updated', 'Not Updated'),
                   ('updated', 'Updated'), ],
        default='not_updated',
    )

    nilai_progress = fields.Integer(
        string='Nilai Progress (1-100)',
        store=True,
        compute='_change_value_progress',
        readonly=True
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

    active = fields.Boolean(
        string='Active',
        default=True,
        required=False)