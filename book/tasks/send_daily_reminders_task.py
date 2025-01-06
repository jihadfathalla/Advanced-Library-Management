from celery import shared_task
from utils.send_email import send_email
from datetime import date, timedelta
from django.utils.translation import gettext as _

from book.models.borrow_book_model import BorrowedBook


@shared_task
def send_reminders():
    reminder_date = date.today() + timedelta(days=3)
    borrowed_books = BorrowedBook.objects.filter(
        returned=False, return_date__lte=reminder_date
    )

    for book in borrowed_books:
        data = {
            "subject": _("Return Reminder"),
            "message": f"Reminder: The book '{book.book_inventory.book.title}' is due on {book.return_date}.",
            "from_email": "noreply@library.com",
            "to_email": book.user.email,
        }
        send_email(data)
