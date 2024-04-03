from rest_framework import viewsets, permissions

from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter

from book_service.models import Book
from book_service.serializers import BookSerializer


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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                description=(
                        "Search books by title or author,"
                        " ?search=title/author"
                ),
                type=str,
                required=False,
            ),
            OpenApiParameter(
                name="ordering",
                description="Order books by author ?ordering=author",
                type=str,
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)
