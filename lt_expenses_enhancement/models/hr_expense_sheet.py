##############################################################################
# Copyright (c) 2022 lumitec GmbH (https://www.lumitec.solutions)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
import base64
import io
import PyPDF2
from PyPDF2 import PdfFileReader
from reportlab.pdfgen import canvas
from odoo import models


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    def print_complete_expense_report(self):
        """An attachment with the expense report along with all attachments is created"""
        pdf, _ = self.env.ref('hr_expense.action_report_hr_expense_sheet')._render_qweb_pdf(self.id)
        pdf_template = self.env['ir.attachment'].search([('name', '=', self.name)])
        if pdf_template:
            pdf_template.unlink()
            pdf, _ = self.env.ref('hr_expense.action_report_hr_expense_sheet')._render_qweb_pdf(self.id)
            pdf_report = self.env['ir.attachment'].search([('name', '=', self.name)])
        else:
            pdf_report = pdf_template
        pdfwriter = PyPDF2.PdfFileWriter()
        stored_attach = pdf_report._full_path(pdf_report.store_fname)
        pdf2_file = open(stored_attach, 'rb')
        pdfreader2 = PyPDF2.PdfFileReader(pdf2_file)
        for page_num in range(pdfreader2.numPages):
            pageobj = pdfreader2.getPage(page_num)
            pdfwriter.addPage(pageobj)
        results = self.env['ir.attachment'].search([('res_model', '=', 'hr.expense'), ('res_id', 'in', self.expense_line_ids.ids)])
        for result in results:
            if result.mimetype in ['image/jpeg', 'image/jpg', 'image/png']:
                packet = io.BytesIO()
                can = canvas.Canvas(packet)
                path = result._full_path(result.store_fname)
                can.drawImage(path, 50, 50, width=500, height=500,
                              preserveAspectRatio=True, mask='auto')
                can.showPage()
                can.save()
                packet.seek(0)
                new_pdf = PdfFileReader(packet)
                pageobj1 = new_pdf.getPage(0)
                pdfwriter.addPage(pageobj1)
            else:
                attach_id = result._full_path(result.store_fname)
                pdf_file = open(attach_id, 'rb')
                pdfreader = PyPDF2.PdfFileReader(pdf_file)
                for page_num in range(pdfreader.numPages):
                    pageobj = pdfreader.getPage(page_num)
                    pdfwriter.addPage(pageobj)
        merged_pdf = io.BytesIO()
        pdfwriter.write(merged_pdf)
        merged_file = self.env['ir.attachment'].sudo().create({
            'name': self.name + '.pdf',
            'datas': base64.b64encode(merged_pdf.getvalue()).decode(),
            'type': 'binary',
            'res_model': self._name,
            'res_id': self.id
        })
        action = self.env.ref('base.action_attachment').sudo().read()[0]
        action['views'] = [(self.env.ref('base.view_attachment_form').id, 'form')]
        action['res_id'] = merged_file.id
        return action
