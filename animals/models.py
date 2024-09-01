from django.db import models





class DietType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    diet_type = models.ForeignKey(DietType, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    unit = models.CharField(max_length=100, default='', blank=True)
    comande_needed = models.BooleanField()
    
    def __str__(self):
        return self.name
    

#class Stock(models.Model):
 #   food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
  #  quantity = models.PositiveIntegerField()  

   # def __str__(self):
    #    return f"{self.food_item.name}: {self.quantity}"

class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    diet_type = models.ForeignKey(DietType, on_delete=models.SET_NULL, null=True)
    #medical_histories = models.ManyToManyField(MedicalHistory, related_name='animals')
    location = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class AnimalDiet(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()  

    def __str__(self):
        return f"{self.animal.name} - {self.food_item.name}: {self.amount}"


    
class MedicalHistory(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='medical_histories')
    event_type = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    

    def __str__(self):
        return f"{self.event_type} on {self.date} for {self.animal.name}"


class MedicalStock(models.Model): 
    description = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=100, default='', blank=True)
    comande_needed = models.BooleanField()