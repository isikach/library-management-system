import stripe
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from payment_service.models import Payment
from payment_service.serializers import (
    PaymentSerializer,
    PaymentSuccessSerializer,
)
from payment_service.utils.services import PaymentService


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(user=self.request.user)

    @action(
        methods=["GET"],
        detail=False,
        url_path="success",
        url_name="success",
    )
    def success_payment(self, request, *args, **kwargs):
        serializer = PaymentSuccessSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        session_id = serializer.validated_data.get("session_id")

        try:
            PaymentService.set_status_as_paid(session_id)
            return Response(
                {"message": f"Thanks for your payment {request.user.email}!"},
                status=status.HTTP_200_OK
            )
        except stripe.error.InvalidRequestError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["GET"],
        detail=False,
        url_path="cancel",
        url_name="cancel",
    )
    def cancel_payment(self, request, *args, **kwargs):
        data = {"info": "You have 24 hours to pay your borrowing"}
        return Response(data, status=status.HTTP_200_OK)
