from rest_framework import serializers

class VerifyOTPSerializer(serializers.Serializer):
    session_id = serializers.CharField()
    otp = serializers.CharField(max_length=6)


class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    session_id = serializers.CharField()
    telegram_id = serializers.IntegerField()