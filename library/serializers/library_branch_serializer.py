from rest_framework import serializers

from library.models.library_branch_model import Category
from library.models.library_branch_model import LibraryBranch


class LibraryBranchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = LibraryBranch
        exclude = ["library"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
