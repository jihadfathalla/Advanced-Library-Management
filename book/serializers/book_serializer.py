from django.db import transaction
from rest_framework import serializers
from django.utils.translation import gettext as _

from book.models.book_model import Book
from book.models.book_inventory import BookInventory
from library.serializers.library_branch_serializer import CategorySerializer


class BookDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Book
        fields = "__all__"


class BookListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "__all__"

    def to_representation(self, instance):
        action = self.context.get("action", None)
        if action == "list":
            representation = super().to_representation(instance)
            representation["author"] = instance.author.name
            representation["category"] = instance.category.name
            return representation
        return super().to_representation(instance)


class BookCreateSerializer(serializers.ModelSerializer):
    branches = serializers.ListField(required=True)

    class Meta:
        model = Book
        fields = "__all__"

    def validate_branches(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError(_("At least one branch is required."))
        return value

    def create(self, validated_data):
        branches = validated_data.pop("branches", [])
        with transaction.atomic():
            book = super().create(validated_data)
            self.create_inventories(branches, book)
        return book

    def update(self, instance, validated_data):
        branches = validated_data.pop("branches", [])
        with transaction.atomic():
            book = super().update(instance, validated_data)

            self.delete_inventories(book)
            self.create_inventories(branches, book)
        return book

    def create_inventories(self, branches, book):
        created_records = []
        for branch in branches:
            obj = BookInventory(book=book, branch_id=branch)
            created_records.append(obj)

        BookInventory.objects.bulk_create(created_records)

    def delete_inventories(self, book):
        book.inventory.all().delete()
