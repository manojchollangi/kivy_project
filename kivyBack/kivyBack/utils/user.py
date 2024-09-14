import re
from backEndApi.models import User


class RegisterUser:
    first_name = ""
    last_name = ""
    mobile_number = ""
    otp = ""
    
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.mobile_number = ""
        self.otp = ""

    def validate_data(self):
        error_list = []
        self.validate_first_name(self.first_name, error_list)
        self.validate_last_name(self.last_name, error_list)
        self.validate_mobile_number(self.mobile_number, error_list)
        self.otp_validation(self.otp,error_list)     
        return error_list
                                 
    def validate_first_name(self, first_name, error_list):
        if self.first_name == None:
            error_list.append('First name cannot be empty')
            return False
        if not self.first_name.isalpha():
            error_list.append("first_name should have only alphabets")
            return False
        if not (len(self.first_name) >= 2 and len(self.first_name) <= 50):
            error_list.append("first_name should have minimum 2 characters maximum 50 characters")
            return False
        return True


    def validate_last_name(self, last_name, error_list):
        if self.last_name == None:
            error_list.append('Last name cannot be empty')
            return False
        if not self.last_name.isalpha():
            error_list.append("last_name should have only alphabets")
            return False
        if not (len(self.last_name)>=2 and len(self.last_name)<=50):
            error_list.append("last_name should have minimum 2 characters maximum 50 characters")
            return False
        return True


    def validate_mobile_number(self, mobile_number, error_list):
        if self.mobile_number == None:
            error_list.append('Mobile number cannot be empty')
            return False
        if not (self.mobile_number.isnumeric() and len(self.mobile_number) == 10):
            error_list.append("Mobile number should be numeric and it should have 10 characters")
            return False
        return True

    def otp_validation(self,otp,error_list):
        if self.otp == None:
            error_list.append('OTP cannot be empty')
            return False
        if not (self.otp.isnumeric() and len(self.otp)== 6):
            error_list.append('OTP must be 6 digit number')
            return False
        return True
    
    def check_mobile_number_exists(self):
        try:
            user_objects = User.objects.filter(mobile_number = self.mobile_number)
            if len(user_objects) != 1 :
                return False
            return True
        except Exception as e:
            pass
        
    def retrieve_validated_user_data(self):
        data = {'first_name':self.first_name,'last_name':self.last_name,"mobile_number":self.mobile_number}
        return data
    