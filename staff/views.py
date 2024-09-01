from rest_framework import generics, status, viewsets
from rest_framework.response import Response
#afrom rest_framework.jsonresponse import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.mail import EmailMessage
from django.core.mail import send_mail
#from backend.settings import EMAIL_HOST_USER
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .models import Staff, StaffTimetable
from .serializers import StaffSerializer, RegisterSerializer, ModifyStaffSerializer, StaffTimetableSerializer

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'You are not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user.staff_role != 'admin' and request.user.staff_role != 'superadmin' and request.user.staff_role != 'manager':
            return Response({'error': 'You are not authorized to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['staff_email']
            name = serializer.validated_data['staff_name']
            fullname = serializer.validated_data['staff_fullname']
            role = serializer.validated_data['staff_role']
            staff_status = serializer.validated_data['staff_status']
            
            user = Staff.objects.create_user(staff_email=email, password=None, staff_name=name, staff_fullname=fullname, staff_role=role, staff_status=staff_status)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            link = f"http://localhost:8081/confirm-password?uid={uid}&token={token}"
            mail_subject = 'Validation de votre adresse email pour votre compte Animako'
            message = "Bonjour " + fullname + ",\n\n" + "Cliquez sur le lien ci-dessous pour valider votre adresse email et activer votre compte:\n" + link + "\n\n" + "Cordialement,\n" + "L'équipe Animako"
            to_email = email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            print (uid)
            # recipient_list = [to_email]
            # send_mail(mail_subject,message,EMAIL_HOST_USER,recipient_list,fail_silently=True)
            # messages.success(request, 'Un mail de vérification vous a été envoyer.')
            return Response({
                'message': 'Un mail de vérification vous a été envoyé.',
                'token': token,
                'uid': uid
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Staff.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Staff.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            return Response({'uid': uidb64, 'token': token})
        return Response({'error': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Staff.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Staff.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            password = request.data.get('password')
            password_confirm = request.data.get('password_confirm')
            if password and password_confirm:
                if password == password_confirm:
                    user.set_password(password)
                    user.is_active = True
                    user.save()
                    login(request, user)
                    return Response({'message': 'Password set successfully.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Passwords are required'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        staff_data = request.data
        staff_email = staff_data.get('staff_email')
        password = staff_data.get('password')

        if not staff_email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        staff = authenticate(request, username=staff_email, password=password)

        if staff is not None:
            login(request, staff)
            refresh = RefreshToken.for_user(staff)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'uid': urlsafe_base64_encode(force_bytes(staff.pk)),
                'isAdmin': True if staff.staff_role == 'admin' or staff.staff_role == 'superadmin' or staff.staff_role == 'manager' else False,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    def post(self, request):
        try:
            # refresh_token = request.data['refresh']
            # token = RefreshToken(refresh_token)
            # token.blacklist()
            logout(request)
            return Response({'message': 'User successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
class StaffListView(generics.ListCreateAPIView):
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'You are not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user.staff_role != 'admin' and request.user.staff_role != 'superadmin' and request.user.staff_role != 'manager':
            return Response({'error': 'You are not authorized to perform this action.',
                             'user': str(request.user),
                             'role': request.user.staff_role,
                             }, status=status.HTTP_401_UNAUTHORIZED)
        staff = Staff.objects.all()
        serializer = StaffSerializer(staff, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class StaffDetailView(generics.RetrieveAPIView):
    
    def get(self, request, id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'You are not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        if request.user.staff_role != 'admin' and request.user.staff_role != 'superadmin' and request.user.staff_role != 'manager':
            return Response({'error': 'You are not authorized to perform this action.',
                             'user': str(request.user),
                             'role': request.user.staff_role,
                             }, status=status.HTTP_401_UNAUTHORIZED)
        try:
            staff = Staff.objects.get(pk=id)
        except (TypeError, ValueError, OverflowError, Staff.DoesNotExist):
            staff = None
        if staff is not None:
            serializer = StaffSerializer(staff)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
class CurrentUserView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        return StaffSerializer
    
class ModifyStaffView(generics.RetrieveUpdateDestroyAPIView):
    def put(self, request, *args, **kwargs):
        
        try:
            user = Staff.objects.get(pk=request.user.pk)
        except (TypeError, ValueError, OverflowError, Staff.DoesNotExist):
            user = None
            
        if user is not None :
            serializer = ModifyStaffSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, id, *args, **kwargs):
        try:
            user = Staff.objects.get(pk=id)
        except (TypeError, ValueError, OverflowError, Staff.DoesNotExist):
            user = None
        if user is not None :
            user.delete()
            return Response({"message": "User successfully deleted."},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class StaffTimetableViewSet(viewsets.ModelViewSet):
    queryset = StaffTimetable.objects.all()
    serializer_class = StaffTimetableSerializer
    #permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)