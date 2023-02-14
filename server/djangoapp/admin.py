from django.contrib import admin
from .models import CarMake, CarModel
# from .models import related models


# Register your models here.
#admin.site.register(CarMake)
#admin.site.register(CarModel)

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel 

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['carMake', 'name', 'dealerId', 'carType', 'year']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
