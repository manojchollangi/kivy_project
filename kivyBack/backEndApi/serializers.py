from rest_framework import serializers
from .models import User
from .manage import *
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken



class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name','mobile_number',"record_created_date")
        write_only_fields = ('first_name','last_name','mobile_number',"record_created_date")

    def create(self, validated_data):
        user = User.objects.create(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            mobile_number = validated_data['mobile_number'],
            record_created_date = timezone.now()            
        )
        user.save()
        return user
    

class LoginUserSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=100) 
    otp = serializers.CharField(max_length=255,write_only=True)
    token = serializers.CharField(max_length=255,read_only=True)

    def validate(self,data):
        mobile_number = data.get("mobile_number",None)
        print(mobile_number)
        otp = data.get("otp",None)
        print(otp)
        if mobile_number and otp:
            users_list = UserOtp.objects.filter(mobile_number = str(mobile_number), otp = otp)
            if len(users_list)==0:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
            print(users_list[0])
            user = users_list[0]
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        try:
            refresh = RefreshToken.for_user(user)
        except Exception as e:
            print("The generated exception is:",str(e))
        return {"Access_Token":str(refresh.access_token)}
