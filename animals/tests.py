from django.test import TestCase
from .models import DietType, FoodItem, Animal, AnimalDiet, MedicalHistory, MedicalStock #, Stock 
import datetime

class AnimalModelTest(TestCase):

    def setUp(self):
        self.diet_type = DietType.objects.create(name="Herbivore")
        self.food_item = FoodItem.objects.create(name="Grass", diet_type=self.diet_type, quantity=100, unit="kg", comande_needed=False )
        #self.stock = Stock.objects.create(food_item=self.food_item, quantity=100)
        self.animal = Animal.objects.create(
            name="Giraffe",
            species="Giraffa camelopardalis",
            date_of_birth="2010-05-01",
            diet_type=self.diet_type,
            location="1"
        )
        self.animal_diet = AnimalDiet.objects.create(animal=self.animal, food_item=self.food_item, amount=50)
        self.medical_history = MedicalHistory.objects.create(
            animal=self.animal,
            event_type="Vaccination",
            description="Routine vaccination",
            date="2023-01-01"
        )
        self.medical_stock = MedicalStock.objects.create(
            description="Syringes",
            quantity=30,
            unit="pieces",
            comande_needed=False
        )
#*******************************création***********************************
    def test_animal_creation(self):
        self.assertEqual(self.animal.name, "Giraffe")
        self.assertEqual(self.animal.species, "Giraffa camelopardalis")
        self.assertEqual(self.animal.diet_type.name, "Herbivore")

    def test_food_item_creation(self):
        self.assertEqual(self.food_item.name, "Grass")
        self.assertEqual(self.food_item.diet_type.name, "Herbivore")
        self.assertEqual(self.food_item.quantity, 100)
        self.assertEqual(self.food_item.unit, "kg")
        self.assertFalse(self.medical_stock.comande_needed)
    #def test_stock_creation(self):
     #   self.assertEqual(self.stock.food_item.name, "Grass")
      #  self.assertEqual(self.stock.quantity, 100)

    def test_animal_diet_creation(self):
        self.assertEqual(self.animal_diet.animal.name, "Giraffe")
        self.assertEqual(self.animal_diet.food_item.name, "Grass")
        self.assertEqual(self.animal_diet.amount, 50)

    def test_medical_history_creation(self):
        self.assertEqual(self.medical_history.animal.name, "Giraffe")
        self.assertEqual(self.medical_history.event_type, "Vaccination")
        self.assertEqual(self.medical_history.description, "Routine vaccination")
        self.assertEqual(self.medical_history.date, "2023-01-01")

    def test_medical_stock_creation(self):
        self.assertEqual(self.medical_stock.description, "Syringes")
        self.assertEqual(self.medical_stock.quantity, 30)
        self.assertEqual(self.medical_stock.unit, "pieces")
        self.assertFalse(self.medical_stock.comande_needed)

#***************************************modification******************************
    def test_animal_update(self):
        self.animal.name = "Updated Giraffe"
        self.animal.species = "Updated Species"
        self.animal.date_of_birth = "2012-06-01"
        self.animal.diet_type = DietType.objects.create(name="Carnivore")
        self.animal.location = "2"
        self.animal.save()

        updated_animal = Animal.objects.get(pk=self.animal.pk)
        self.assertEqual(updated_animal.name, "Updated Giraffe")
        self.assertEqual(updated_animal.species, "Updated Species")
        self.assertEqual(updated_animal.date_of_birth, datetime.date(2012, 6, 1))
        self.assertEqual(updated_animal.diet_type.name, "Carnivore")
        self.assertEqual(updated_animal.location, 2)

    def test_food_item_update(self):
        self.food_item.name = "Updated Grass"
        self.food_item.diet_type = DietType.objects.create(name="Omnivore")
        self.food_item.quantity = 200
        self.food_item.unit = "liters"
        self.food_item.comande_needed = True
        self.food_item.save()

        updated_food_item = FoodItem.objects.get(pk=self.food_item.pk)
        self.assertEqual(updated_food_item.name, "Updated Grass")
        self.assertEqual(updated_food_item.diet_type.name, "Omnivore")
        self.assertEqual(updated_food_item.quantity, 200)
        self.assertEqual(updated_food_item.unit, "liters")
        self.assertEqual(updated_food_item.comande_needed, True)

    #def test_stock_update(self):
     #   self.stock.quantity = 200
      #  self.stock.save()

       # updated_stock = Stock.objects.get(pk=self.stock.pk)
        #self.assertEqual(updated_stock.quantity, 200)

    def test_animal_diet_update(self):
        self.animal_diet.amount = 100
        self.animal_diet.save()

        updated_animal_diet = AnimalDiet.objects.get(pk=self.animal_diet.pk)
        self.assertEqual(updated_animal_diet.amount, 100)

    def test_medical_history_update(self):
        self.medical_history.event_type = "Checkup"
        self.medical_history.description = "Updated description"
        self.medical_history.date = "2024-02-01"
        self.medical_history.save()

        updated_history = MedicalHistory.objects.get(pk=self.medical_history.pk)
        self.assertEqual(updated_history.event_type, "Checkup")
        self.assertEqual(updated_history.description, "Updated description")
        self.assertEqual(updated_history.date, datetime.date(2024, 2, 1))

    def test_medical_stock_update(self):
        self.medical_stock.description = "Updated Syringes"
        self.medical_stock.quantity = 50
        self.medical_stock.unit = "boxes"
        self.medical_stock.comande_needed = True
        self.medical_stock.save()

        updated_medical_stock = MedicalStock.objects.get(pk=self.medical_stock.pk)
        self.assertEqual(updated_medical_stock.description, "Updated Syringes")
        self.assertEqual(updated_medical_stock.quantity, 50)
        self.assertEqual(updated_medical_stock.unit, "boxes")
        self.assertTrue(updated_medical_stock.comande_needed)

#****************************************supprétion*******************************
def test_animal_deletion(self):
        animal_id = self.animal.id
        self.animal.delete()

        with self.assertRaises(Animal.DoesNotExist):
            Animal.objects.get(id=animal_id)

def test_food_item_deletion(self):
    food_item_id = self.food_item.id
    self.food_item.delete()

    with self.assertRaises(FoodItem.DoesNotExist):
        FoodItem.objects.get(id=food_item_id)

#def test_stock_deletion(self):
 #   stock_id = self.stock.id
  #  self.stock.delete()

   # with self.assertRaises(Stock.DoesNotExist):
    #    Stock.objects.get(id=stock_id)

def test_animal_diet_deletion(self):
    animal_diet_id = self.animal_diet.id
    self.animal_diet.delete()

    with self.assertRaises(AnimalDiet.DoesNotExist):
        AnimalDiet.objects.get(id=animal_diet_id)

def test_medical_history_deletion(self):
    medical_history_id = self.medical_history.id
    self.medical_history.delete()

    with self.assertRaises(MedicalHistory.DoesNotExist):
        MedicalHistory.objects.get(id=medical_history_id)

def test_medical_stock_deletion(self):
    medical_stock_id = self.medical_stock.id
    self.medical_stock.delete()

    with self.assertRaises(MedicalStock.DoesNotExist):
        MedicalStock.objects.get(id=medical_stock_id)


def test_cascade_delete(self):
        self.animal.delete()

        with self.assertRaises(AnimalDiet.DoesNotExist):
            AnimalDiet.objects.get(animal=self.animal)

        with self.assertRaises(MedicalHistory.DoesNotExist):
            MedicalHistory.objects.get(animal=self.animal)