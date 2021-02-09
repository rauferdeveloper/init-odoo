# -*- coding: utf-8 -*- 
from odoo import api, models
from odoo.exceptions import ValidationError
from datetime import datetime
"""import logging
_logger = logging.getLogger(__name__)"""
#from odoo.exceptions import ValidationError 

class TodoTask(models.Model): 
    _inherit = 'todo.task' 
    
    @api.model 
    def website_form_input_filter(self, request, values):
        #raise ValidationError(values)
        """if 'date_deadline' in values:
            values['date_deadline'] = datetime.strptime(date_deadline, '%dd/%mm/%Y')"""

        if 'name' in values: 
            values['name'] = values['name'].strip()
            if len(values['name']) < 7: 
                raise ValidationError('El nombre de la tarea debe de contener al menos 7 caracteres')
        return values 