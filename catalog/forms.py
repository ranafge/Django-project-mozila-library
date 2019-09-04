import datetime
from django.forms import ModelForm
from .models import BookInstance
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='Date between not and 4 weeks')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalide date - renewal more than 4 weeks ahead'))
        return data


class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renael to past'))
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        return data

    class Meta:
            model = BookInstance
            fields = "__all__"
            labels = {'due_back': _('New reneal date')}
            help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}
