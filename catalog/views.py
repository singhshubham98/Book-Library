from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from catalog.models import Book, Genre,BookInstance, Language, Author
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

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
        'num_visits' : num_visits,
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

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/Book/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact='o').order_by('due_back')
   
class LoanedBooksByAllUserListView(ListView):
    model = BookInstance
    template_name ='catalog/Book/bookinstance_list_all_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact = 'o').order_by('due_back')


class MyView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_mark_returned'
    # Or multiple permissions
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    # Note that 'catalog.can_edit' is just an example
    # the catalog application doesn't have such permission!


import datetime
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        book_renewal_form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if book_renewal_form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('borrowed-book') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': book_renewal_form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/Book/book_renew_librarian.html', context)



from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Author,Book

#Author 
class AuthorCreate(CreateView):
    model   = Author
    fields  = '__all__'
    initial = {'date_of_death' : '05/01/2090'} 

class AuthorUpdate(UpdateView):
    model   = Author
    fields  = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model   = Author
    success_url = reverse_lazy('authors')


#BOOK

class BookCreate(CreateView):
    model    = Book
    fields   = '__all__'

class BookUpdate(UpdateView):
    model    = Book
    fields   = '__all__'

class BookDelete(DeleteView):
    model   = Book
    success_url  = reverse_lazy('books') 