# -*- coding: utf-8 -*-
from datetime import datetime 

from odoo import models, fields, api

class hr_report(models.TransientModel):
    _name = "wizard.payroll"
    _description = "Export Payslip"

    # employee_payslip = fields.Many2one('hr.payslip', string='Employee Payslip')
    date_from = fields.Date("Start date",default=datetime.today().replace(day=1))
    date_to = fields.Date("End date",default=datetime.today())

    # @api.multi
    # def export_xls(self):
    #     context = self._context
    #     data = {}         
    #     data['form'] = self.read()[0]        
    #     return self.env['report'].get_action(self,'hr_report.payslip_report_xlsx',data=data) #Error data tidak mau masuk
        

    @api.multi
    def export_xls(self):
        context = self._context
        data = {}         
        data['form'] = self.read()[0]        
        if context.get('export_xls'):
            return {'type': 'ir.actions.report.xml',
                    'report_name': 'hr_report.payslip_report_xlsx',
                    'datas': data,
                    'name': 'Payslip Report'
                    }
