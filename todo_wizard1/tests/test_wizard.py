# -*- coding: utf-8 -*- 
from datetime import date
from odoo.tests.common import TransactionCase
from odoo.exceptions import Warning
from odoo import fields
class TestWizard(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestWizard, self).setUp(*args, **kwargs)
        # Cerrar cualquier tarea de la aplicacion
        self.env['todo.task']\
            .search([('is_done', '=', False)])\
            .write({'is_done': True})
        # Demo user will be used to run tests
        demo_user = self.env.ref('base.user_demo') 
        # Create two Todo tasks to use in tests
        t0 = date.today()
        Task = self.env['todo.task'].sudo(demo_user)
        self.todo1 = Task.create({
            'name': 'pruebadetest1',
            'date_deadline': fields.Date.to_string(t0)})
        self.todo2 = Task.create({
            'name': 'pruebadetest2'})
        # Create Wizard instance to use in tests
        Wizard = self.env['todo.wizard'].sudo(demo_user)
        self.wizard = Wizard.create({})
    def test_count(self): 
        'Probar el boton de cantidad' 
        with self.assertRaises(Warning) as e: 
            self.wizard.do_count_tasks() 
        self.assertIn('2', str(e.exception))
    
    """ En desarrollo
    def test_populate_tasks(self): 
        "Actualizar los datos de las dos tareas" 
        with self.assertRaises(Warning) as e: 
            self.wizard['new_deadline'] = "2019-05-20"
        self.assertTrue(self.wizard.do_mass_update(), str(e.exception))"""
        