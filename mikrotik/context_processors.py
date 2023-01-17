def menu(request):
    menu = {
        'menu':{
            'Administración':'administrations.index',
            'Clientes': 'clients.index',
            'Nodos': 'nodos.index',
            'Planes': 'routers.plans.index',
            'Routers': 'routers.index', 
            'Soporte': 'supports.index',
            'Ventas': 'ventas.index',
        }
    }
    return menu