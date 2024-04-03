from django.shortcuts import render, get_object_or_404
from .models import Book, Author, BookInstance, Genre, Language
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from catalog.forms import RenewBookModelForm
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.apps import apps

# Home
def index(request):
    '''View function for home page of site.'''

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_genres = Genre.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # Available books (title = 'a')
    num_books_with_the = Book.objects.filter(title__icontains='the').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_with_the': num_books_with_the,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

# List view
class GenericListView(generic.ListView):
    template_name = 'list_generic.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self):
        model_name = self.kwargs['model_name']
        model = apps.get_model('catalog', model_name)
        return model.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.kwargs['model_name']
        return context
    
# Detail views
# Book details
class BookDetailView(generic.DetailView):
    model = Book

# Author details
class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.object
        context['books'] = author.book_set.all() 
        return context
    
# Genre details
class GenreDetailView(generic.DetailView):
    model = Genre

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre = self.object
        context['books'] = genre.book_set.all() 
        return context
    
# Language details
class LanguageDetailView(generic.DetailView):
    model = Language

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = self.object
        context['books'] = language.book_set.all() 
        return context
    
# Book Instance details
class BookInstanceDetailView(generic.DetailView):
    model = BookInstance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookinstance = self.object
        context['books'] = bookinstance
        return context

# Create view
class GenericCreateView(PermissionRequiredMixin, CreateView):
    # Gets model from kwargs
    def get_model(self):
        # Retrieve the model_name from URL parameters
        model_name = self.kwargs['model_name']

        # Fetch the actual model class based on the model_name
        return apps.get_model('catalog', model_name)
    
    # Get fields based on dictionary 
    def get_fields(self):
        # Dictionary to map model_name to fields - default is all
        fields_map = {
            'Book': ['title', 'author', 'summary', 'isbn', 'genre', 'language'],
            'Author': ['first_name', 'last_name', 'date_of_birth', 'date_of_death'],  
            'Genre': ['name'],
            'Language': ['name'],
            'BookInstance' : ['book', 'imprint', 'due_back', 'borrower', 'status'], 
        }

        # Fetch fields based on model_name from the dictionary
        model_name = self.kwargs['model_name']
        return fields_map.get(model_name, '__all__') 
    
    # Check if user has required permissions based on model_name
    def get_permission_required(self):
        model_name = self.kwargs['model_name']
        return ['catalog.add_' + model_name.lower()]
      
    # Redirect to a success URL after creating the object
    def get_success_url(self):
        # Go back to generic-list with model_name passed in
        return reverse('generic-list', kwargs={'model_name': self.kwargs['model_name']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.kwargs['model_name']
        return context
    
    # Pass in 
    template_name = 'form_generic.html'
    model = property(get_model)
    fields = property(get_fields)
    permission_required = property(get_permission_required)
    success_url = property(get_success_url)

# Update view
class GenericUpdateView(PermissionRequiredMixin, UpdateView):
    # Gets model from kwargs
    def get_model(self):
        # Retrieve the model_name from URL parameters
        model_name = self.kwargs['model_name']

        # Fetch the actual model class based on the model_name
        return apps.get_model('catalog', model_name)
    
    # Get fields based on dictionary 
    def get_fields(self):
        # Dictionary to map model_name to fields - default is all
        fields_map = {
            'BookInstance' : ['book', 'imprint', 'due_back', 'borrower', 'status'], 
        }

        # Fetch fields based on model_name from the dictionary
        model_name = self.kwargs['model_name']
        return fields_map.get(model_name, '__all__') 
    
    # Check if user has required permissions based on model_name
    def get_permission_required(self):
        model_name = self.kwargs['model_name']
        return ['catalog.change_' + model_name.lower()]
      
    # Redirect to a success URL after creating the object
    def get_success_url(self):
        # Go back to generic-list with model_name passed in
        return reverse('generic-list', kwargs={'model_name': self.kwargs['model_name']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.kwargs['model_name']
        return context
    
    # Pass in 
    template_name = 'form_generic.html'
    model = property(get_model)
    fields = property(get_fields)
    permission_required = property(get_permission_required)
    success_url = property(get_success_url)

# Delete view
class GenericDeleteView(PermissionRequiredMixin, DeleteView):
    # Gets model from kwargs
    def get_model(self):
        # Retrieve the model_name from URL parameters
        model_name = self.kwargs['model_name']

        # Fetch the actual model class based on the model_name
        return apps.get_model('catalog', model_name)
    
    # Check if user has required permissions based on model_name
    def get_permission_required(self):
        model_name = self.kwargs['model_name']
        return ['catalog.delete_' + model_name.lower()]
      
    # Redirect to a success URL after creating the object
    def get_success_url(self):
        # Go back to generic-list with model_name passed in
        return reverse('generic-list', kwargs={'model_name': self.kwargs['model_name']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.kwargs['model_name']
        return context
    
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse('book-delete', kwargs={'pk': self.object.pk})
            )
    
    # Pass in 
    template_name = 'confirm_delete_generic.html'
    model = property(get_model)
    permission_required = property(get_permission_required)
    success_url = property(get_success_url)


# List showing loaned books
class LoanedBooksListView(LoginRequiredMixin,generic.ListView):
    '''Generic class-based view listing books on loan.'''
    model = BookInstance
    template_name = 'catalog/bookinstance_borrowed_list.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o')
            .order_by('due_back')
        )

# List showing a user's borrowed books
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    '''Generic class-based view listing books on loan to current user.'''
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

# Book Instance renewal/borrow/return
# Allow librarian to renew loaned and overdue books
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=4)
        form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

# Allow librarian to mark books as returned
def book_return_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Sets status of book_instance to 'o' and sets borrower to current user and due date four weeks out from now
    if request.method == 'POST':
        book_instance.status = 'a'  # Set status to 'a' for 'Available'
        book_instance.borrower = None
        book_instance.due_back = None
        book_instance.save()

        return HttpResponseRedirect(reverse('borrowed'))
    
    context = {
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_return.html', context)

# Allow users to borrow books   
def book_borrow(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Sets status of book_instance to 'o' and sets borrower to current user and due date four weeks out from now
    if request.method == 'POST':
        book_instance.status = 'o'  # Set status to 'o' for 'On loan'
        book_instance.borrower = request.user
        book_instance.due_back = datetime.date.today() + datetime.timedelta(weeks=4)
        book_instance.save()

        return HttpResponseRedirect(reverse('my-borrowed'))
    
    context = {
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_borrow.html', context)