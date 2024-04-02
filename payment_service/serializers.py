from rest_framework import serializers

from payment_service.models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "payment_type",
            "borrowing",
            "session_url",
            "session_id",
            "money_to_pay",
        )


class PaymentBorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "payment_type",
            "session_url",
            "money_to_pay"
        )


class PaymentSuccessSerializer(serializers.Serializer):
    session_id = serializers.CharField(max_length=100)
