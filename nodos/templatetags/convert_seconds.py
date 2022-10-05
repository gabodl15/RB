from django import template

register = template.Library()

@register.filter
def convert_seconds(seconds):
    horas = int(seconds / 60 / 60)
    seconds -= horas*60*60
    minutos = int(seconds/60)
    seconds -= minutos*60
    return f"{horas:02d}:{minutos:02d}:{seconds:02d}"
