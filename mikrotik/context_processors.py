def menu(request):
    menu = {
        'menu':{
            'administration':['Administración','administrations.index'],
            'clients':['Clientes','clients.index'],
            'nodos': ['Nodos', 'nodos.index'],
            'plans':['Planes', 'routers.plans.index'],
            'routers':['Routers', 'routers.index'] ,
            'supports':['Soporte', 'supports.index'],
            'ventas':['Ventas', 'ventas.index'],
        }
    }
    return menu