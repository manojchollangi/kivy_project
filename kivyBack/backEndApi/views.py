from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes
import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from .manage import *
from kivyBack.utils.user import *
from kivyBack.utils.results import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken

#Globally declaring a list named with logout tokens
logout_tokens = [] 



#Mobile number verification API
@api_view(['POST'])
@permission_classes((AllowAny,))
def get_otp_to_mobile_number(request):
    result = ResultObject()
    if request.method == "POST":
        mobile_number = request.data["mobile_number"]
        valid = mobile_number_validation(mobile_number)
        if not valid:
            result.set_message(message ="Mobile number is invalid",result_status=False)
            return JsonResponse({"data":ResultObjectSerializer(result).data}, status=status.HTTP_400_BAD_REQUEST, safe = False)
        otp = send_otp(mobile_number)
        print(otp)
        save_otp_db(mobile_number,otp)
        result.set_message(message ="OTP successfully generated",result_status=True)
        return JsonResponse({"data":ResultObjectSerializer(result).data},status=status.HTTP_201_CREATED,safe=False)
    return JsonResponse({"message":"GET method not implemented"}, status = status.HTTP_400_BAD_REQUEST)


def get_register_user(request):
    register_user = RegisterUser()
    register_user.first_name = request.data.get('first_name')
    register_user.last_name  = request.data.get('last_name')
    register_user.mobile_number = request.data.get('mobile_number')
    register_user.otp = request.data.get('otp')
    return register_user


@api_view(["POST"]) 
@permission_classes((AllowAny,))
def user_creation(request):
    result = ResultObject()
    if request.method == 'POST':
        register_user = get_register_user(request)
        error_list = register_user.validate_data()
        if len(error_list) > 0:
            result.set_error_list(error_list,False)
            return JsonResponse({"data":ResultObjectSerializer(result).data},status=status.HTTP_400_BAD_REQUEST)
        verified=verify_otp(register_user.mobile_number,register_user.otp)
        if not verified:
            result.set_error_list(['OTP check is failed'],False)
            return JsonResponse({"data":ResultObjectSerializer(result).data},status=status.HTTP_400_BAD_REQUEST)
        """
        exists = register_user.check_mobile_number_exists()
        if exists:
            result.set_error_list(['Mobile number is already in use'],False)
            return JsonResponse({"data":ResultObjectSerializer(result).data},status=status.HTTP_400_BAD_REQUEST)
        """
        data = register_user.retrieve_validated_user_data()
        serialized = RegisterUserSerializer(data = data)
        if not serialized.is_valid():
            return JsonResponse({"data":serialized._errors}, status = status.HTTP_400_BAD_REQUEST)
        user = serialized.save()
        if user:
            token = RefreshToken.for_user(user)
            print(str(token.access_token))         
            result.set_message_object("User successfully created",serialized.data,True)
            return JsonResponse({"data":ResultObjectSerializer(result).data,"Access_Token":str(token.access_token)}, status = status.HTTP_201_CREATED)
    return JsonResponse({"message":"GET method not implemented"}, status = status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def signin_view(request):
    result = ResultObject()
    if request.method == 'POST':
        mobile_number = request.data.get('mobile_number')
        otp = request.data.get('otp')
        checked = check_mobile_number_in_user(mobile_number)
        if not checked:
            result.set_error_list(['User is not Registered with this mobile number'],False)
            return JsonResponse({"data":ResultObjectSerializer(result).data},status=status.HTTP_400_BAD_REQUEST)
        verified = verify_otp(mobile_number,otp)
        if not verified:
            result.set_error_list(['OTP check is failed'],False)
            return JsonResponse({"data":ResultObjectSerializer(result).data},status=status.HTTP_400_BAD_REQUEST)
        serialized = LoginUserSerializer(data = request.data)
        try:
            if serialized.is_valid(raise_exception=True):        
                result.set_message_object("Welcome back "+mobile_number,serialized.validate(data=request.data),True)
                return JsonResponse({"data":ResultObjectSerializer(result).data}, status = status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"data":str(e)}, status = status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"message":"GET method not implemented"}, status = status.HTTP_400_BAD_REQUEST)





@api_view(["POST"])
@permission_classes([IsAuthenticated,])
def signout_view(request):
    try:
        jwt_token = request.headers['Authorization']
        if jwt_token[:4] == "JWT":
            token = jwt_token.split(' ')[1]
            logout_tokens.append(token)
        return JsonResponse({"message":"You are successfully signed out"},status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return JsonResponse({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated,])
def get_all_users(request):
    try:
        users_list = User.objects.all()
        return JsonResponse({"data":users_list},status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({"error_data":str(e)},status=status.HTTP_400_BAD_REQUEST)
