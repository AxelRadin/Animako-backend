from django.contrib import admin
from .models import Animal, DietType, FoodItem, AnimalDiet #, Stock

admin.site.register(Animal)
admin.site.register(DietType)
admin.site.register(FoodItem)
#admin.site.register(Stock)
admin.site.register(AnimalDiet)
