import os

os.environ.setdefault('DJANGO_SETINGS_MODULE', 'ecommerce.settings')


import django
django.setup()

import random
from api.models import *
from faker import Faker

fakegen = Faker()

user_type = ['Admin', 'Customer']

def add_types(i):
    t = UserType.objects.get_or_create(description=user_type[i])[0]
    t.save()
    return t


def customer_populate(n=3):
    for user in range(n):
        firstName = fakegen.first_name()
        lastName = fakegen.last_name()
