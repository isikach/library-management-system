from rest_framework import viewsets, mixins

from borrowing_service.models import Borrowing
from borrowing_service.serializers import BorrowingSerializer, BorrowingDetailSerializer, BorrowingListSerializer


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer

        if self.action == "retrieve":
            return BorrowingDetailSerializer

        return self.serializer_class
