from rest_framework import serializers

from borrowing_service.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )
        read_only_fields = ("actual_return_date", "borrow_date",)


class BorrowingDetailSerializer(BorrowingSerializer):
    # TODO book=BookDetailSerializer
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="email"
    )


class BorrowingListSerializer(BorrowingSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="email"
    )
    book = serializers.SlugRelatedField(
        slug_field="title"
    )

