# -*- coding: utf-8 -*- 
from odoo import http 
from odoo.http import request

class Todo(http.Controller): 

    @http.route('/helloworld', auth='public') 
    def hello_world(self): 
        return('<h1>Hola Mundo!!!!!</h1>')

    @http.route('/hello', auth='public', website=True) 
    def hello(self, **kwargs):
        return request.render('todo_website1.hello')
    
    @http.route('/hellocms/<page>', auth='public')
    def hellocms(self, page, **kwargs):
        # Ejemplo sencillo de CMS
        return request.render(page)
    @http.route('/tareas', auth='user' , website=True) 
    def index(self, **kwargs): 
        TodoTask = request.env['todo.task'] 
        tasks =  TodoTask.search([]) 
        return request.render('todo_website1.index', {'tasks': tasks})
    @http.route('/tareas/<model("todo.task"):task>', website=True) 
    def detail(self, task, **kwargs): 
        return http.request.render('todo_website1.detail', {'task': task})
    @http.route('/tareas/add', website=True) 
    def add(self, **kwargs): 
        users = request.env['res.users'].search([]) 
        return request.render('todo_website1.add', {'users': users})