from rest_framework import viewsets, generics
from .models import Animal, DietType, FoodItem, AnimalDiet, MedicalHistory, MedicalStock #, Stock
from .serializers import AnimalSerializer, DietTypeSerializer, FoodItemSerializer, AnimalDietSerializer, MedicalHistorySerializer, MedicalStockSerializer #, StockSerializer

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    
class AnimalByLocationView(generics.ListAPIView):
    serializer_class = AnimalSerializer

    def get_queryset(self):
        location = self.kwargs['location']
        return Animal.objects.filter(location=location)

class AllLocationsView(generics.ListAPIView):
    serializer_class = AnimalSerializer

    def get_queryset(self):
        return Animal.objects.all()

class DietTypeViewSet(viewsets.ModelViewSet):
    queryset = DietType.objects.all()
    serializer_class = DietTypeSerializer

class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

#class StockViewSet(viewsets.ModelViewSet):
 #   queryset = Stock.objects.all()
  #  serializer_class = StockSerializer

class AnimalDietViewSet(viewsets.ModelViewSet):
    queryset = AnimalDiet.objects.all()
    serializer_class = AnimalDietSerializer

class MedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer

class MedicalStockViewSet(viewsets.ModelViewSet):
    queryset = MedicalStock.objects.all()
    serializer_class = MedicalStockSerializer
