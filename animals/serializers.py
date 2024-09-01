from rest_framework import serializers
from .models import Animal, DietType, FoodItem, AnimalDiet, MedicalHistory, MedicalStock #, Stock

class AnimalSerializer(serializers.ModelSerializer):
    diet_type_name = serializers.CharField(source='diet_type.name', read_only=True)

    class Meta:
        model = Animal
        fields = '__all__'

class DietTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietType
        fields = '__all__'

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'

#class StockSerializer(serializers.ModelSerializer):
 #   class Meta:
  #      model = Stock
   #     fields = '__all__'

class AnimalDietSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalDiet
        fields = '__all__'

class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = '__all__'

class MedicalStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalStock
        fields = '__all__'
