from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.index, name='index'),

    # Generic list view
    path('<str:model_name>/', views.GenericListView.as_view(), name='generic-list'),

    # Generic create view
    path('<str:model_name>/create/', views.GenericCreateView.as_view(), name='create'),

    # Generic update views - With int pk & uuid pk
    path('<str:model_name>/<int:pk>/update/', views.GenericUpdateView.as_view(), name='update'),
    path('<str:model_name>/<uuid:pk>/update/', views.GenericUpdateView.as_view(), name='update-uuid'),

    # Generic delete views
    path('<str:model_name>/<int:pk>/delete/', views.GenericDeleteView.as_view(), name='delete'),
    path('<str:model_name>/<uuid:pk>/delete/', views.GenericDeleteView.as_view(), name='delete-uuid'),

    # Detail views
    # Book
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),

    # Author
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
   
    # Genre
    path('genre/<int:pk>', views.GenreDetailView.as_view(), name='genre-detail'),

    # Language
    path('language/<int:pk>', views.LanguageDetailView.as_view(), name='language-detail'),

    # BookInstance
    path('bookinstance/<uuid:pk>', views.BookInstanceDetailView.as_view(), name='bookinstance-detail'),

    # Renewal/borrow/return & user books
    path('books/borrowed/', views.LoanedBooksListView.as_view(), name='borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('book/<uuid:pk>/borrow/', views.book_borrow, name='borrow-book'),
    path('book/<uuid:pk>/return/', views.book_return_librarian, name='return-book-librarian'),
    path('books/mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]