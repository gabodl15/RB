from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Router, Plan

import getpass

@receiver(post_migrate)
def crear_router(sender, **kwargs):
    if sender.name == 'routers':
        if not Router.objects.exists():
            print('\n')
            print('------------------------')
            print('CONFIGURACION DEL ROUTER')
            router_nombre = input("Nombre del Router: ")
            router_ip = input('IP: ')
            router_user = input('Usuario: ')
            router_password = getpass.getpass('Password: ')
            Router.objects.create(
                name=router_nombre,
                ip=router_ip,
                user=router_user,
                password=router_password
            )

@receiver(post_migrate)
def create_plan(sender, **kwargs):
    if sender.name == 'routers':
        if not Plan.objects.exists():
            routers = Router.objects.all().values_list('id')
            plan = Plan.objects.create(
                name='CORTADOS',
                code='CORTADO',
                price=0.00,
            )

            plan.routers.add(routers)