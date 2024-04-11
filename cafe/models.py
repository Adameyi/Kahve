from django.db import models

ROAST_LEVEL_CHOICES = (
    ('Light','LIGHT'),
    ('Medium', 'MEDIUM'),
    ('Medium-Dark','MEDIUM-DARK'),
    ('Dark','DARK'),
    ('Espresso','ESPRESSO'),
)

SIZE_CHOICES = (
    ('Small','SMALL'),
    ('Medium', 'MEDIUM'),
    ('Large','LARGE'),
)
class Product(models.Model): 
    #CATEGORIES
    COFFEE = 'Coffee'
    MILKSHAKE = 'Milkshake'
    TEA = 'Tea'
    SMOOTHIE = 'Smoothie'
    OTHER = 'Other'
    
    DRINK_CHOICES = [
        (COFFEE, 'COFFEE'),
        (TEA ,'TEA'),
        (MILKSHAKE,'MILKSHAKE'),
        (SMOOTHIE,'SMOOTHIE'),
        (OTHER,'OTHER')
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, blank=True)
    price = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=20, choices=DRINK_CHOICES, default=OTHER)
    favourited = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        #Check if image = models.ImageField is blank
        if not self.image:
            self.image = 'images/coffeePlaceholder.jpg'
            print(self.image)
        super().save(*args, **kwargs)

class ProductCustomization(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, blank=True)
    quantity_small = models.CharField(max_length=4, blank=True)
    quantity_medium = models.CharField(max_length=4, blank=True)
    quantity_large = models.CharField(max_length=4, blank=True)
    temperature = models.CharField(max_length=4, default=75, blank=True)
    brewing_method = models.CharField(max_length=100, blank=True)
    roast_level = models.CharField(max_length=20, choices=ROAST_LEVEL_CHOICES, blank=True)
    milk_type = models.CharField(max_length=50, blank=True)

class ProductPreference(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    toppings = models.ManyToManyField('Topping', blank=True)
    sweeteners = models.ManyToManyField('Sweetener', blank=True)
    flavours = models.ManyToManyField('Flavour', blank=True)

class Topping(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Sweetener(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Flavour(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
