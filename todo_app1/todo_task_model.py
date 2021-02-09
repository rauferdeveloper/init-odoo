# -*- coding: utf-8 -*- 
from odoo import models, fields, api
class TodoTask(models.Model): 
    _name = 'todo.task' 
    _description = 'To-do Task'
    name = fields.Char('Description', required=True) 
    is_done = fields.Boolean('Done?') 
    active = fields.Boolean('Active?', default=True)
    # Esta funcion cambia el valor del campo is_done (campo que se usa para saber si una tarea esta realizada o no) de todas las tareas a valor False (o tarea no realizada) 
    @api.multi 
    def do_toggle_done(self): 
        for task in self: 
            task.is_done = False
        return True
    # Esta funcion busca todas las tareas donde el valor sea True (o tarea realizada) en el campo is_done y cambia el valor del campo active a False que eso conlleva a que esa tarea/tareas no se muestren en el navegador 
    @api.multi 
    def do_clear_done(self): 
        dones = self.search([('is_done', '=', True)]) 
        dones.write({'active': False}) 
        return True
    @api.multi
    def do_delete_all(self):
        dones = self.search([('is_done','=',True)]).unlink()
        return True
