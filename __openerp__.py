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
{
    "name": "Braint Tec Todo module",
    "version": "1.0",
    "author": "brain-tec AG",
    "description": """This module allows you to manage TODO list:
    - Task categories.
    - Task management.""",
    "category": "Custom/TodoList",
    "website": "http://www.brain-tec.ch",
    "depends": ["base", "bt_report_webkit", "account"],
    "data": [
        "data/internal_header_logo.xml",
        'view/bt_todo_view.xml',
        'wizard/bt_todo_view.xml',
        'report/bt_todo_report.xml',
        'security/ir.model.access.csv',
    ],
    "active": False,
    "installable": True,
}
