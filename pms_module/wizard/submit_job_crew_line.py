from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta
import logging
_logger = logging.getLogger(__name__)


class SubmitJobCrewLine(models.Model):
    _name = "submit.job.crew.line.wizard"
    _description = "Submit Wizard"

    name = fields.Char(
        string='Name',
        required=False)

    current_date = fields.Date(
        string='Current Date',
        readonly=True
    )

    last_main_date = fields.Date(
        string='Last Main Date',
        readonly=True
    )

    est_next_due_date = fields.Date(
        string='Est. Next Due Date',
        readonly=True
    )

    interval_time = fields.Integer(
        string='Interval Time',
        readonly=True
    )

    current_value = fields.Integer(
        string='Current Value',
        readonly=False
    )

    last_value = fields.Integer(
        string='Last Value',
        readonly=True
    )

    interval_value = fields.Integer(
        string='Interval Value',
        readonly=True
    )

    type_time = fields.Selection(
        string='Type Time',
        store=True,
        selection=[('running', 'Running'),
                   ('time_base', 'Day'), ],
        readonly=True,
    )

    type_satuan = fields.Selection(
        string='Type Satuan',
        store=True,
        selection=[('hours', 'Hours'),
                   ('kilometer', 'Kilometer'), ],
        readonly=True,
    )

    image_1920 = fields.Binary("Image")

    keterangan = fields.Text(
        string="Work Description",
        required=False)

    status = fields.Selection(
        string='Status',
        store=True,
        selection=[('not_updated', 'Not Updated'),
                   ('updated', 'Updated'), ],
        readonly=True,
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

    @api.model
    def default_get(self, fields):
        res = super(SubmitJobCrewLine, self).default_get(fields)
        active_id = self._context.get('active_id')
        brw_id = self.env['job.crew.line'].browse(int(active_id))

        if active_id:
            res['name'] = brw_id.name
            res['last_main_date'] = brw_id.last_main_date
            res['est_next_due_date'] = brw_id.est_next_due_date
            res['current_date'] = brw_id.current_date
            res['interval_time'] = brw_id.interval_time
            res['current_value'] = brw_id.current_value
            res['last_value'] = brw_id.last_value
            res['interval_value'] = brw_id.interval_value
            res['type_time'] = brw_id.type_time
            res['type_satuan'] = brw_id.type_satuan
            res['status'] = brw_id.status
        return res

    def submit_job_crew_line(self):
        active_id = self._context.get('active_id')
        brw_id = self.env['job.crew.line'].browse(int(active_id))
        today = datetime.now().date()

        new_last_value = 0
        new_last_main_date = False
        new_est_next_due_date = False
        for rec in self:
            status = 'updated'
            if rec.interval_time:
                new_est_next_due_date = today + timedelta(days=rec.interval_time)
                new_last_main_date = today
            if rec.current_value:
                new_last_value = rec.current_value + rec.interval_value

        brw_id.write({'status': status,'status_progress': self.status_progress,'keterangan': self.keterangan,'current_value': self.current_value,'last_value': new_last_value,'last_main_date':new_last_main_date,'est_next_due_date':new_est_next_due_date,'image_1920': self.image_1920})
