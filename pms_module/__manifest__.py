# -*- coding: utf-8 -*-
{
    'name': "Plan Management System (PMS) Module",

    'summary': """
        Form plan management system untuk crew kapal""",

    'description': """
        Form ini diisi untuk management job list
    """,

    'author': "Alwan",
    'website': "https://barokahperkasagroup.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'PMS',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        "security/pms_security.xml",
        'security/ir.model.access.csv',
        'views/jobCrew_view.xml',
        'views/jobCrewLine_view.xml',
        'views/vehicle_view.xml',
        'wizard/submit_job_crew_line.xml',
        'views/gas_maintenance_vehicle.xml',
        'views/gas_maintenance_vehicle_sequence.xml',
        'views/jobCrewEvidence_view.xml',
        'views/mom_request.xml',
        'report/pms.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
     #   'demo/demo.xml',
    #],
}
