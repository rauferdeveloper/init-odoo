# -*- coding: utf-8 -*- 
from odoo import models, fields, api, exceptions 
import logging 
"""LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
LOG_FILE = 'todo_wizard_model.log'
logging.basicConfig(filename=LOG_FILE,
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode="a")"""
_logger = logging.getLogger(__name__) 

class TodoWizard(models.TransientModel): 
    _name = 'todo.wizard' 
    _description = 'Asistente de tareas por hacer' 
    task_ids = fields.Many2many('todo.task',string='Tasks') 
    new_deadline = fields.Date('Deadline to Set') 
    new_user_id = fields.Many2one('res.users',string='Responsible to Set')
    
    # Metodo para actualizar los nuevos datos que haya metido el usuario
    @api.multi 
    def do_mass_update(self): 
      self.ensure_one() 
      # Si no se han metido una nueva fecha o un nuevo responsable lanza una excepcion en la aplicacion
      if not (self.new_deadline or self.new_user_id):
        raise exceptions.ValidationError('No hay datos actualizados') 
      # Se guarda un mensaje en el registro
      _logger.debug('Actualizacion en el asistente de tareas por hacer %s', self.task_ids.ids) 
      vals = {} 
      if self.new_deadline: 
        vals['date_deadline'] = self.new_deadline 
      if self.new_user_id:
        vals['user_id'] = self.new_user_id.id
      # El asistente escribe valores en todas las tareas seleccionadas
      if vals: 
        self.task_ids.write(vals) 
      return True
    # Metodo para saber la cantidad de tareas pendientes/activas
    @api.multi 
    def do_count_tasks(self): 
        Task = self.env['todo.task'] 
        count = Task.search_count([('is_done', '=', False)]) 
        raise exceptions.Warning('La cantidad de tareas activas son: %d' %count)
    
    # Metodo para abrir de nuevo el mismo asistente
    @api.multi 
    def _reopen_form(self): 
        self.ensure_one() 
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,  # Este modelo             
            'res_id': self.id,  # El asistente que se ha grabado  
            'view_type': 'form', 
            'view_mode': 'form', 
            'target': 'new'}
    @api.multi 
    def do_populate_tasks(self): 
        self.ensure_one()         
        Task = self.env['todo.task']
        all_tasks = Task.search([('is_done', '=', False)])
        # Fill the wizard Task list with all tasks 
        self.task_ids = all_tasks 
        # reopen wizard form on same wizard record 
        return self._reopen_form()
    