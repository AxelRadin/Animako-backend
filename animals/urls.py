from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from .views import AnimalListView, AnimalDetailView, StockListView, MedicalHistoryListView
from .views import AnimalViewSet, DietTypeViewSet, FoodItemViewSet, AnimalDietViewSet, MedicalHistoryViewSet, MedicalStockViewSet, AnimalByLocationView, AllLocationsView #, StockViewSet

router = DefaultRouter()
router.register(r'animals', AnimalViewSet)
router.register(r'diettypes', DietTypeViewSet)
router.register(r'fooditems', FoodItemViewSet)
#router.register(r'stocks', StockViewSet)
router.register(r'animaldiets', AnimalDietViewSet)
router.register(r'medicalhistories', MedicalHistoryViewSet)
router.register(r'medicalstocks', MedicalStockViewSet)

urlpatterns = [
    #path('animals/', AnimalListView.as_view(), name='animal-list'),
    #path('animals/<int:pk>/', AnimalDetailView.as_view(), name='animal-detail'),
    #path('stocks/', StockListView.as_view(), name='stock-list'),
    #path('medical-history/', MedicalHistoryListView.as_view(), name='medical-history-list'),
    path('', include(router.urls)),
    path('animals/location/<int:location>/', AnimalByLocationView.as_view(), name='animal-by-location'),
    # path('animals/', AllLocationsView.as_view(), name='all-animals'),
]
