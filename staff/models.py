from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from animals.models import Animal

TASK_STATUS = (
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
)

TASK_TYPE = (
    ('feeding', 'Feeding'),
    ('cleaning', 'Cleaning'),
    ('medication', 'Medication'),
    ('veterinary', 'Veterinary'),
    ('show', 'Show'),
    ('other', 'Other'),
)

class StaffTimetable(models.Model):
    staff_id = models.ManyToManyField('Staff', related_name='timetables')
    animals_id = models.ManyToManyField('animals.Animal', related_name='timetables', blank=True)
    staff_task = models.CharField(max_length=250)
    task_start_time = models.DateTimeField()
    task_end_time = models.DateTimeField()
    task_status = models.CharField(max_length=50, choices=TASK_STATUS, default='pending')
    task_type = models.CharField(max_length=50, choices=TASK_TYPE)

    class Meta:
        db_table = 'staff_timetable'
        managed = True
        verbose_name = 'Staff Timetable'
        verbose_name_plural = 'Staff Timetables'

    def __str__(self):
        return self.staff_task
    
class StaffManager(BaseUserManager):
    def create_user(self, staff_email, password=None, **extra_fields):
        if not staff_email:
            raise ValueError('The Email field must be set')
        staff_email = self.normalize_email(staff_email)
        user = self.model(staff_email=staff_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, staff_email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        extra_fields.setdefault('staff_name', 'Superuser')
        extra_fields.setdefault('staff_fullname', 'Admin')
        extra_fields.setdefault('staff_role', 'admin')
        extra_fields.setdefault('staff_status', True)
        
        return self.create_user(staff_email, password, **extra_fields)

class Staff(AbstractBaseUser, PermissionsMixin):
    
    staff_email = models.EmailField(max_length=255, unique=True)
    staff_name = models.CharField(max_length=50)
    staff_fullname = models.CharField(max_length=50)
    staff_role = models.CharField(max_length=50)
    staff_picture = models.ImageField(null=True, default='default.jpg')
    staff_status = models.BooleanField()
    
    is_staff = models.BooleanField(default=True)
    
    objects = StaffManager()
    
    USERNAME_FIELD = 'staff_email'
    REQUIRED_FIELDS = ['staff_name', 'staff_fullname', 'staff_role', 'staff_status']

    class Meta:
        db_table = 'staff'
        managed = True
        verbose_name = 'Staff'
        verbose_name_plural = 'Staffs'

    def __str__(self):
        return self.staff_fullname

    
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Staff.objects.create(staff=instance)
        
# def save_user_profile(sender, instance, **kwargs):
#     instance.staff.save()
    