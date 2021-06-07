from rest_framework import serializers
from rest_framework import fields
from .models import *
from rest_framework.authtoken.models import Token
import django.contrib.auth.password_validation as validators
from rest_framework import status


class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True,style={"input_type":"password"})
    status = serializers.CharField(read_only=True)
    
    class Meta:
        model = Account
        fields = ('email','password','status')
       
    def validate_password(self, data):
            validators.validate_password(password=data, user=Account)
            return data 

    def create(self, validated_data):
        user = Account.objects.create(
          
            email = validated_data['email'],
        ) 

        user.set_password(validated_data['password'])
        user.save()

        response = {
            'email': validated_data['email'],
            'status': status.HTTP_200_OK
        }

        return response



class UserLoginSerializer(serializers.ModelSerializer):
    
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True,style={"input_type":"password"})

    class Meta:
        model = Account
        fields = ['email','password']



class ForgotPasswordSerializer(serializers.ModelSerializer):
    
    email = serializers.CharField(max_length=255)
    
    class Meta:
        model = Account
        fields = ['email']


class ChangePasswordSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(max_length=255,style={"input_type":"password"})
    confirm_password = serializers.CharField(max_length=255,style={"input_type":"password"})

    class Meta:
        model = Account
        fields = ['password','confirm_password']
        validators = []  


    def validate(self, data):
        validators.validate_password(password=data, user=Account)
        return data
    
    
class ProfileSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = profile
        fields = '__all__'

