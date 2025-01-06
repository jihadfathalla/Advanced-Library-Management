from rest_framework import serializers
from datetime import timedelta, date

from utils.send_email import send_email
from notification_channels.notify_book_returned_view import notify_book_returned

from django.utils.translation import gettext as _

from book.models.book_inventory import BookInventory
from book.models.borrow_book_model import BorrowedBook


class BorrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = [
            "return_date",
            "book_inventory",
        ]

    def validate_book_inventory(self, value):
        if not BookInventory.objects.filter(id=value.id, available=True).exists():
            raise serializers.ValidationError(
                "Sorry, but this Book is not available in this branch right now."
            )
        return value

    def validate_return_date(self, value):
        max_return_date = date.today() + timedelta(days=30)
        if value > max_return_date:
            raise serializers.ValidationError(
                "The return date cannot exceed 1 month from today."
            )
        return value

    def validate(self, data):
        user = self.context.get("user")
        errors = {}
        borrowed_count = BorrowedBook.objects.filter(user=user, returned=False).count()
        if borrowed_count >= 3:
            errors["book"] = (
                "You cannot borrow more than 3 books. Return a book to borrow another."
            )
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        user = self.context.get("user")
        validated_data["user"] = user
        validated_data["borrowed_date"] = date.today()

        borrowed_book = super().create(validated_data=validated_data)
        book = borrowed_book.book_inventory
        book.available = False
        book.save()
        data = {
            "subject": "Borrowing Confirmation",
            "message": f"You have borrowed '{borrowed_book.book_inventory.book.title}'. Return it by {borrowed_book.return_date}.",
            "from_email": "noreply@library.com",
            "to_email": user.email,
        }
        send_email(data)
        return borrowed_book


class ReturnBookSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.borrowed_book = None

    class Meta:
        model = BorrowedBook
        fields = [
            "book_inventory",
        ]

    def validate_book_inventory(self, value):
        user = self.context.get("user")
        borrowed_book = BorrowedBook.objects.filter(
            user=user, book_inventory_id=value, returned=False
        ).first()
        if not borrowed_book:
            raise serializers.ValidationError(_("No record of borrowing this book."))

        self.borrowed_book = borrowed_book
        return value

    def validate_return_date(self, value):
        max_return_date = date.today() + timedelta(days=30)
        if value > max_return_date:
            raise serializers.ValidationError(
                _("The return date cannot exceed 1 month from today.")
            )
        return value

    def create(self, validated_data):
        borrowed_book = self.borrowed_book
        borrowed_book.returned = True
        borrowed_book.return_date = date.today()
        borrowed_book.save()
        book = borrowed_book.book_inventory
        book.available = True
        book.save()

        notify_book_returned(
            borrowed_book.book_inventory.book.title,
            borrowed_book.book_inventory.branch.branch_name,
        )
        borrowed_book.calculate_penalty()

        return borrowed_book
