from django.db import transaction
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
        )
        read_only_fields = ("actual_return_date", "borrow_date",)

    def validate(self, attrs):
        data = super(BorrowingSerializer, self).validate(attrs)
        Borrowing.validate_book_inventory(
            attrs["book"].inventory,
            attrs["book"].title,
            attrs["book"].id,
        )
        return data

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data.pop("book")
            book.inventory -= 1
            book.save()

            return Borrowing.objects.create(**validated_data)


class BorrowingDetailSerializer(BorrowingSerializer):
    # TODO book=BookDetailSerializer
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="email",
    )


class BorrowingListSerializer(BorrowingSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="email",
    )
    book = serializers.SlugRelatedField(
        slug_field="title",
        read_only=True,
    )

