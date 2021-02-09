# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
# from odoo.addons.base.res.res_request import referenceable_models este paquete ha sido eliminado a partir de Odoo 12
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)

# Modelo Etiqueta 
class Tag(models.Model):
    _name = 'todo.task.tag'
    _description = 'To-do Tag'
    name = fields.Char(string='Name', size=40, translate=True)
    # Relacion inversa Muchos a Muchos (Many2Many)
    task_ids = fields.Many2many('todo.task', string='Tasks')
    # Relaciones jerarquicas:
    _parent_store = True
    _parent_name = 'parent_id'  # Por defecto
    parent_id = fields.Many2one('todo.task.tag', 'Parent Tag', ondelete='restrict')
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)
    parent_path = fields.Char('Parent Path',index=True)
    child_ids = fields.One2many('todo.task.tag', 'parent_id', 'Child Tags')

# Modelo Estado
class Stage(models.Model):
    _name = 'todo.task.stage' 
    _description = 'To-do Stage' 
    _order = 'sequence,name' 
    name = fields.Char(string='Name',size=40,translate=True)    
    desc = fields.Text('Description') 
    state = fields.Selection( 
        [('draft','New'), ('open','Started'),
        ('done','Closed')],'State',default="draft") 
    docs = fields.Html('Documentation') 
    # Campos numericos: 
    sequence = fields.Integer('Sequence') 
    perc_complete = fields.Float('% Complete', (3, 2)) 
    # Campos de fecha: 
    date_effective = fields.Date('Effective Date') 
    date_changed = fields.Datetime('Last Changed') 
    # Otros campos utiles: 
    fold = fields.Boolean('Folded?') 
    image = fields.Binary('Image')
    # Relacion inversa Uno a Muchos (One2Many)
    task_ids = fields.One2many('todo.task', 'stage_id', 'Tasks in this stage')

# Modelo Principal
class TodoTask(models.Model): 
    _inherit = 'todo.task' 
    stage_id = fields.Many2one('todo.task.stage', 'Stage') 
    tag_ids = fields.Many2many('todo.task.tag', string='Tags')

    # Campos de referencia dinamicos
    refers_to = fields.Reference(
        # Ponemos una lista, asi es:
        [('res.user', 'User'), ('res.partner', 'Partner')],
        # Usamos  el estandar "Referenceable Models":
        # referenceable_models, Tenemos que usar el anterior por la version de Odoo 12 
        'Refers to',  # string= (title)
    )
    # Campos relacionados
    stage_state = fields.Selection(
        related='stage_id.state',
        string='Stage State')

    # Campos calculados:
    stage_fold = fields.Boolean(
        string='Stage Folded?',
        compute='_compute_stage_fold',
        search='_search_stage_fold',
        inverse='_write_stage_fold',
        store=False,  # Por defecto
    )    
    @api.one
    @api.depends('stage_id.fold')
    def _compute_stage_fold(self):
        for task in self:
            task.stage_fold = task.stage_id.fold

    def _search_stage_fold(self, operator, value):
        return [('stage_id.fold', operator, value)]

    def _write_stage_fold(self):
        self.stage_id.fold = self.stage_fold

    # Restricciones
    _sql_constraints = [(
        'todo_task_name_unique',
        'UNIQUE (name, user_id, active)',
        'El titulo de la tarea solo puede ser unico'
    )]
    @api.one
    @api.constrains('name')
    def _check_name_size(self):
        if len(self.name) < 7:
            raise ValidationError('El titulo tiene que ser minimo de 7 caracteres')
    @api.one
    def compute_user_todo_count(self):
        for task in self:
            task.user_todo_count = task.search_count([('user_id', '=', task.user_id.id)]) 


    user_todo_count = fields.Integer('User To-Do Count',compute='compute_user_todo_count')

    effort_estimate = fields.Integer('Effort Estimate')