##############################################################################
# Copyright (c) 2022 lumitec GmbH (https://www.lumitec.solutions)
# All Right Reserved
#
# See LICENSE file for full licensing details.
##############################################################################
{
    'name': 'Expense Enhancement',
    'summary': 'Expense Enhancement',
    'author': "lumitec GmbH",
    'website': "https://www.lumitec.solutions",
    'category': 'Human Resources/Expenses',
    'version': '16.0.1.0.0',
    'license': 'OPL-1',
    'images': ['static/description/thumbnail.png'],
    'depends': [
        'base',
        'hr_expense',
    ],
    'data': [
        "report/expense_report.xml"
    ],

    'installable': True,
    'auto_install': False,
    'application': False
}
