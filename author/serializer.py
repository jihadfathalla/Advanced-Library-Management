from rest_framework import serializers

from author.models import Author
from book.serializers.book_serializer import BookDetailSerializer


class AuthorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"

    def to_representation(self, instance):
        action = self.context.get("action", None)
        if action == "list":
            representation = super().to_representation(instance)
            representation["book_count"] = instance.book_count
            return representation
        return super().to_representation(instance)


class AuthorDetailsSerializer(serializers.ModelSerializer):
    books = BookDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = "__all__"
