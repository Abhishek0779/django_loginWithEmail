
from django.urls import path
from .views import *
urlpatterns = [
    path('register/',UserRegisterAPIView.as_view(),name="UserRegisterAPIView"),
    path('login/',UserLoginView.as_view(),name="UserLoginView"),
    path('profile/',ProfileAPIView.as_view(),name="ProfileAPIView"),
    path('profile/<int:id>/edit/',ProfileRetrieveUpdateDestroyAPIView.as_view(),name="ProfileRetrieveUpdateDestroyAPIView"),
    path('forgotpassword/',ForgotPasswordView.as_view(),name="ForgotPasswordView"),
    path('changepassword/<str:token>',ChangePasswordView.as_view(),name="ChangePasswordView"),
    
]
