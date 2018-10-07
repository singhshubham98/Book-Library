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
    LoanedBooksByAllUserListView,
    renew_book_librarian,
    AuthorCreate,
    AuthorUpdate,
    AuthorDelete,
    BookCreate,
    BookUpdate,
    BookDelete,
)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^books/$', BookListView.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)$', BookDetailView.as_view(), name='book-detail'),
    url(r'^authors/$', AuthorListView.as_view(), name='authors'),
    url(r'^author/(?P<pk>\d+)$', AuthorDetailView.as_view(), name='author-detail'),
    url(r'^mybooks/', LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    url(r'^loanbooks/', LoanedBooksByAllUserListView.as_view(), name='borrowed-book'),
    url(r'^book/<uuid:pk>/renew/', renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [  
    url('author/create/', AuthorCreate.as_view(), name='author_create'),
    url('author/(?P<pk>\d+)/update/', AuthorUpdate.as_view(), name='author_update'),
    url('author/(?P<pk>\d+)/delete/', AuthorDelete.as_view(), name='author_delete'),
]

urlpatterns += [  
    url('book/create/', BookCreate.as_view(), name='book_create'),
    url('book/(?P<pk>\d+)/update/', BookUpdate.as_view(), name='book_update'),
    url('book/(?P<pk>\d+)/delete/', BookDelete.as_view(), name='book_delete'),
]