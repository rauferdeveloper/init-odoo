{ 
    'name': 'Gestor de tareas', 
    'description': 'Gestiona tus tareas personales.', 
    'author': 'Raul Fernandez', 
    'depends': ['base'], 
    'application': True,
    'category': 'test', 
    'data': [
        'views/todo_view.xml',
        'views/todo_menu.xml',
        'security/ir.model.access.csv',
        'security/todo_access_rules.xml' 
    ]
}