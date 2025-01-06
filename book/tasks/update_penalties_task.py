from celery import shared_task
from datetime import date
from book.models.borrow_book_model import BorrowedBook


@shared_task
def update_penalties():
    borrowed_books = BorrowedBook.objects.filter(
        returned=False, return_date__lt=date.today()
    )
    for book in borrowed_books:
        book.calculate_penalty()
