from django.db import transaction
from rest_framework import serializers

from django.utils.translation import gettext as _


from library.models.library_model import Library
from library.models.library_branch_model import LibraryBranch
from library.serializers.library_branch_serializer import LibraryBranchSerializer


class LibrarySerializer(serializers.ModelSerializer):
    branches = LibraryBranchSerializer(many=True, required=True)

    class Meta:
        model = Library
        fields = "__all__"

    def validate_branches(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError(_("At least one branch is required."))
        return value

    def create(self, validated_data):
        branches = validated_data.pop("branches", [])
        with transaction.atomic():
            library = super().create(validated_data)
            self.create_branches(branches, library)
        return library

    def update(self, instance, validated_data):
        branches = validated_data.pop("branches", [])
        with transaction.atomic():
            library = super().update(instance, validated_data)

            self.delete_branches(library)
            self.create_branches(branches, library)
        return library

    def create_branches(self, branches, library):
        created_records = []
        for branch in branches:
            obj = LibraryBranch(
                library=library,
                **branch,
            )
            created_records.append(obj)

        LibraryBranch.objects.bulk_create(created_records)

    def delete_branches(self, library):
        library.branches.all().delete()
