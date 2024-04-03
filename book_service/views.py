from rest_framework import viewsets, permissions

from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema_view

from book_service.models import Book
from book_service.serializers import BookSerializer
from book_service.utils.schemas import book_list_schema

@extend_schema_view(
    list=book_list_schema()
)
class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "author"]
    ordering_fields = ["author"]

    def get_permissions(self):

        if self.action in ["update", "create", "partial_update", "delete"]:
            return [permissions.IsAdminUser()]

        elif self.action == "list":
            return [permissions.AllowAny()]

        elif self.action == "retrieve":
            return [permissions.IsAuthenticated()]

        return super().get_permissions()
