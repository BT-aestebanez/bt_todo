# b-*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010 brain-tec AG (http://www.brain-tec.ch)
# All Right Reserved
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp.osv import osv, fields

#===============================================================================
# bt_todo_tasks_wizard
#===============================================================================
class bt_todo_tasks_wizard(osv.TransientModel):
    _name = 'bt.todo.tasks.wizard'
    _inherit = 'bt.todo.tasks'

    # function to save task data into bt.todo.tasks
    def save_task(self, cr, uid, ids, context=None):
        todo_tasks_model = self.pool.get('bt.todo.tasks')
        wizard = self.browse(cr, uid, ids[0], context)

        data_list = {
             'name': wizard.name,
             'description': wizard.description,
             'priority': wizard.priority,
             'due_date': wizard.due_date,
             'due_time': wizard.due_time,
             'user_id': wizard.user_id.id,
             'private': wizard.private,
             'notify': wizard.notify,
             'category_id': wizard.category_id.id,
             'state': wizard.state
            }

        # We need to create res_id with a function to get "active_model" and "active_id"
        res_ids = self.get_active_model_record(context)
        for res_id in res_ids:
            data_list['res_id'] = res_id
            todo_tasks_model.create(cr, uid, data_list, context)

        return {}
    
    # Gets the current model and the active record all encoded in a string
    def get_active_model_record(self, context):
        data_wiz = {}

        if not (context.get('active_ids')):
            raise osv.except_osv(_('Not possible to save the todo task'),
                                 _('No records selected to create the task'))

        if not context.get('active_model'):
            raise osv.except_osv(_('Not possible to save the todo task'),
                                 _('The model selected is not valid'))
            
        res_values = []
        for active_id in context.get('active_ids'):
            res_id_value = context.get('active_model') + ',' + str(active_id)
            res_values.append(res_id_value)
 
        return res_values

bt_todo_tasks_wizard()

