from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from library.models.library_model import Library
from library.models.library_branch_model import LibraryBranch
from book.models.book_model import Book
from book.models.book_inventory import BookInventory
from book.models.borrow_book_model import BorrowedBook


def roles(request):
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    librarian_group, _ = Group.objects.get_or_create(name="Librarian")
    member_group, _ = Group.objects.get_or_create(name="Member")

    library_ct = ContentType.objects.get_for_model(Library)
    libraryBranch_ct = ContentType.objects.get_for_model(LibraryBranch)

    book_ct = ContentType.objects.get_for_model(Book)
    book_inventory_ct = ContentType.objects.get_for_model(BookInventory)
    borrowed_book_ct = ContentType.objects.get_for_model(BorrowedBook)

    admin_permissions = Permission.objects.all()
    admin_group.permissions.set(admin_permissions)

    librarian_permissions = Permission.objects.filter(
        content_type__in=[
            book_ct,
            borrowed_book_ct,
            book_inventory_ct,
            library_ct,
            libraryBranch_ct,
        ]
    )
    librarian_group.permissions.set(librarian_permissions)

    member_permissions = Permission.objects.filter(
        codename__in=[
            "view_book",
            "add_borrowedbook",
            "change_borrowedbook",
        ]
    )
    member_group.permissions.set(member_permissions)

