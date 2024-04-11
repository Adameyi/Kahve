from django.contrib import admin
from. models import Product, ProductCustomization, ProductPreference, Sweetener, Topping, Flavour

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductCustomization)
admin.site.register(ProductPreference)
admin.site.register(Topping)
admin.site.register(Sweetener)
admin.site.register(Flavour)