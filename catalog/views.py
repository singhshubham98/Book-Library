from django.shortcuts import render
from django.views.generic import ListView, DetailView
from catalog.models import Book, Genre,BookInstance, Language, Author

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()

    # num_genre = Genre.objects.filter(status__exact='a').count()

    num_book  = Book.objects.filter(title__iexact='cryptography').count()
    
    context = {
        # 'num_genre' : num_genre,
        'num_book' : num_book,
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(ListView):
    model = Book
    template_name = 'catalog/Book/book_list.html'
    paginate_by = 2

class BookDetailView(DetailView):
    model = Book
    template_name = 'catalog/Book/book_detail.html'
    paginate_by = 2

class AuthorListView(ListView):
    model = Author
    template_name = 'catalog/Author/author_list.html'
    paginate_by = 2

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'catalog/Author/author_detail.html'
    paginate_by = 2

   