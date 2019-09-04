from django.shortcuts import render
from .models import Book,Author, BookInstance, Language, Genre
from django.views.generic import ListView, UpdateView, CreateView,DetailView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required # for function
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from  django.urls import reverse_lazy
# import form
from .forms import RenewBookForm

# Create your views here.from django.contrib.auth.decorators import login_required

def index(request):
    number_visits = request.session.get('number_visits', 0)
    request.session['number_visits'] = number_visits +1
    """ View function for home page of site """
    # Generate counts of some of the main objects
    num_of_books = Book.objects.all().count()
    num_of_book_instances = BookInstance.objects.all().count()
    num_of_book_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_of_book_authors = Author.objects.count()
    num_of_book_genre = Genre.objects.count()
    num_of_book_title_Science_fiction =  Genre.objects.filter(name__exact='Science Fiction').count()
    num_of_book_title_Fantacy = Genre.objects.filter(name__exact='Fantacy').count()
    num_of_book_title_Geography =  Genre.objects.filter(name__exact='Geography').count()

    context = {
        'num_of_books' : num_of_books,
        'num_of_book_instances' : num_of_book_instances,
        'num_of_book_instances_available' : num_of_book_instances_available,
        'num_of_book_authors' : num_of_book_authors,
        'num_of_book_genre':num_of_book_genre,
        'num_of_book_title_Science_fiction':num_of_book_title_Science_fiction,
        'num_of_book_title_Fantacy':num_of_book_title_Fantacy,
        'num_of_book_title_Geography':num_of_book_title_Geography,
        "number_visits": number_visits

    }

    return render(request, 'catalog/index.html', context=context)

# GENERIC Book List views

class BookListView(ListView):
    model = Book
    paginate_by = 2

    def get_context_data(self,  **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data (context dict)'
        context['second'] = '<br>6'
        return context

class BookDetailView(DetailView):
    model = Book


def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    total_available = BookInstance.objects.filter(status__exact='a').count()
    total_on_loan = BookInstance.objects.filter(status__exact='o').count()
    total_on_maintenance = BookInstance.objects.filter(status__exact='m').count()
    total_on_reserved = BookInstance.objects.filter(status__exact='r').count()
    context = {
        "book":book,
        "total_available" :  total_available   ,
        "total_on_loan"  :  total_on_loan   ,
        "total_on_maintenance" :  total_on_maintenance       ,
        "total_on_reserved"  :   total_on_reserved   ,

    }

    return render(request, 'catalog/book_detail.html', context=context)
# Author views

def author_detail_view(request, primary_key):
    author = get_object_or_404(Author, pk=primary_key)
    return render(request, 'catalog/author_detail.html', context={'author': author})

class AuthorListView(ListView):
    model = Author

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBookByUserListView(LoginRequiredMixin, ListView):
    """ Listing books on loan to ucrrent user"""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')



class LoanedAllBookListView(PermissionRequiredMixin,ListView):
    permission_required = 'catalog.can_mark_required'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return  BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_required')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance,pk=pk)
    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('catalog:book-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context ={
        'form': form,
        'book_instance' : book_instance
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(CreateView):
    model = Author
    fields = "__all__"
    initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(CreateView):
    model = Book
    fields = "__all__"

class BookUpdate(UpdateView):
    model = Book
    fields = "__all__"

class BookDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')



