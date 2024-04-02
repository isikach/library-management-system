import datetime

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowing_service.models import Borrowing
from borrowing_service.serializers import (
    BorrowingSerializer,
    BorrowingDetailSerializer,
    BorrowingListSerializer
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        queryset = self.queryset

        if is_active := self.request.query_params.get("is_active", False):
            queryset = queryset.filter(actual_return_date__isnull=True)

        if self.request.user.is_staff:

            if user_id := self.request.query_params.get("user_id"):
                queryset = queryset.filter(user_id=user_id)

        else:
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["POST"], detail=True, url_path="return")
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()

        if borrowing.actual_return_date:
            return Response(
                "This borrowing has already been returned.",
                status=status.HTTP_400_BAD_REQUEST
            )

        borrowing.actual_return_date = datetime.date.today()
        borrowing.book.inventory += 1
        borrowing.book.save()
        borrowing.save()

        return Response("Successfully returned.", status=status.HTTP_200_OK)
