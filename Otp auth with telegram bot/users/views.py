import random
import uuid
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import OTP, User
from rest_framework.permissions import AllowAny
from .serializers import VerifyOTPSerializer,SendOTPSerializer


class RegisterView(APIView):
    def post(self, request):
        session_id = str(uuid.uuid4())

        return Response({
            "session_id": session_id,
            "bot_link": f"https://t.me/otpauthtest_bot?start={session_id}"
            })

class SendOTPView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = SendOTPSerializer

    def post(self, request):
        try:
            print("📥 REQUEST DATA:", request.data)

            serializer = SendOTPSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            phone = serializer.validated_data["phone"]
            session_id = serializer.validated_data["session_id"]
            telegram_id = serializer.validated_data["telegram_id"]

            print("✅ VALIDATED:", phone, session_id, telegram_id)

            otp_code = str(random.randint(100000, 999999))

            otp_obj = OTP.objects.create(
                session_id=session_id,
                phone=phone,
                telegram_id=telegram_id,
                otp=otp_code
            )

            print("✅ SAVED OTP:", otp_obj.id)

            return Response({
                "status": "ok",
                "otp": otp_code
            })

        except Exception as e:
            print("🔥 ERROR:", e)

            return Response({
                "error": str(e)
            }, status=500)

class VerifyOTPView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session_id = serializer.validated_data["session_id"]
        otp = serializer.validated_data["otp"]

        try:
            otp_obj = OTP.objects.filter(
            session_id=session_id,
            otp=otp,
            is_used=False
            ).first()
            
            if not otp_obj:
                return Response({
                    "status": "error",
                    "message": "OTP not found or already used"
                })
            otp_obj.is_used = True
            otp_obj.save()

            user, created = User.objects.get_or_create(
                telegram_id=otp_obj.telegram_id,
                defaults={
                    "phone": otp_obj.phone
                }
            )
            if created:
                return Response({
                    "status": "registered",
                    "user": {
                        "telegram_id": user.telegram_id,
                        "phone": user.phone
                    }
                })
            else:
                return Response({
                    "status": "login",
                    "message": "Siz oldin ro'yxatdan o'tgansiz",
                    "user": {
                        "telegram_id": user.telegram_id,
                        "phone": user.phone
                    }
                })
        
        except Exception as e:
            return Response({"status": "error"})