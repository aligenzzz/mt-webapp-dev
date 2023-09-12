from django import template
from ..models import Client


register = template.Library()


@register.filter(name='is_client')
def is_client(username):
    return Client.objects.filter(username=username).exists()
