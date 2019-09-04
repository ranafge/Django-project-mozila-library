
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import BookListView, AuthorListView

app_name='catalog'

urlpatterns = [
    path('',views.index, name='index'),
    path('books/', BookListView.as_view(), name='books'),
    path('book/<int:primary_key>/', views.book_detail_view, name='book-detail'),

]

urlpatterns += [
    path('author/<int:primary_key>/', views.author_detail_view, name='author-detail'),
    path('authors/', AuthorListView.as_view(), name='authors'),
]

# borrower by user
urlpatterns += [
    path('mybooks/', views.LoanedBookByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.LoanedAllBookListView.as_view(), name='book-borrowed'),
]

# book renewal data url

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]


urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
]


urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
]