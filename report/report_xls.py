# -*- coding: utf-8 -*-


import datetime

from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx

class PayrollReport(ReportXlsx):
    

    
    # def get_payslip(self,data):
    #     payslip = []
        
    #     date_from = data['form']['date_from']
    #     date_to = data['form']['date_to']                 

    #     payslip = self.env['hr.payslip'].search([
    #             ('date_from', '=' , date_from),
    #             ('date_to', '=' , date_to),
    #             ])
    # def get_worked_days(self,id) :


    
   
    def get_workday(self,id) :
        res = self.env['hr.payslip.worked_days'].search([
            ('code', '=', 'WORKDAY'),
            ('payslip_id', '=' , id),
            ])
        return res.number_of_days

    def get_lateness(self,id) :
        res = self.env['hr.payslip.worked_days'].search([
            ('code', '=', 'LATENESS'),
            ('payslip_id', '=' , id),
            ])
        return res.number_of_days
    
    def get_halfday(self,id) : 
        res = self.env['hr.payslip.worked_days'].search([
            ('code', '=', 'HALFDAY'),
            ('payslip_id', '=' , id),
            ])
        return res.number_of_days

    def get_attendance(self,id) :
        res = self.env['hr.payslip.worked_days'].search([
            ('code', '=', 'ATTN'),
            ('payslip_id', '=' , id),
            ])
        return res.number_of_days

    def get_gajiPokok(self,id) :
        res = self.env['hr.payslip.line'].search([
            ('code', '=', 'GPOKOK'),
            ('slip_id', '=' , id),
            ])
        return res.amount

    def get_gajiLembur(self,id) :
        res = self.env['hr.payslip.line'].search([
            ('code', '=', 'GLEMBUR'),
            ('slip_id', '=' , id),
            ])
        return res.amount
    
    def get_gajiBonus10(self,id) :
        res = self.env['hr.payslip.line'].search([
            ('code', '=', 'GBNS10'),
            ('slip_id', '=' , id),
            ])
        return res.amount

    def get_uangMakan(self,id) :
        res = self.env['hr.payslip.line'].search([
            ('code', '=', 'GUM'),
            ('slip_id', '=' , id),
            ])
        return res.amount

    def get_bonusManual(self,id) :
        res = self.env['hr.payslip.line'].search([
            ('code', '=', 'GBNSM'),
            ('slip_id', '=' , id),
            ])
        return res.amount
    
    def get_potonganAbsen(self,id) :
        res = self.env['hr.payslip.line'].search([
            ('code', '=', 'PABSEN'),
            ('slip_id', '=' , id),
            ])
        return res.amount

    def get_potonganManual(self,id) :
        res = self.env['hr.payslip.line'].search([
            ('code', '=', 'PMANUAL'),
            ('slip_id', '=' , id),
            ])
        return res.amount

    def get_totalGaji(self,id) :
        gPokok = self.get_gajiPokok(id)
        gLembur = self.get_gajiLembur(id)
        gBNS10 = self.get_gajiBonus10(id)
        gUM = self.get_uangMakan(id)
        gBNSM = self.get_bonusManual(id)
        pAbsen = self.get_potonganAbsen(id)
        pMan = self.get_potonganManual(id)

        res = (gPokok+gLembur+gBNS10+gUM+gBNSM) + (pAbsen+pMan)

        return res

    


    def generate_xlsx_report(self, workbook, data, lines):  
            date_from = data['form']['date_from']
            date_to = data['form']['date_to']                 

            sheet = workbook.add_worksheet()
            bold = workbook.add_format({'bold': True})

            merge_format = workbook.add_format({
                'bold' : True,
                'align': 'center',
                'valign': 'vcenter',
                })
            merge_format_wrap = workbook.add_format({
                'text_wrap' : True,
                'bold' : True,
                'align': 'center',
                'valign': 'vcenter',
                })

            currency_format = workbook.add_format({'num_format': '"Rp. "#,0'})

            if data.get('form', False) and data['form'].get('date_from', False):                                                   
                t = ' - '                

                report_date = date_from + t + date_to

                sheet.merge_range('C1:E1',report_date,merge_format)
                # sheet.write('C1',date_from)
                # sheet.write('D1'," - ")
                # sheet.write('E1',date_to)

            sheet.merge_range('A2:A3','No',merge_format)
            sheet.merge_range('B2:B3','Nama',merge_format)
            sheet.merge_range('C2:C3','Hari Kerja',merge_format)
            sheet.merge_range('D2:D3','Jml Masuk',merge_format)
            sheet.merge_range('E2:E3','Jml 1/2 Hari',merge_format)            
            sheet.merge_range('F2:F3','Jml Telat',merge_format)            
            sheet.merge_range('G2:G3','Gaji Pokok',merge_format)
            sheet.merge_range('H2:H3','Lembur',merge_format)
            sheet.merge_range('I2:I3','10%',merge_format)
            sheet.merge_range('J2:J3','Makan',merge_format)
            sheet.merge_range('K2:K3','Bonus Manual',merge_format_wrap)
            sheet.merge_range('L2:L3','Potongan Absen',merge_format_wrap)
            sheet.merge_range('M2:M3','Potongan Manual',merge_format_wrap)
            sheet.merge_range('N2:N3','Total Gaji',merge_format)
            sheet.merge_range('O2:O3','TT',merge_format)
            sheet.merge_range('P2:P3','Keterangan',merge_format)
            
            sheet.merge_range('A1:B1','Periode :', merge_format)
            
            # sheet.write_formula('C1','=_xlfn.CONCAT(date_from)')
            count_rows = self.env['hr.payslip'].search_count([
                ('date_from', '=' , date_from),
                ('date_to', '=' , date_to),
                ])

            sheet.write('F1','Jml Data :')    
            sheet.write('G1',count_rows)

            
            # lines = self.get_lines(data)

            lines = self.env['hr.payslip'].search([
                ('date_from', '=' , date_from),
                ('date_to', '=' , date_to),
                ])
            

            # count = len(lines)
            # sheet.write('I1',count)
            no=1
            i=0
            # for i in range(0,count_rows):                            
            for line in lines :   
                sheet.write(i+3,0,no)                                                               
                sheet.write(i+3,1,line.employee_id.name)  
                sheet.write(i+3,2,self.get_workday(line.id)) 
                sheet.write(i+3,3,self.get_attendance(line.id))
                sheet.write(i+3,4,self.get_halfday(line.id))
                sheet.write(i+3,5,self.get_lateness(line.id))                  
                sheet.write(i+3,6,self.get_gajiPokok(line.id),currency_format) 
                sheet.write(i+3,7,self.get_gajiLembur(line.id),currency_format) 
                sheet.write(i+3,8,self.get_gajiBonus10(line.id),currency_format) 
                sheet.write(i+3,9,self.get_uangMakan(line.id),currency_format) 
                sheet.write(i+3,10,self.get_bonusManual(line.id),currency_format) 
                sheet.write(i+3,11,self.get_potonganAbsen(line.id),currency_format) 
                sheet.write(i+3,12,self.get_potonganManual(line.id),currency_format) 
                sheet.write(i+3,13,self.get_totalGaji(line.id),currency_format) 
                i+=1
                no+=1

                    

                    # break
                # Todo : i=3 karena mulai dari row 4 , dan menggunakan sheet.write(row,column)
                                                 
                    # workday_ = self.get_workday_id(line.id)
                    # sheet.write(i+3,2,line.worked_days_line_ids[line.id].number_of_days)
                    # break
                    # sheet.write(i+3,2,workday_id)
                    # sheet.write(i+3,3,line.worked_days_line_ids.LATENESS.number_of_days)
                    # sheet.write(i+3,4,line.worked_days_line_ids.number_of_days)


PayrollReport('report.hr_report.payslip_report_xlsx','hr.payslip')