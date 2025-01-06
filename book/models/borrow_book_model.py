from django.db import models
from datetime import date

from user.models import User
from book.models.book_inventory import BookInventory


class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_inventory = models.ForeignKey(BookInventory, on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()
    returned = models.BooleanField(default=False)
    penalty = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def calculate_penalty(self):
        if not self.returned and self.return_date < date.today():
            overdue_days = (date.today() - self.return_date).days
            self.penalty = overdue_days * 2.00
            self.save()
