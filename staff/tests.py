from django.test import TestCase

from staff.models import Staff, StaffTimetable

class StaffTestCase(TestCase):
    
    TEST_NOM = "Aude"
    
    def setUp(self):
        self.staffTest = Staff()
        self.staffTest.staff_name = self.TEST_NOM
        self.staffTest.staff_fullname = "Aude"
        self.staffTest.staff_email = "aude@mail.com"
        self.staffTest.staff_role = "role"
        self.staffTest.staff_status = False
        
        self.staffTest.save()
    
    def test_staff(self):
        #self.assertTrue(True)
        
        nb_staff_before = Staff.objects.count()
        
        new_staff = Staff()
        new_staff.staff_fullname = "John"
        new_staff.staff_name = "Doe"
        new_staff.staff_email = "mail@mail.com"
        new_staff.staff_role = "role"
        new_staff.staff_status = False
        
        new_staff.save()        
        
        nb_staff_after = Staff.objects.count()
        
        self.assertTrue(nb_staff_after, nb_staff_before + 1)
 
    def test_update_staff(self):
        
        self.assertEqual(self.staffTest.staff_name, self.TEST_NOM)
        
        self.staffTest.staff_name = "John"
        self.staffTest.save()
        
        temp_staff = Staff.objects.get(pk=self.staffTest.pk)
        
        self.assertEqual(temp_staff.staff_name, "John")        
        
    def test_delete_staff(self):
        
        nbr_staff_before = Staff.objects.count()
        
        self.staffTest.delete()
        
        nbr_staff_after = Staff.objects.count()
        
        self.assertTrue(nbr_staff_after == nbr_staff_before - 1)
        
class StaffTimetableTestCase(TestCase):        
    
    def setUp(self):
        self.staff = Staff.objects.create(staff_name="Doe", staff_fullname="John", staff_email="test@mail.com", staff_role="role", staff_status=False)
        
    def test_staff_timetable(self):
        #self.assertTrue(True)
        
        nb_staff_timetable_before = StaffTimetable.objects.count()
        
        new_staff_timetable = StaffTimetable()
        new_staff_timetable.staff_id = self.staff
        new_staff_timetable.staff_task = "Task"
        new_staff_timetable.staff_status = False
        
        new_staff_timetable.save()        
        
        nb_staff_timetable_after = StaffTimetable.objects.count()
        
        self.assertTrue(nb_staff_timetable_after, nb_staff_timetable_before + 1)
    