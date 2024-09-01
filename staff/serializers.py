from rest_framework import serializers
from .models import Staff, StaffTimetable

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id','staff_email', 'staff_name', 'staff_fullname', 'staff_role', 'staff_status', 'is_staff']
                
    def create(self, validated_data):
        staff = Staff(**validated_data)
        staff.set_password(None)
        staff.save()
        return staff
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
        
class RegisterSerializer(serializers.Serializer):
    staff_email = serializers.EmailField()
    staff_name = serializers.CharField(max_length=50)
    staff_fullname = serializers.CharField(max_length=50)
    staff_role = serializers.CharField(max_length=50)
    staff_status = serializers.BooleanField()
    
class ModifyStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['staff_email', 'staff_name', 'staff_fullname', 'staff_role', 'staff_status', 'is_staff']
        extra_kwargs = {
            'staff_email': {'required': False},
            'staff_name': {'required': False},
            'staff_fullname': {'required': False},
            'staff_role': {'required': False},
            'staff_status': {'required': False},
            'is_staff': {'required': False}   
        }
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        password_confirm = validated_data.pop('password_confirm', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
                        
        if password and password_confirm:
            if password == password_confirm:
                instance.set_password(password)
            else:
                raise serializers.ValidationError({'password': 'Passwords do not match.'})
        instance.save()
        return instance

class StaffTimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffTimetable
        fields = '__all__'