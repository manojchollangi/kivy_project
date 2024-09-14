from .models import *
import http.client
import random as r
from django.conf import settings
from datetime import datetime

 
def user_objects(mobile_number):
    return User.objects.filter(mobile_number=mobile_number)


def mobile_number_validation(mobile_number):
    if not (mobile_number.isnumeric() and len(mobile_number) == 10):
        return False
    return True


def random_password_generator():
    password = ""
    for i in range(6):
        password += str(r.randint(0,9))
    return password


def send_otp(mobile):
    try:
        conn = http.client.HTTPSConnection("2factor.in")
        otp = random_password_generator()
        conn.request("GET", settings.API_URL+"module=SMS_OTP&apikey="+settings.API_KEY+"&to="+str(mobile)+"&otpvalue="+str(otp))
        res = conn.getresponse()
        data = res.read()
        return otp
    except Exception as e:
        print("Generated exception is:",str(e))


def save_otp_db(mobile_number,otp):
    try:
        #get otp mobile object from otp table with mobile_number if it is null create new object
        otp_obj = get_otp_obj_by_mobile(mobile_number)
        if otp_obj is None :
            new_object_creation_in_user_otp(mobile_number,otp)
        else:
            update_otp_object(otp, otp_obj)
    except Exception as e:
        print('Error while saving OTP to DB : ',str(e))


#
def get_otp_obj_by_mobile(mobile_number):
    try:
        user = UserOtp.objects.filter(mobile_number = str(mobile_number))
        if len(user)>0:
            return user[0]
        return None
    except Exception as e:
        print("The generated exception is:",str(e))
        return None


def update_otp_object(otp,otp_obj):
    try:
        otp_obj.otp = otp
        otp_obj.created_time = datetime.now()
        otp_obj.save()
    except Exception as e:
        print("The Generated exception is:",str(e))
        pass


def new_object_creation_in_user_otp(mobile_number,otp):
    UserOtp.objects.create(mobile_number=str(mobile_number), otp=otp, created_time = datetime.now())


def verify_otp(mobile_number,otp):
    try:
        otp_obj = UserOtp.objects.filter(mobile_number=str(mobile_number),otp=str(otp))
        if len(otp_obj) == 1:
            return True
        return False
    except Exception as e:
        print("Exception in checking otp:",str(e))
        return False


def check_mobile_number_in_user(mobile_number):
    try:
        user_obj = User.objects.filter(mobile_number = str(mobile_number))
        print(user_obj,type(user_obj))
        print(len(user_obj))
        if len(user_obj) == 1:
            return True
        return False
    except Exception as e:
        print("Exception in checking user:",str(e))
        return False