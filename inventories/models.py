from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=50, verbose_name='Marca')

    def __str__(self) -> str:
        return self.name

class Inventory(models.Model):
    image = models.ImageField(upload_to='inventories', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='Equipo')
    brand = models.ForeignKey(Brand, verbose_name='Marca', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(verbose_name='Descripción', blank=True, null=True)
    stored = models.IntegerField(default=0, verbose_name='Almacenado')

    def __str__(self) -> str:
        return self.name
    