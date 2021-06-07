from django.shortcuts import get_object_or_404, render
from .models import *
from .serializers import * 
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateAPIView ,RetrieveUpdateDestroyAPIView,RetrieveAPIView
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from random import choice 
from django.core.mail import send_mail
from string import ascii_uppercase,ascii_lowercase,digits
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import get_default_password_validators
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.filters import OrderingFilter

class UserRegisterAPIView(ListCreateAPIView):
    
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer
    
    def perform_create(self, serializer):
          
        a= serializer.save()
       
        return a

    def get(self,request):
        response = {
            'message': 'Get Method Not Allowed'
            }
        return Response(response)


class UserLoginView(RetrieveAPIView):
    
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        user = authenticate(email=email, password=password)
        
        if user == None:
            response = {'message': 'User Not found'} 
        else:
            token = Token.objects.get(user=user).key
            
            response = {'token' : token , 'status' : status.HTTP_200_OK }

        return Response(response)

    def get(self,request):
        response = {
            'message': 'Get Method Not Allowed'
            }
        return Response(response)



class ForgotPasswordView(RetrieveAPIView):
    
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        email = request.data.get("email", None)
        user = Account.objects.filter(email=email)
        if user.exists(): 
            token = ChangePassword.objects.filter(user_id=user[0].id)
            
            if token.exists():
                key = token[0].key
                print(key)
            else:   
                t = ''.join([choice(ascii_uppercase + ascii_lowercase + digits) for n in range(20)]) 
                key = ChangePassword.objects.create(user_id=user[0].id,key=t)
                print(key)

            email_plaintext_message = "http://"+ request.META.get('HTTP_HOST')+"/changepassword/{}".format(key)
            send_mail(
                # title:
                "Password Reset for {title}".format(title="Some website title"),
                # message:
                email_plaintext_message,
                # from:
                "ecommercekarma@gmail.com",
                # to:
                [email]
            )
            response = {'email' : email}
        else:
            response={'message' : 'User does not Exist'}
        return Response(response)
    def get(self,request):
        response = {
            'message': 'Get Method Not Allowed'
            }
        return Response(response)

class ChangePasswordView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ChangePasswordSerializer

    def put(self,request,*args, **kwargs):
        password = request.data.get("password", None)
        confirm_password = request.data.get("confirm_password", None)
        obj = ChangePassword.objects.filter(key = self.kwargs.get('token'))

        errors = []
        password_validators=None
        if password_validators is None:
            password_validators = get_default_password_validators()
        for validator in password_validators:
            try:
                validator.validate(password)
            except ValidationError as error:
                errors.append(error)
        if errors:
            res = list(map(''.join, errors))
            response = {'message':res}

        else:
            if(obj.exists()):

                if(password != confirm_password):
                    response = {
                    'message': 'Password Not Match'
                    }
                else:
                    user = Account.objects.get(id=obj[0].user_id)
                    user.set_password(confirm_password)
                    user.save()

                    obj.delete()

                    response = {
                    'message': 'Password Change'
                    }
            else:
                response = {
                    'message': 'Token invalid'
                    }
            
        return Response(response)


    def get(self,*args, **kwargs):
        
        response = {
                'message': 'Get Method Not Allowed'
                }
        return Response(response)
        
        
class ProfileAPIView(ListCreateAPIView):
    queryset = profile.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProfileSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = '__all__'

    
    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        queryset = profile.objects.all()
        return queryset



class ProfileRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)


    def get_object(self):
        return get_object_or_404(profile, pk=self.kwargs.get("id"))


def validate_token(request,token):
    pass