from django import template

register = template.Library()

@register.filter
def sum_price(profiles):
    total = 0
    for profile in profiles:
        total += profile.plan.price
        
    return total
