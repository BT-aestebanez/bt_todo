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

from osv import osv, fields
from tools.translate import _

import time

#===============================================================================
# bt_todo_tasks
#===============================================================================
class bt_todo_tasks(osv.Model):
    _name = 'bt.todo.tasks'
    _description = 'TODO tasks'

    AVAILABLE_PRIORITIES = [
        ('5', _('Very Low')),
        ('4', _('Low')),
        ('3', _('Medium')),
        ('2', _('High')),
        ('1', _('Very High')),
    ]

    # search for Models all models
    def _search_selection(self, cr, uid, context=None):
        '''Gets links value for reference field'''
        
        obj = self.pool.get('ir.model')
        ids = obj.search(cr, uid, [])
        res = obj.read(cr, uid, ids, ['model', 'name'], context)
        
        return [(r['model'], r['name']) for r in res]


    _columns = {
        'name': fields.char(_('Title'), size=128, required=True),
        'user_id': fields.many2one('res.users', string=_('User'), required=True),
        'priority': fields.selection(AVAILABLE_PRIORITIES, _('Priority'), required=True),
        'due_date': fields.date(_('Due Date'), required=True),
        'due_time': fields.float(_('Time Required'), required=False),
        'res_id': fields.reference(_('Reference'), _search_selection, 128),
        'category_id': fields.many2one('bt.todo.categories', string=_('Category'), required=False),
        'private': fields.boolean(_('Private'),
                                  help=_('Check this field to show this TODO task only to the '
                                         'specified user')),
        'notify': fields.boolean(_('Notify'),
                                 help=_('Check this field to send an email to the specified user '
                                        'when the due date is near')),
        'state': fields.selection([('open', _('Open')),
                                   ('hold', _('Hold')),
                                   ('done', _('Done'))],
                                  string=_('State'), required=True, readonly=True),
        'description': fields.text(_('Description'), required=False),
        'create_uid': fields.many2one('res.users', _('Created by'), readonly=True),
    }

    _defaults = {
        'user_id': lambda self, cr, uid, context: uid,
        'priority': lambda self, cr, uid, context: '3',
        'due_date': lambda self, cr, uid, context: time.strftime('%Y-%m-%d'),
        'private': False,
        'notify': False,
        'state': 'open',
    }

    def action_hold(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'hold'}, context)

    def action_done(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'done'}, context)

    def action_reset(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'open'}, context)


bt_todo_tasks()

#===============================================================================
# todo_categories
#===============================================================================
class bt_todo_categories(osv.Model):
    _name = 'bt.todo.categories'
    _description = 'TODO Categories'

    def name_get(self, cr, uid, ids, context={}):
        '''
        Return the categories' display name, including their direct parent by default.

        :param dict context: the "todo_category_display" key can be used to select the short version
                             of the category name (without the direct parent), when set to "short". 
                             The default is the long version.'''

        if context.get('partner_category_display') == 'short':
            return super(bt_todo_categories, self).name_get(cr, uid, ids, context)
        
        res = []
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context=context)
        for record in reads:
            name = record['name']
            
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
                
            res.append((record['id'], name))
            
        return res

    def name_search(self, cr, uid, name, args={}, operator='ilike', context={}, limit=100):
        if name:
            # Be sure name_search is symmetric to name_get
            name = name.split(' / ')[-1]
            ids = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        
        return self.name_get(cr, uid, ids, context)

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _columns = {
        'name': fields.char(_('Category Name'), required=True, select=True, size=64, translate=True),
        'parent_id': fields.many2one('bt.todo.categories', _('Parent Category'), select=True, ondelete='cascade'),
        'complete_name': fields.function(_name_get_fnc, type='char', string=_('Full Name')),
        'child_ids': fields.one2many('bt.todo.categories', 'parent_id', _('Child Categories')),
        'active' : fields.boolean(_('Active'), help='Uncheck this field to hide the category without removing it'),
        'parent_left' : fields.integer(_('Left parent'), select=False),
        'parent_right' : fields.integer(_('Right parent'), select=False),
        'task_ids': fields.one2many('bt.todo.tasks', 'category_id', string=_('TODO Tasks')),
    }
    
    _constraints = [
        (osv.osv._check_recursion, 'You cannot create recursive categories', ['parent_id'])
    ]
    
    _defaults = {
        'active' : True,
    }
    
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'

bt_todo_categories()
