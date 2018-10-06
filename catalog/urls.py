from django.conf.urls import url
from .views import (
    BookListView,
    index,
    BookInstance,
    Book,
    BookDetailView,
    AuthorListView,
    AuthorDetailView,
    LoanedBooksByUserListView,
    LoanedBooksByAllUserListView
)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^books/$', BookListView.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)$', BookDetailView.as_view(), name='book-detail'),
    url(r'^authors/$', AuthorListView.as_view(), name='authors'),
    url(r'^author/(?P<pk>\d+)$', AuthorDetailView.as_view(), name='author-detail'),
    url(r'^mybooks/', LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    url(r'^loanbooks/', LoanedBooksByAllUserListView.as_view(), name='borrowed-book')
]