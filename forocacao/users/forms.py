# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField, LazyTypedChoiceField
from django_countries import countries

from .models import User
from forocacao.app.models import * 

class SignupForm(forms.Form):
    type = forms.ModelChoiceField(queryset=AttendeeType.objects.all(),label=_('Type'))
    first_name = forms.CharField(max_length=30, label=_('First name'))
    last_name = forms.CharField(max_length=30, label=_('Last name'))
    second_lastname = forms.CharField(max_length=30, label=_('Second Last name'),required=False)
    country = LazyTypedChoiceField(choices=countries)
    profession = forms.ModelChoiceField(queryset=Profession.objects.all(),label=_('Profession'))
    phone = forms.CharField(max_length=50, label=_('Phone'),required=False)
    sponsored = forms.BooleanField(label=_('Sponsored'),required=False)
    sponsor = forms.ModelChoiceField(queryset=Sponsor.objects.all(),label=_('Sponsor'))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.second_lastname = self.cleaned_data['second_lastname']
        user.phone = self.cleaned_data['phone']
        user.country = self.cleaned_data['country']
        user.type = self.cleaned_data['type']
        user.sponsored = self.cleaned_data['sponsored']
        user.sponsor = self.cleaned_data['sponsor']
        user.save()
