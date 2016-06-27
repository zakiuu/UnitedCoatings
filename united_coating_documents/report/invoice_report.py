# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time

from openerp.report import report_sxw
from openerp.osv import osv
from openerp.addons.smile_amount_in_letters.tools import format_amount_fr


class Invoice(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(Invoice, self).__init__(cr, uid, name, context = context)
        self.localcontext.update({'amount_in_letters': self.amount_in_letters})

    def amount_in_letters(self, amount):
        currency_symbol = u'DZD'
        currency_in_letters = u'Dinars Algerien'
        return format_amount_fr(amount, currency_symbol, currency_in_letters, in_letters=True)


class report_invoice(osv.AbstractModel):

    _name = 'report.united_coating_documents.report_unitedcoating_invoice_document'
    _inherit = 'report.abstract_report'
    _template = 'united_coating_documents.report_unitedcoating_invoice_document'
    _wrapped_report_class = Invoice
