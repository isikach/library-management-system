from drf_spectacular.utils import extend_schema, OpenApiParameter


def book_list_schema():
    return extend_schema(
        description=(
            "Endpoint for representing a list of books "
            "with filtering options by title and author."
        ),
        parameters=[
            OpenApiParameter(
                name="search",
                type=str,
                description="Search books by title or author (e.g., ?search=title/author)",
                required=False,
            ),
            OpenApiParameter(
                name="ordering",
                type=str,
                description="Sort books by author (e.g., ?ordering=author)",
                required=False,
            ),
        ]
    )
