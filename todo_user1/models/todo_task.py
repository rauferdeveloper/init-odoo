# -*- coding: utf-8 -*- 
from odoo import models, fields, api 
from odoo.exceptions import ValidationError
#Herencia del modelo padre
class TodoTask(models.Model):
    _name = 'todo.task'
    _inherit = ['todo.task','mail.thread'] 
    user_id = fields.Many2one('res.users', 'Responsible') 
    date_deadline = fields.Date('Deadline')
    name = fields.Char(help="Que necesitas hacer?")

    @api.multi 
    def do_clear_done(self): 
        domain = [('is_done', '=', True), 
                '|', ('user_id', '=', self.env.uid), 
                        ('user_id', '=', False)] 
        dones = self.search(domain) 
        dones.write({'active': False}) 
        return True
    
    @api.multi 
    def do_toggle_done(self): 
        for task in self: 
            if task.user_id != self.env.user: 
                raise ValidationError('Solo el responsable puede hacerlo') 
            else:
                return super(TodoTask, self).do_toggle_done()
    