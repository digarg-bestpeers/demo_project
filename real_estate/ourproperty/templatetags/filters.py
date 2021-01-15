from django import template
from ourproperty.models import Address
register = template.Library()


@register.filter(name='city')
def city(value):
  qs = Address.objects.all()
  l = []
  for obj in qs:
    x = obj.city
    if x not in l:
      l.append(x)
  print(l)
  return l

