from django.db import models
from django.urls import reverse  # used to genereate urls by reversing the url patterns
from django.contrib.auth.models import User
import uuid
from django.db.models import Value
from django.db.models.functions import Concat
from datetime import date

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter book genre (e.g. science)')
    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=100, help_text='Enter the language (e.g. ENGLISH, Bangla)')

    def __str__(self):
        return f"{self.name}"

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter brief desction of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)


    def display_genre(self):
        return ','.join(genre.name for genre in self.genre.all()[:4])
    display_genre.short_discriptions = 'Genre'

    def __str__(self):
        return "{} {}".format(self.title,self.author)

    def get_absolute_url(self):
        """Return the url ot access a detail record for this book"""
        return reverse('catalog:book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    "Model representiang a speco copy of book"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(max_length=1,
                              choices=LOAN_STATUS,
                              blank=True,
                              default='m',
                              help_text='Book availablity'
                              )

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned', 'set book as returned'),
                       ('can_mark_retunred_admin', 'set book as returned admin'),
                       )

    def __str__(self):
        return f"{self.book.title} ({self.id} )"


    @property
    def is_overdue(self):
        if self.due_back  and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = [ 'last_name', 'first_name']


    def get_absolute_url(self):
        return reverse('catalog:author-detail', args=[str(self.id)])

    def full_name(self):
        return self.first_name + ' ' + self.last_name
    full_name.admin_order_field = Concat('first_name', Value(' '), 'last_name')

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"











