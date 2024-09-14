from django.db import models
from django.contrib.auth.models import AbstractBaseUser,UserManager
import uuid


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False,unique=True)
    first_name = models.CharField(db_column='FIRST_NAME', max_length=100, blank=True, null=True)
    mobile_number = models.CharField(db_column='MOBILE_NUMBER',max_length=10,blank=True, null=True,unique = True) 
    last_name = models.CharField(db_column='LAST_NAME', max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    record_created_date = models.DateTimeField(blank=True, null=True)
    record_update_date = models.DateTimeField(blank=True, null=True)
    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = ["first_name","last_name"]

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.mobile_number

    class Meta:
        db_table = U"users"


class UserOtp(models.Model):
    id = models.AutoField(primary_key=True)
    mobile_number = models.CharField(db_column='MOBILE_NUMBER', max_length=10, blank=True, null=True)  # Field name made lowercase.
    otp = models.CharField(db_column='OTP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    created_time = models.DateTimeField(db_column='CREATED_TIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'user_otp'