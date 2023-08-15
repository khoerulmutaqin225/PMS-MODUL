# -*- coding: utf-8 -*-

{
    'name': 'Shipping Company Management V2',
    'version': '13.0.1.0.0',
    'summary': """Manages Shipping Management, Vessel, Crew Documents, etc.""",
    'description': """Manages Shipping Management, Vessel, Crew Documents, etc .""",
    'category': 'Enterprice',
    'author': 'Arif Munandar',
    'company': 'Barokah Perkasa Group',
    'maintainer': 'Arif Munandar',
    'website': "https://barokahperkasagroup.com",
    'depends': ['base', 'hr'],
    'data': [
        'security/operation_security.xml',
        'security/ir.model.access.csv',
        'views/shipping_vessel_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
