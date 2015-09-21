# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView, DetailView

from .views import HomeView, ActivitiesView, AttendeeDetailView, AttendeeBadgeView, AttendeeJPEGView, AttendeeReceiptView, AttendeeMarkTrue, ContentView, event

from model_report import report
report.autodiscover()

urlpatterns = [

    # home
    url(r'^$', HomeView.as_view(), name='home'),

    # events' pages
    url(r'^(?P<slug>[\w-]+)/about/$', ContentView.as_view(page='about'), name='about'),
    url(r'^(?P<slug>[\w-]+)/services/$', ContentView.as_view(page='services'), name='services'),
    url(r'^(?P<slug>[\w-]+)/contact/$', ContentView.as_view(page='contact'), name='contact'),
    url(r'^(?P<slug>[\w-]+)/activities/$', ActivitiesView.as_view(), name='activities'),

    # attendees' pages
    url(r'^attendee/(?P<username>[\w.@+-]+)/$',AttendeeDetailView.as_view(), name='detail'),
    url(r'^attendee/(?P<username>[\w.@+-]+)/badge/$',AttendeeBadgeView.as_view(), name='badge'),
    url(r'^attendee/(?P<username>[\w.@+-]+)/jpeg/$',AttendeeJPEGView.as_view(), name='jpeg'),
    url(r'^attendee/(?P<username>[\w.@+-]+)/receipt/$',AttendeeReceiptView.as_view(), name='receipt'),
    url(r'^attendee/(?P<username>[\w.@+-]+)/markTrue/(?P<field>[\w]+)/$',AttendeeMarkTrue, name='marktrue'),

    # reports
    url(r'^report/', include('model_report.urls')),

    # events : /myevent
    url(r'^(?P<url>.*/)$', event, name='event'),

]
