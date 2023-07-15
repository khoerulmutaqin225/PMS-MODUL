# -*- coding: utf-8 -*-
import json
import requests
from odoo.tests import Form
import werkzeug.wrappers

from datetime import datetime
from datetime import timedelta
from odoo import http, _, exceptions
from odoo.http import content_disposition, request
from operator import itemgetter,methodcaller


class PmsModule(http.Controller):

    @http.route('/api/get_info_vehicle', auth='user', type="json", method='GET')
    def get_info_vehicle(self, **kw):
        data = request.env['vehicle.vehicle'].sudo().search([('vehicle_id.id', '=', kw['vehicle_id'])])
        dict = {}
        for j in data:
            dict = {'id': j.id, 'name': j.name, 'type': j.type,
                        'persentase': j.persentase}
        return dict
    @http.route('/api/get_all_job_crew', auth='user', type="json", method='GET')
    def get_all_job_crew(self, **kw):
        job = request.env['job.crew'].sudo().search([('vehicle_id.id', '=', kw['vehicle_id'])])
        dict_job = {}
        data_job = []
        for j in job:
            dict_job = {'id': j.id, 'name': j.name, 'vehicle_id': j.vehicle_id.id,
                               'vehicle_id_name': j.vehicle_id.name,
                               'last_update_rh_date': j.last_update_rh_date, 'current_hours': j.current_hours,
                               'nilai_progress': j.nilai_progress,'persentase': j.persentase,'status_progress': j.status_progress,'status': j.status}
            data_job.append(dict_job)
        return data_job

    @http.route(['/api/one_job_crew'],  auth='user', type="json", method='GET')
    def one_job_crew(self, **kw):
        job = request.env['job.crew'].sudo().search([('id', '=', kw['id'])])
        dict_job = {}
        data_job = []
        for j in job:
            dict_j_line = {}
            data_j_line = []
            for line in j.line_jobs:
                dict_j_line = {'id': line.id, 'name': line.name, 'last_main_date': line.last_main_date,
                               'est_next_due_date': line.est_next_due_date, 'interval_time': line.interval_time,
                               'current_value': line.current_value,
                               'last_value': line.last_value, 'interval_value': line.interval_value,
                               'type_time': line.type_time,
                               'type_satuan': line.type_satuan,
                               'keterangan': line.keterangan, 'nilai_progress': line.nilai_progress,'status_progress': line.status_progress,'status': line.status,}
                data_j_line.append(dict_j_line)
            dict_job = {'id': j.id, 'name': j.name, 'vehicle_id': j.vehicle_id.id,
                               'vehicle_id_name': j.vehicle_id.name,
                               'last_update_rh_date': j.last_update_rh_date, 'current_hours': j.current_hours,
                               'last_running_hours': j.last_running_hours,
                               'nilai_progress': j.nilai_progress,'persentase': j.persentase,'status_progress': j.status_progress,'status': j.status,'line_jobs': data_j_line}
            # data_work_orders.append(dict_work_orders)
        return dict_job

    @http.route(['/api/get_all_job_crew_line'], type='json', auth='user', method='GET', csrf=False, website=False)
    def get_all_job_crew_line(self, **kw):
        job = request.env['job.crew.line'].sudo().search([('active','=',True)])
        dict_j_line = {}
        data_j_line = []
        for line in job:
            dict_j_line = {'id': line.id, 'name': line.name, 'last_main_date': line.last_main_date,
                           'est_next_due_date': line.est_next_due_date, 'interval_time': line.interval_time,
                           'current_value': line.current_value,
                           'last_value': line.last_value, 'interval_value': line.interval_value,
                           'type_time': line.type_time,
                           'type_satuan': line.type_satuan,'nilai_progress': line.nilai_progress,'status_progress': line.status_progress,'status': line.status, 'active': line.active,}
            data_j_line.append(dict_j_line)
        return data_j_line

    @http.route(['/api/get_all_job_crew_line_byId'], type='json', auth='user', method='GET', csrf=False, website=False)
    def get_all_job_crew_line_byId(self, **kw):
        job = request.env['job.crew.line'].sudo().search([('vehicle_id.id', '=', kw['vehicle_id']),('active','=',True)])
        dict_j_line = {}
        data_j_line = []
        for line in job:
            dict_j_line = {'id': line.id, 'name': line.name, 'last_main_date': line.last_main_date,
                           'est_next_due_date': line.est_next_due_date, 'interval_time': line.interval_time,
                           'current_value': line.current_value,
                           'last_value': line.last_value, 'interval_value': line.interval_value,
                           'type_time': line.type_time,
                           'type_satuan': line.type_satuan, 'keterangan': line.keterangan,
                           'nilai_progress': line.nilai_progress,'status_progress': line.status_progress,'status': line.status,'active': line.active, }
            data_j_line.append(dict_j_line)
        return data_j_line

    @http.route(['/api/one_job_line_crew'], type='json', auth='user', method='GET', csrf=False, website=False)
    def one_job_line_crew(self, **kw):
        job = request.env['job.crew.line'].sudo().search([('id', '=', kw['id'])])
        dict_job = {}
        data_job = []
        for line in job:
            dict_j_line = {'id': line.id, 'name': line.name, 'last_main_date': line.last_main_date,
                           'est_next_due_date': line.est_next_due_date, 'interval_time': line.interval_time,
                           'current_value': line.current_value,
                           'last_value': line.last_value, 'interval_value': line.interval_value,
                           'type_time': line.type_time,
                           'type_satuan': line.type_satuan,
                           'image_1920': line.image_1920,
                           'keterangan': line.keterangan, 'nilai_progress': line.nilai_progress,'status_progress': line.status_progress,'status': line.status, 'active': line.active,}
            # data_work_orders.append(dict_work_orders)
        return dict_j_line


    @http.route(['/api/edit_job'], type='json', auth='user', method='POST', csrf=False, website=False)
    def edit_job(self, **kw):
        job = request.env['job.crew'].sudo().search([('id', '=', kw['id'])])
        job.write({'last_update_rh_date': kw['last_update_rh_date'],
                   'nilai_progress_temp': kw['nilai_progress'],
                   'status_progress': kw['status_progress'],
                    'current_hours': kw['current_hours'],
                   'persentase': kw['persentase'],
                    })
        return kw

    @http.route(['/api/edit_line_job'], type='json', auth='user', method='POST', csrf=False, website=False)
    def edit_line_job(self, **kw):
        job = request.env['job.crew.line'].sudo().search([('id', '=', kw['id'])])
        today = datetime.now().date()

        status = ''
        current = 0
        new_last_value = 0
        new_last_main_date = False
        new_est_next_due_date = False
        for rec in job:
            if rec.interval_time:
                new_est_next_due_date = today + timedelta(days=rec.interval_time)
                new_last_main_date = today
            if rec.current_value:
                current = int(kw['current_value'])
                new_last_value = current + rec.interval_value

        job.write({'keterangan': kw['keterangan'],
                   'image_1920': kw['image_1920'],
                   'current_value': current,
                   'last_value': new_last_value,
                   'last_main_date': new_last_main_date,
                   'est_next_due_date': new_est_next_due_date,
                   'nilai_progress_temp': kw['nilai_progress'],
                   'status_progress': kw['status_progress'],
                   'status': 'updated',
                   })
        return kw


