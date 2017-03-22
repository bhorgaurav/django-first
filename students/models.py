from django.db import models

from django.core.validators import RegexValidator

# Create your models here.
mobile_phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$', message="Format is: '+999999999'. You can enter upto 12 digits.")

class StudentRecord(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(validators=[mobile_phone_regex], max_length=13)
    def __str__(self):
        return str(self.mobile_number) + "::" + str(self.name)

class StudentClasses(models.Model):
    student_id = models.ForeignKey(StudentRecord, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=10)
    def __str__(self):
        return str(self.class_name)

class VerificationCodes(models.Model):
    mobile_number = models.CharField(validators=[mobile_phone_regex], max_length=13)
    # To separate registration and view info verification process. 1 = registration. 2 = view info.
    type_flag = models.PositiveSmallIntegerField()
    pin = models.PositiveSmallIntegerField()
    def __str__(self):
        return str(self.mobile_number) + "::" + str(self.pin)