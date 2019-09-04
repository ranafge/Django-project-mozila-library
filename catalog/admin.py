from django.contrib import admin
from .models import Book,BookInstance,Genre,Language,Author

class BookInline(admin.TabularInline):
    model = Book

class LangulageInline(admin.TabularInline):
    model = Language

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','date_of_birth','date_of_death','full_name',)
    fields = [('first_name', 'last_name'),('date_of_birth','date_of_death')]
    inlines = [BookInline]


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','display_genre')
    inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display =('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )