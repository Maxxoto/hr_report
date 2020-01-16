# -*- coding: utf-8 -*-
{
    'name': "hr_report",
    'summary': "Excel Report for Payslips",
    'description': " Excel Report for Payslips",
    'author': "Satusoft",
    'website': "https://www.satusoft.com",
    'category': 'Report',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_payroll','hr_attendance','report_xlsx'],

    # always loaded
    'data': ['views/wizard_view.xml',],
    'license': "AGPL-3",
    'installable': True,
    'auto_install': False,
}