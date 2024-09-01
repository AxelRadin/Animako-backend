from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, VerifyEmailView, ModifyStaffView, StaffListView, StaffTimetableViewSet, LogoutView, CurrentUserView, StaffDetailView

router = DefaultRouter()
router.register('timetable', StaffTimetableViewSet, basename='staff-timetable')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('modify-staff/', ModifyStaffView.as_view(), name='modify-staff'),
    path('delete-staff/<id>/', ModifyStaffView.as_view(), name='delete-staff'),
    path('list/', StaffListView.as_view(), name='staff-list'),
    path('info/<id>/', StaffDetailView.as_view(), name='staff-info'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('', include(router.urls))
]