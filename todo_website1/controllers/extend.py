# -*- coding: utf-8 -*- 
from odoo import http 
from custom.todo_website1.controllers.main import Todo 

class TodoExtended(Todo): 
    @http.route(['/hello', '/hello/<name>'])
    def hello(self, name=None, **kwargs): 
        response = super(TodoExtended, self).hello() 
        response.qcontext['name'] = name 
        return response