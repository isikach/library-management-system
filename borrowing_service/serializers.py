import datetime

from django.db import transaction
from rest_framework import serializers

from book_service.serializers import BookSerializer
from borrowing_service.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )
        read_only_fields = ("id", "actual_return_date", "borrow_date",)

    def validate(self, attrs):
        data = super(BorrowingSerializer, self).validate(attrs)
        Borrowing.validate_book_inventory(
            attrs["book"].inventory,
            attrs["book"].title,
            attrs["book"].id,
        )
        if datetime.date.today() > attrs["expected_return_date"]:
            raise serializers.ValidationError(
                {
                    "borrow_date":
                    "expected_return_date must be after borrow_date"
                 }
            )
        return data

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data["book"]
            Borrowing.validate_book_inventory(
                book.inventory,
                book.title,
                book.id,
            )
            book.inventory -= 1
            book.save()
            validated_data["borrow_date"] = datetime.date.today()
            return Borrowing.objects.create(**validated_data)


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="email",
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingListSerializer(BorrowingSerializer):
    book = serializers.SlugRelatedField(
        slug_field="title",
        read_only=True,
    )
