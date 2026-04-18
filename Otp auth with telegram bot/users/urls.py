from django.urls import path
from users.views import SendOTPView, VerifyOTPView,RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name = 'register'),
    path("send-otp/", SendOTPView.as_view(), name = 'send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
]
