from drf_spectacular.utils import extend_schema, OpenApiParameter


def borrowing_list_schema():
    return extend_schema(
        description=(
            "Endpoint for representation list of borrowings "
            "with filtering by active borrowings and specific user."
        ),
        parameters=[
            OpenApiParameter(
                "is_active",
                type=str,
                description="Filter active borrowings (ex. ?is_active=true)"
            ),

            OpenApiParameter(
                "user_id",
                type=int,
                description=(
                    "Filter borrowing of the specific"
                    " user(only for admin) ex. ?user_id=2"
                )
            )
        ]
    )
