from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarMakeAdmin class - customiza a exibição no admin
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'country', 'established_year']
    search_fields = ['name', 'country']
    list_filter = ['country']


# CarModelAdmin class - customiza a exibição no admin
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'car_make', 'type', 'year', 'dealer_id', 'price']
    search_fields = ['name', 'car_make__name']  # Busca por nome do modelo ou marca
    list_filter = ['type', 'year', 'car_make', 'fuel_type', 'transmission']
    ordering = ['-year', 'car_make']


# Registra os models no admin site
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)

