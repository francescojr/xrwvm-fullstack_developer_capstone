# Uncomment the following imports before adding the Model code

from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Optional: add more fields
    country = models.CharField(max_length=50, blank=True, null=True)  # País de origem
    established_year = models.IntegerField(blank=True, null=True)  # Ano de fundação
    
    def __str__(self):
        return self.name  # Return the name as the string representation


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Dealer Id (IntegerField)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    # Many-to-One relationship to CarMake
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    
    # Dealer Id - refers to dealer created in Cloudant database
    dealer_id = models.IntegerField()
    
    # Car Model Name
    name = models.CharField(max_length=100)
    
    # Type choices
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('HATCHBACK', 'Hatchback'),
        ('COUPE', 'Coupe'),
        ('CONVERTIBLE', 'Convertible'),
        ('TRUCK', 'Truck'),
        ('VAN', 'Van'),
    ]
    type = models.CharField(max_length=15, choices=CAR_TYPES, default='SUV')
    
    # Year with validators
    year = models.IntegerField(
        default=2023,
        validators=[
            MaxValueValidator(2023),
            MinValueValidator(2015)
        ]
    )
    
    # Optional: Additional fields
    color = models.CharField(max_length=50, blank=True, null=True)
    mileage = models.IntegerField(blank=True, null=True, help_text="Mileage in miles")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    transmission = models.CharField(
        max_length=20, 
        choices=[
            ('AUTOMATIC', 'Automatic'),
            ('MANUAL', 'Manual'),
        ],
        blank=True,
        null=True
    )
    engine_size = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        blank=True, 
        null=True,
        help_text="Engine size in liters"
    )
    fuel_type = models.CharField(
        max_length=20,
        choices=[
            ('GASOLINE', 'Gasoline'),
            ('DIESEL', 'Diesel'),
            ('ELECTRIC', 'Electric'),
            ('HYBRID', 'Hybrid'),
        ],
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"  # Return car make and model
