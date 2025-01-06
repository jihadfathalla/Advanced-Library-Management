from django.db import models
from book.models.book_model import Book
from library.models.library_branch_model import LibraryBranch


class BookInventory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="inventory")
    branch = models.ForeignKey(
        LibraryBranch, on_delete=models.CASCADE, related_name="inventory"
    )
    available = models.BooleanField(default=True)

    class Meta:
        unique_together = (("book", "branch"),)

    def __str__(self):
        return f"{self.book.title} in {self.branch.branch_name}"
