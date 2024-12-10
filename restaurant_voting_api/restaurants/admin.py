from django.contrib import admin

from .models import Item, Menu, Restaurant

admin.site.register(Menu)
admin.site.register(Item)
admin.site.register(Restaurant)
