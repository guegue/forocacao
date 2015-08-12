# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_('First name'))
    last_name = forms.CharField(max_length=30, label=_('Last name'))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
