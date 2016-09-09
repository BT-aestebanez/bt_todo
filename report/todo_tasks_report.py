# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from openerp.addons.bt_report_webkit import report_sxw_ext
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
import pytz
from openerp.tools.translate import _
import calendar

class todo_tasks_report(report_sxw_ext.rml_parse):
    
    TIMEZONE = 'Europe/Zurich'
    
    def __init__(self, cr, uid, name, context):
        print 'INIT........................................................................................'
        super(todo_tasks_report, self).__init__(cr, uid, name, context=context)

        #these are the variables we have available from mako view (${ctx}, ${time})
        self.localcontext.update({
            'time': time,
            'ctx': context,
            'get_translation': self.get_translation,
            'get_current_date': self.get_current_date,
         })
       
    def get_translation(self, src):
        return _(src)

    def get_current_date(self):
        now = datetime.now(pytz.timezone(self.TIMEZONE)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return now
    
report_sxw_ext.report_sxw_ext('report.todo.tasks.report',
                       'bt.todo.tasks', 
                       'bt_todo/report/todo_tasks_report.mako',
                       parser=todo_tasks_report)


